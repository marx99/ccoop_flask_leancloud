from flask import render_template
from flask import Flask
from flask import request
from ccoop_lean import Fanpai,getAccount

app = Flask(__name__)
#app.config.update(
#    PREFERRED_URL_SCHEME='https'
#)

@app.route('/')
def hello(name=None):
    
    return render_template('hello.html')

@app.route('/fanpai',methods=['POST'])
def fanpai():
    try:
        num = request.form['num']
        print(num)
        list_user = getAccount(int(num))
        return list_user
    except Exception as e:
        print(e)        
        return e
    
#    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)

