from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from flask import Flask, render_template, request, flash, url_for, redirect,make_response,session,Response,g
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_script import Manager
from flask_login import LoginManager,UserMixin,login_required
from flask_wtf import FlaskForm
from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField,IntegerRangeField
from wtforms.validators import DataRequired,Length,email_validator,email,Email
from flask_wtf.file import FileField,FileRequired,FileAllowed
import os, random, sys,click,pandas,pickle,threading
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'main'
os.environ['FLASK_ENV'] = 'development'
app.config['WTF_I18N_ENABLED'] = False
app.config['ALLOWED_EXTENSIONS'] = ['png','jpg','jpeg','mp4','avi','mov']
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024 #最大上传200MB的文件
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', 'hello world')
Thread_Pool = ThreadPoolExecutor()


# 邮件smtp相关配置
manager = Manager(app)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.qq.com',#用于发送邮件的SMTP服务
    MAIL_PORT=465,#发信端口
    MAIL_USE_SSL=True,#是否使用SSL
    MAIL_USERNAME='928309386@qq.com',#发信服务器的用户名
    MAIL_PASSWORD='zzdhxdgourtabdgb',#发信服务器的密码
    MAIL_DEFAULT_SENDER=('April Zhao', '928309386@qq.com')#默认的发信人
))
mail = Mail(app)
# 邮件发送函数
def send_email(user_email, content=u'这是一条从民航行程推荐网站发来的邮件'):
    respect = [user_email]
    msg = Message('EmailTest', sender="928309386@qq.com", recipients=respect)
    msg.body = content
    mail.send(msg)


@app.before_first_request
def login_primary_verification():
    pass

@app.route('/login',methods=['GET','POST'])
def login():
    response = make_response(render_template('login'))
    if request.method == 'POST':
        pass
        session.permanent = True
    return response

@app.route('/register',methods=['GET','POST'])
def register():
    return 'register'

# index函数为航班推荐主页面
@app.route('/',methods=['GET','POST'])
def index():
    user_id = session.get("user_id")
    login_status = session.get('login_status')
    if login_status and user_id:
        g.login_status = True
        g.user_id = user_id
        response = make_response(render_template('index.html'))
        return response
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor()
    print('服务器开始运行')
    app.run(debug=True, port=80, host='127.0.0.1')
    print('服务器关闭')