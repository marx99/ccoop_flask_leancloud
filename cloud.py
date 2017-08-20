# coding: utf-8

from leancloud import Engine
from leancloud import Object
from leancloud import LeanEngineError
import time
import requests
import cont
from app import app
from send_mail import send_mail
import threading
from ccoop_lean import Fanpai,qiangquan,getAccount

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

engine = Engine(app)
    
@engine.define
def sign():
    time1 = time.time()
    
    qiandaoOkNum = 0
    for i in range(1,7031):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            qiandaoOkNum += login(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(9000,9301):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            qiandaoOkNum += login(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(9001,9016):
        
        user = 's%s' % str(i).zfill(4)

        try:
            qiandaoOkNum += login(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(1190,2191):
        
        user = 'syj%s' % str(i).zfill(4)

        try:
            qiandaoOkNum += login(user,'000999')
        except Exception as e:
            print(user,e)

    #真实超市
    for i in cont.chaoshi:
        try:
            qiandaoOkNum += login(i,'123123')
        except Exception as e:
            print(i,e)
            
    print('OK num :%s' % qiandaoOkNum,round(time.time()-time1),3)
    send_mail('OK:%s,time:%s' % (qiandaoOkNum,time.time()-time1),str(qiandaoOkNum))
    
@engine.define
def qianquan_ap():
    for i in range(1,100):
        
        user = 'sy%s' % str(i).zfill(4)
#        print(user,'#'*20,time.time())
        try:
            qiangquan(user,'111111')
        except Exception as e:
            print(user,e)
            
@engine.define
def huanxingLean():
    print ('huanxingLean',time.time())

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
        return 0

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
    
    qiandaoOkNum = 0
    if '签到成功' in html.json()['msg']:
        qiandaoOkNum += 1
    else:    
        print(user,html.json(),time.time())    
    time.sleep(0.05)
    
    return qiandaoOkNum
     
@engine.define
def testT():
    #多线程抢券
    for i in range(10):
        t =threading.Thread(target=Tqian,args=(i,))
        t.start()
        
def Tqian(i):

    for k in range(i*100+1,i*100+70):
        
        user = 'sy%s' % str(k).zfill(4)
        try:
            qiangquan(user,'111111')
            pass
        except Exception as e:
            print(user,e)

@engine.define
def fanpai():

    for i in range(600,7031):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            Fanpai(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(9000,9301):
        
        user = 'sy%s' % str(i).zfill(4)

        try:
            Fanpai(user,'111111')
        except Exception as e:
            print(user,e)
            
    for i in range(1190,2191):
        
        user = 'syj%s' % str(i).zfill(4)

        try:
            Fanpai(user,'000999')
        except Exception as e:
            print(user,e)

    #真实超市
    for i in cont.chaoshi:
        try:
            Fanpai(i,'123123')
        except Exception as e:
            print(i,e)

@engine.define
def getAccountTest():
    print(getAccount(3))
    return getAccount(3)
    
if __name__ == '__mian__':

    qiangquan('sy0001','111111')

#    testT()