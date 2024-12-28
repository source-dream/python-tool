import zlib
from flask.sessions import session_json_serializer, SecureCookieSessionInterface
from flask import Flask
import os
from itsdangerous import base64_decode

def coookie_to_session(cookie):
    payload = cookie.encode()
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)
    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True
    payload = base64_decode(payload)
    if decompress:
        payload = zlib.decompress(payload)
    return session_json_serializer.loads(payload)

def session_to_cookie(session):
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.dumps(session)

if __name__ == '__main__':
    # 如果config.py不存在则生成
    if not os.path.exists('config.py'):
        with open('config.py', 'w') as f:
            f.write("secret_key = ''\ncookie = ''\nsession = {}")
    app = Flask(__name__)
    from config import secret_key, cookie, session
    if cookie:
        print("cookie_to_session", coookie_to_session(cookie))
    if secret_key and session:
        app.secret_key = secret_key
        print("session_to_cookie", session_to_cookie(session))