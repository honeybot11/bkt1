import aiohttp
import base64
import hmac
from os import path
import requests
from datetime import datetime
from time import timezone
from json_minify import json_minify
import json, time
from colorama import Fore
from binascii import hexlify
from hashlib import sha1
from os import urandom
from uuid import uuid4, UUID
import pyfiglet
import asyncio
from hashlib import sha1
import names
import random
import hmac
import platform,socket,re,uuid
import requests_random_user_agent
THIS_FOLDER = path.dirname(path.abspath(__file__)) 
emailfile=path.join(THIS_FOLDER,"accounts.json")
link="http://aminoapps.com/p/i7hyh5"
def dev():
    hw=(names.get_full_name()+str(random.randint(0,10000000))+platform.version()+platform.machine()+names.get_first_name()+socket.gethostbyname(socket.gethostname())+':'.join(re.findall('..', '%012x' % uuid.getnode()))+platform.processor())
    identifier=sha1(hw.encode('utf-8')).digest()
    mac = hmac.new(bytes.fromhex('76b4a156aaccade137b8b1e77b435a81971fbd3e'), b"\x32" + identifier, sha1)
    return (f"32{identifier.hex()}{mac.hexdigest()}").upper()
    
def user_agent():
    s = requests.Session()
    return s.headers['User-Agent']
    
class FromLink:
    def __init__(self, data):
        self.json = data
        self.path = None
        self.objectType = None
        self.shortCode = None
        self.fullPath = None
        self.targetCode = None
        self.objectId = None
        self.shortUrl = None
        self.fullUrl = None
        self.comId = None

    @property
    def FromCode(self):
        try: self.path = self.json["path"]
        except (KeyError, TypeError): pass
        try: self.objectType = self.json["extensions"]["linkInfo"]["objectType"]
        except (KeyError, TypeError): pass
        try: self.shortCode = self.json["extensions"]["linkInfo"]["shortCode"]
        except (KeyError, TypeError): pass
        try: self.fullPath = self.json["extensions"]["linkInfo"]["fullPath"]
        except (KeyError, TypeError): pass
        try: self.targetCode = self.json["extensions"]["linkInfo"]["targetCode"]
        except (KeyError, TypeError): pass
        try: self.objectId = self.json["extensions"]["linkInfo"]["objectId"]
        except (KeyError, TypeError): pass
        try: self.shortUrl = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
        except (KeyError, TypeError): pass
        try: self.fullUrl = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["extensions"]["community"]["ndcId"]
        except (KeyError, TypeError):
            try:
                self.comId = self.json["extensions"]["linkInfo"]["ndcId"]
            except (KeyError, TypeError):
                pass
        try: self.name = self.json["extensions"]["community"]["name"]
        except (KeyError, TypeError): pass
        return self
