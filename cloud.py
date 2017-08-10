# coding: utf-8

from leancloud import Engine
from leancloud import Object
from leancloud import LeanEngineError
import time
import requests
from app import app

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

engine = Engine(app)
    
@engine.define
def sign():
    time1 = time.time()
    
    for i in range(1,7000):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            login(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(9000,9301):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            login(user,'111111')
        except Exception as e:
            print(user,e)
    
    print(time1,time.time())

@engine.define
def signTemp5000():
    time1 = time.time()
    
    for i in range(5000,6000):
        
        user = 'sy%s' % str(i).zfill(4)
#        print(user,'#'*20,time.time())
        try:
            login(user,'111111')
        except Exception as e:
            print(user,e)
    
    print(time1,time.time())
    
#error_log
def saveErrorLog(user,msg):

    Balance = Object.extend('ErrorLog')
    balance = Balance()
    balance.set('msg',msg)
    balance.set('user',user)
    balance.save()
    
#error_log
def saveZhongJiang(user,msg):

    Balance = Object.extend('ZhongJiang')
    balance = Balance()
    balance.set('msg',msg)
    balance.set('user',user)
    balance.save()    
    
def login(user,password):
    re = requests.Session()

    headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'Content-Length':'59',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'passport.ccoop.cn',
        'Origin':'http://passport.ccoop.cn',
        'Proxy-Connection':'keep-alive',
        'Referer':'http://passport.ccoop.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
    
    login_url = 'http://passport.ccoop.cn/account/login'
    data = {'username':user,
        'password':password,
        'returnurl':'',
        'rememberMe':'false',
        }
    html = re.post(login_url,data=data,headers = headers)
    cookies = requests.utils.dict_from_cookiejar(re.cookies)
#    print(cookies)
    cook = ''
    for key,values  in cookies.items():
        cook += ('%s=%s;' % (key,values))
#    print(cook)
    if html.json()['uid'] == 0 :
        saveErrorLog(user,html.json())
        return

    #sign
    headers_sign = {'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'Content-Length':'44',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'chaoshi.ccoop.cn',
        'Cookie':cook,
        'Origin':'http://chaoshi.ccoop.cn',
        'Proxy-Connection':'keep-alive',
        'Referer':'http://chaoshi.ccoop.cn/SignIn/Sign',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
    
    login_sign = 'http://chaoshi.ccoop.cn/SignIn/AddSignInRecord'
    data_sign = {'prizeActId':'794',
        'couponActId':'796',
        'signInCount':'1'}
    html = requests.post(login_sign,data=data_sign,headers = headers_sign,timeout=4)
    print(user,html.json(),time.time())    
#    time.sleep(0.1)
    
    #Prize
    url_prize = 'http://chaoshi.ccoop.cn/Prize/Prizing'
    headers_prize = {'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'Content-Length':'26',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'chaoshi.ccoop.cn',
#        'Cookie':'gr_user_id=54f2b428-84f2-46fb-bf6b-ec6ff0dae68e; Hm_lvt_d1335608ddcd24dc0e0e31c11dcc343f=1502326243; Hm_lpvt_d1335608ddcd24dc0e0e31c11dcc343f=1502329108; zhtxcszhxy=0A2k/Jjrvmd24m0/MoxDWElU9oD5Wx17l2r39iYt3J6gQJS95OnQsSrK0IOKXrzUY7tzHXKjO3sWhVpgRObBFQ==; zhtxnewcs=V6MoBimXqy2mf5/MuLfa1iwb5vTWUEuMMAAbMSFMJFD312efysYG5b8pe7dhgOM4bQRSkWpeK+AtdgD7XY4+yQ==; zhtxgosproject=lMJowmXT6GcF9AfBKJZCfDlQkYH8GeA44Ih8MJBc5bO0YQ1EyJQyihdMFOHVL5t3zGACr5XLIVZgHIY5EAfCKmjBQTgYuFO0oshZyb6mq31x0eyG31yr3eOzN9%2bLG25Z66Kb6%2bMdGqKVAHyIO5R7RZn3qylFRlT0KXIW3Vo8vPTWYPYdhIClCmD45ENlfLEgQsMq7v%2bGBACRVa4mM3LoRJ2t12rjqFi14%2fS8jj%2btdYjzDNmXix3kAbKI9eh3AvphcmNu63JC6CztVt0SUSop%2b3sURtWcUlIKmDH6D9B4KcgTsuyoU4nbPw1ZR1m3TDsptnS%2fKTA4ryazxS1vvkhzqQso6Qby1VqifyU1qbtC67MnVhclD9qBEXzTOLcE%2fRUMTeY8ZSujNrqrujC6QBtFmga1sg2Bwo%2blweoaHwAZ4F87LsuGM%2f3FKVbM6V0fJoVcVd4YimsC5CrvRUq5MYV3LYGenKgCFE2bPpgADGgW4GKSR7VQMGuExvOcYaog3E86u%2feu%2fbHYejeS4ibbd3N9xI6O%2fzUBCllckZl3VCADriTn1wL6UTSc0v53L2cGmGWc4VUPuJYtmS0380Pc6dk1ub%2fsNfot4XSJgrlaEVh4YmtpK%2b0JMStvMJEinl25U6AwFVS70Sm3l7sDC7b%2bQ10I7bf61zHh%2bP90kcVOjzGsssOrhN3sSOKsv6452CbnXk1Oa%2f20pHjOROEPjruj06%2bNfhPliiH05HejpPjST91X7HmGUoJEEA8AlodspEtxfIt1vQCxMlRLxBcrIoGUA1FdI%2b0dZVjjFcJKXYg4DDqu%2f7AW0ALYWIG4yNL96ifeMGDcUv0W%2fM98euOVo46HYwsFNWGW37tnAt1DVbEWXodmCePlwqZQE%2br0nzXRrShleTletD445PLWDhDltzjKOc%2b4OYaCl6Mo8K6ACPrHHb%2bzmGQ1DFwX462aNvAFKFJYcN4Uwxm%2bjQ%3d%3d; zhtxcslogintime=hcM0oyCY71Y%3d; IsFirstLoad=zQ%3d%3d; gr_session_id_96df24f07db1c09e=b416ee3d-b73d-496b-9dbf-d5ba3ecec6b6',
        'Cookie':cook,
        'Origin':'http://chaoshi.ccoop.cn',
        'Proxy-Connection':'keep-alive',
        'Referer':'http://chaoshi.ccoop.cn/_818room/index?type=3',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
    
    data_prize = {'prizeType':'0',
        'prizePattern':'3'}

    html = requests.post(url_prize,data=data_prize,headers = headers_prize,timeout=3)

    if (html.json()['result']>0):
        #中奖了
        print(html.json()['result'],'*'*50)
        saveZhongJiang(user,html.json())
        
if __name__ == '__mian__':

    pass