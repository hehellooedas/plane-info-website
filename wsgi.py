import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from flask import Flask, render_template, request, flash, url_for, redirect, make_response, session, Response, g,jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_script import Manager
from flask_seasurf import SeaSurf
from markupsafe import escape
from flask_login import LoginManager, UserMixin, login_required
import os, random, sys, click, threading, Function
from PIL import Image

app = Flask(__name__)
csrf = SeaSurf(app)
# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'main'
os.environ['FLASK_ENV'] = 'development'
app.config['WTF_I18N_ENABLED'] = False
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov']
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 最大上传200MB的文件
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', Function.create_string(16))
Thread_Pool = ThreadPoolExecutor()

# 邮件smtp相关配置
manager = Manager(app)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.qq.com',  # 用于发送邮件的SMTP服务
    MAIL_PORT=465,  # 发信端口
    MAIL_USE_SSL=True,  # 是否使用SSL
    MAIL_USERNAME='928309386@qq.com',  # 发信服务器的用户名
    MAIL_PASSWORD='zzdhxdgourtabdgb',  # 发信服务器的密码
    MAIL_DEFAULT_SENDER=('April Zhao', '928309386@qq.com')  # 默认的发信人
))
mail = Mail(app)


# 邮件发送函数
def send_email(app, emails, subject='EmailTest', content=u'这是一条从民航行程推荐网站发来的邮件(收到请勿回复!)'):
    with app.app_context():
        msg = Message(
            subject=subject,
            sender="928309386@qq.com",
            recipients=emails
        )
        msg.body = content + '\n收到请勿回复！若您从未注册民航推荐网，请无视这封邮件，注意不要泄露个人信息！'
        mail.send(msg)
        return True


def register(email, password):
    pass




@app.route('/login', methods=['GET', 'POST'])
def login():
    response = make_response(render_template('login.html'))
    return response

@app.route('/login_ajax',methods=['GET','POST'])
def login_ajax():
    email = escape(request.get_json().get('email'))
    Verification_status = request.get_json().get('status')
    Verification_Code = Function.create_string()
    if email and Verification_status:
        if Function.exist_account(email):
            session['login_status'] = True
            session['user_id'] = email
            session.permanent = True
        else:
            flash(u'您的账户并未注册，请检查邮件是否填写正确！')
    else:
        content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
        Thread_Pool.submit(send_email, args=(app, email, '民航推荐网站注册',content))
        return jsonify(Verification_Code=Verification_Code)

app.route('/logout')
def logout():
    if 'login_status' in session:
        session.pop('login_status')
        g.login_status = False
        g.user_id = None
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    response = make_response(render_template('register.html'))
    return response


# index函数为航班推荐主页面
@app.route('/', methods=['GET', 'POST'])
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
