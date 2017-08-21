from flask import render_template
from flask import Flask
from flask import request
from ccoop_lean import Fanpai,getAccount,updateAccount,getAccountCount

app = Flask(__name__)
#app.config.update(
#    PREFERRED_URL_SCHEME='https'
#)

@app.route('/')
def hello(name=None):
    
    return render_template('hello.html',count=getAccountCount())

@app.route('/fanpai/',methods=['POST'])
def fanpai():
    try:
        num = request.form['num']

        list_user = getAccount(int(num))
#        print(int(num),list_user)
        #成功个数
        numOK = 0
        for user in list_user:
            objectId = user[0]
            userId = user[1]
            password = user[2]
            try:
                #抢券 100元
                numOK += Fanpai(userId,password)
                #抢券之后标记
                updateAccount(objectId)
            except:
                pass
            
        countStr = '未抢券账户数 ：%s' % getAccountCount()
        okStr = '本次处理 %s 个账号,抽中 %s 个券' % (len(list_user),numOK)
        return str({"count":countStr,"ok":okStr})
        
    except Exception as e:
        print(e)        
        return e
    
#    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)

