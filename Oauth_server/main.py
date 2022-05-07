from datetime import datetime, timedelta
from flask import Flask, abort, jsonify, request
from flask_caching import Cache
import threading
import time
import requests
import dotenv
import os
import logging
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


dotenv.load_dotenv()
eztexting_username              = os.getenv('EZTEXTING_USERNAME')
eztexting_password              = os.getenv('EZTEXTING_PASSWORD')
eztexting_url                   = os.getenv('EZTEXTING_URL', 'https://a.eztexting.com/v1')
shared_secret                   = os.getenv('SHARED_SECRET', None)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)

with app.app_context():
    class Token:
        def __init__(self, accessToken='unitialized', refreshToken='unitialized', expires_at_isoformat='unitialized'):
            self.accessToken = accessToken
            self.refreshToken = refreshToken
            self.expires_at_isoformat = expires_at_isoformat

    def generate_tokens_continuously(token: Token=None, appKey=None, appSecret=None):
        while True:
            response = requests.request(
                method='POST',
                url=f'{eztexting_url}/tokens/create',
                json={'appKey': appKey, 'appSecret': appSecret}
            )

            if response.ok:
                token.accessToken = response.json.get('accessToken')
                token.refreshToken = response.json.get('refreshToken')
                token.expires_at_isoformat = (datetime.now() + timedelta(response.json.get('expiresInSeconds'))).isoformat()
            else:
                if os.getenv('DEBUG', False):
                    token.accessToken = 'asdfo23109fd'
                    token.refreshToken = '1309jsa[knd'
                    token.expires_at_isoformat = (datetime.now() + timedelta(seconds=5400)).isoformat()
                else:
                    raise

            cache.set('accessToken', token.accessToken)
            cache.set('refreshToken', token.refreshToken)
            cache.set('expires_at_isoformat', token.expires_at_isoformat)

            time.sleep(300)

    @app.route('/generate_token', methods=['GET'])
    async def main():
        print(request.headers)
        try:
            request.headers.get('Shared-Secret') == shared_secret
        except:
            abort(403)

        try:
            return jsonify({
                'accessToken': cache.get('accessToken'),
                'refreshToken': cache.get('refreshToken'),
                'expires_at_isoformat': cache.get('expires_at_isoformat')
            })

        except Exception as e:
            print(e)
            abort(403)

if __name__ == '__main__':
    token = Token()
    f = threading.Thread(target=generate_tokens_continuously, args=[token, eztexting_username, eztexting_password])
    f.start()
    logger.info(f'thread startup: {f.getName()} {f.is_alive()}')
    app.run(port=8888)