class Account():
    def __init__(self, accountline, session, link=None):
        self.authenticated = False
        self.session = session
        self.link = link
        self.email = accountline["email"]
        self.password = accountline["password"]
        self.device_id= accountline["device"]
        self.tapjoy_headers = {
            'cookies': '__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096',
            'authorization': 'Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA==',
            'X-Tapdaq-SDK-Version': 'android-sdk_7.1.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9 Pro Build/QQ3A.200805.001; com.narvii.amino.master/3.4.33585)'
        }
        self.sid = None
        self.uid = None
        self.api = 'https://service.narvii.com/api/v1'
        self.apip = 'https://aminoapps.com/api-p'
    async def from_link(self, link):
        async with self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.generate_headers()) as response:
            response = await response.json()
            if response["api:statuscode"] == 0:
                pass
            else:
                raise Exception(response['api:message'])
            return FromLink(response["linkInfoV2"]).FromCode
    def generate_headers(self, data=None, content_type=None, sig=None):
        headers = {
            'NDCDEVICEID': dev(),
            'Accept-Language': 'en-US',
            'Content-Type': 'text/html',
            'User-Agent': user_agent(),
            'Host': 'service.narvii.com',
            'Accept-Encoding': 'gzip',
            'Connection': 'Keep-Alive'
        }
        #print(headers)
        if data:
            headers['Content-Length'] = str(len(data))
            if sig:
                headers['NDC-MSG-SIG'] = sig
        if self.sid:
            headers['NDCAUTH'] = f'sid={self.sid}'
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def generate_tapjoy_data(self):
        data = {
            'reward': {
                'ad_unit_id': 't00_tapjoy_android_master_checkinwallet_rewardedvideo_322',
                'credentials_type': 'publisher',
                'custom_json': {
                    'hashed_user_id': self.uid
                },
                'demand_type': 'sdk_bidding',
                'event_id': str(uuid4()),
                'network': 'tapjoy',
                'placement_tag': 'default',
                'reward_name': 'Amino Coin',
                'reward_valid': True,
                'reward_value': 2,
                'shared_id': '4d7cc3d9-8c8a-4036-965c-60c091e90e7b',
                'version_id': '1569147951493',
                'waterfall_id': '4d7cc3d9-8c8a-4036-965c-60c091e90e7b'
            },
            'app': {
                'bundle_id': 'com.narvii.amino.master',
                'current_orientation': 'portrait',
                'release_version': '3.4.33585',
                'user_agent': 'Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)'
            },
            'device_user': {
                'country': 'US',
                'device': {
                    'architecture': 'aarch64',
                    'carrier': {
                        'country_code': 255,
                        'name': 'Vodafone',
                        'network_code': 0
                    },
                    'is_phone': True,
                    'model': 'GT-S5360',
                    'model_type': 'Samsung',
                    'operating_system': 'android',
                    'operating_system_version': '29',
                    'screen_size': {
                        'height': 2300,
                        'resolution': 2.625,
                        'width': 1080
                    }
                },
                'do_not_track': False,
                'idfa': '0c26b7c3-4801-4815-a155-50e0e6c27eeb',
                'ip_address': '',
                'locale': 'ru',
                "timezone": {
                    'location': 'Asia\/Seoul',
                    'offset': 'GMT+02:0'
                },
                'volume_enabled': True
            },
            'session_id': '7fe1956a-6184-4b59-8682-04ff31e24bc0',
            'date_created': 1633283996
        }
        return data

    async def sig(self, data):
        signature = base64.b64encode(bytes.fromhex("32") + hmac.new(bytes.fromhex("fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2"), data.encode("utf-8"), sha1).digest()).decode("utf-8")
        return signature

    async def login(self):
        try:
            data = json.dumps({
                'email': self.email,
                'v': 2,
                'secret': f'0 {self.password}',
                'deviceID': self.device_id,
                'clientType': 100,
                'action': 'normal',
                'timestamp': int(time.time() * 1000)
            })
            async with self.session.post(f'{self.api}/g/s/auth/login', headers=self.generate_headers(data=data, sig=await self.sig(data)),
                                        data=data) as response:
                response = await response.json()
                #print(response)
                if response["api:statuscode"] == 0:
                    pass
                else:
                    #print(response)
                    raise Exception(response['api:message'])
                self.sid = response["sid"]
                self.uid = response["account"]["uid"]
                self.authenticated = True
        except:
            pass

    async def tapjoy_farm(self):
        await asyncio.gather(*[asyncio.create_task(
            self.session.post('https://ads.tapdaq.com/v4/analytics/reward', headers=self.tapjoy_headers,
                              json=self.generate_tapjoy_data())) for _ in range(400)])

    async def join_community(self, target):
        async with self.session.post(f'{self.api}/x{target}/s/community/join', headers=self.generate_headers()) as response:
            response = await response.json()
            if response["api:statuscode"] == 0:
                pass
            else:
                raise Exception(response['api:message'])

    async def join_(self, target):
        async with self.session.post(f'{self.api}/x{target.comId}/s/community/join', headers=self.generate_headers()) as response:
            response = await response.json()
            if response["api:statuscode"] == 0:
                pass
            else:
                raise Exception(response['api:message'])
    async def ran(self, search:str,start: int = 0, size: int = 25):
        async with self.session.get(f"https://service.narvii.com/api/v1/g/s/community/search?q={search}&language=en&completeKeyword=1&start={start}&size={size}",headers=self.generate_headers()) as response:
          response = await response.json()
          if response["api:statuscode"] == 0:
              com=[]
              r=response["communityList"]
              for listt in r:
                  com.append(listt["ndcId"])
              #print(com)
              return com
          else:
              return response.json()

    async def send_my_coins(self, target):
        async with self.session.get(f'{self.api}/g/s/wallet', headers=self.generate_headers()) as response:
            response = await response.json()
            if response["api:statuscode"] == 0:
                pass
            else:
                raise Exception(response['api:message'])
            coins = int(response['wallet']['totalCoins'])
            if not coins:
                return coins
            data = json.dumps(
                {'coins': coins % 500,
                 'tippingContext': {"transactionId": str(UUID(hexlify(urandom(16)).decode('ascii')))},
                 'timestamp': int(time.time() * 1000)})
            async with self.session.post(f'{self.api}/x{target.comId}/s/blog/{target.objectId}/tipping',
                                         headers=self.generate_headers(data=data, sig=await self.sig(data)),
                                         data=data) as response:
                response = await response.json()
                if response["api:statuscode"] == 0:
                    pass
                else:
                    raise Exception(response['api:message'])
            for _ in range(coins // 500):
                data = json.dumps(
                    {'coins': 500,
                     'tippingContext': {"transactionId": str(UUID(hexlify(urandom(16)).decode('ascii')))},
                     'timestamp': int(time.time() * 1000)})
                async with self.session.post(f'{self.api}/x{target.comId}/s/blog/{target.objectId}/tipping',
                                             headers=self.generate_headers(data=data, sig=await self.sig(data)),
                                             data=data) as response:
                    response = await response.json()
                    if response["api:statuscode"] == 0:
                        pass
                    else:
                        raise Exception(response['api:message'])
            return coins
    async def part_of_sobj_farm(self, target):
        data = {
            'userActiveTimeChunkList': [{'start': int(datetime.timestamp(datetime.now())),
                                         'end': int(datetime.timestamp(datetime.now())) + 300} for _ in range(12)],
            'timestamp': int(time.time() * 1000),
            'optInAdsFlags': 2147483647,
            'timezone': int(-timezone // 1000)
        }
        data = json_minify(json.dumps(data))
        #print(data)
        async with self.session.post(f'{self.api}/x{target}/s/community/stats/user-active-time',
                                headers=self.generate_headers(data=data, sig=await self.sig(data)), data=data) as response:
                                response = await response.json()
                                print(response["api:message"])

    async def send_active_farm(self, target, requests=25):
                tasks = []
                for _ in range(requests):
                	tasks.append(asyncio.create_task(self.part_of_sobj_farm(target=target)))
                await asyncio.gather(*tasks)


async def farm(accountline, target, session):
    try:
        account = Account(accountline=accountline, session=session)
        now = time.time()
        await account.login()
        print(f'{account.email}')
        await account.tapjoy_farm()
        await account.join_(target)
        ra1=random.randint(0,5)
        r1=["anime","sorts","sports","adventure","study","money"]
        search=r1[ra1]
        ra2=random.randint(0,20)
        tarr=await account.ran(search)
        tar=tarr[ra2]
        #print(tar)
        await account.join_community(target=tar)
        await account.send_active_farm(target=tar)
        timer = time.time()-now

        timer = float('{:.3f}'.format(timer))
        
        print(f'- {await account.send_my_coins(target=target)}coins > {timer} sec')
    except Exception as g:
      #print(g)
      pass

async def main():
    i=0
    with open(emailfile) as f: 
        accountlines = json.load(f) 
    
    async with aiohttp.ClientSession() as session:
        seeker = Account(accountlines[i], session)
        await seeker.login()
        target = await seeker.from_link(link=link)
        i+=1
        while True:
            for accountline in accountlines:
              await farm(accountline=accountline, session=session, target=target)
# asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_until_complete(main())