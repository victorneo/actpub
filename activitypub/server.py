import json
import requests
import base64, hashlib, hmac, time
import email.utils
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from urllib.parse import urlparse
from db.db import async_session
from models.users import RemoteUser
from sqlmodel import select
from activitypub.activitystreams import ActivityTypes


async def send_activity(private_key: str, user_id: str, target_id: str, body: dict):
    # 1. Fetch target inbox
    # 1.1 Check if we know the user's inbox
    async with async_session() as s:
        statement = select(RemoteUser).where(RemoteUser.remote_id == target_id)
        results = await s.execute(statement)
        user = results.first()
    
    if user:
        inbox = user[0].inbox
    else:
        # 1.2 If not, fetch from remote server
        resp = requests.get(target_id, headers={'accept': 'application/activity+json'})
        target = resp.json()
        inbox = target['inbox']

        remote_user = RemoteUser(remote_id=target_id, inbox=target['inbox'], public_key=target['publicKey']['publicKeyPem'])
        async with async_session() as s:
            s.add(remote_user)
            await s.commit()
    
    # 2. Send activity to target inbox
    private_key = serialization.load_pem_private_key(private_key.encode('utf-8'), password=None)
    urlparts = urlparse(target_id)

    m = hashlib.sha256()
    m.update(json.dumps(body).encode('utf-8'))
    digestHash = base64.b64encode(m.digest()).decode()

    created_timestamp = int(time.time())
    header_time = email.utils.formatdate(created_timestamp, usegmt=True)

    toSign = '(request-target): post {}\nhost: {}\ndate: {}\ndigest: SHA-256={}'.format(
        urlparts.path,
        urlparts.netloc,
        header_time,
        digestHash
    )

    signed = private_key.sign(
        toSign.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    signature = 'keyId="{}#main-key",headers="(request-target) host date digest",signature="{}"'.format(
        user_id,
        base64.b64encode(signed).decode(),
    )
    headers = {
        'Content-type': 'application/ld+json',
        'Host': urlparts.netloc,
        'Date': header_time,
        'Signature': signature,
        'Digest': 'SHA-256={}'.format(digestHash)
    }
    resp = requests.post(inbox, json=body, headers=headers)
    print(resp.text)