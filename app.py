from flask import render_template
from flask import Flask
from flask import request

app = Flask(__name__)
app.config.update(
    PREFERRED_URL_SCHEME='https'
)

@app.route('/')
def hello(name=None):
    
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)

