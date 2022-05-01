from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from flask import Flask, render_template, request, url_for, redirect, make_response, session, Response, g,jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_script import Manager
from flask_seasurf import SeaSurf
from markupsafe import escape
import os,click,threading,multiprocessing,Function


app = Flask(__name__)
csrf = SeaSurf(app)
# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'wsgi'
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
    DEBUG=False,
    MAIL_SERVER='smtp.qq.com',  # 用于发送邮件的SMTP服务
    MAIL_PORT=465,  # 发信端口
    MAIL_USE_SSL=True,  # 是否使用SSL
    MAIL_USERNAME='928309386@qq.com',  # 发信服务器的用户名
    MAIL_PASSWORD='uhnufypshcmhbejf',  # 发信服务器的密码
    MAIL_DEFAULT_SENDER=('April Zhao', '928309386@qq.com')  # 默认的发信人
))
mail = Mail(app)

emails_db = Function.emails_db('./files/emails.pickle')
planes_db = Function.planes_db('./files/planes.pickle')

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





@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@csrf.exempt
@app.route('/login_ajax1',methods=['GET','POST'])
def login_ajax():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        Verification_Code = Function.create_string()
        if email and emails_db.exist_account(email):
            content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
            #send_email(app, [email], '民航推荐网站登录', content)
            t = threading.Thread(target=send_email,args=(app, [email], '民航推荐网站登录', content))
            t.start()
            string = u'邮件已发送，请注意查收！'
        else:
            string = u'您的账户并未注册，请检查邮件是否填写正确！'
        dic = {
        'Code':Verification_Code,
        'string':string
        }
        return jsonify(dic)
        #t = threading.Thread(target=send_email,args=(app, [email], '民航推荐网站登录', content))
        #t.start()


@csrf.exempt
@app.route('/login_ajax2',methods=['GET','POST'])
def login_ajax2():
    if request.method == 'POST':
        email = request.form.get('email')
        session['login_status'] = True
        session['email'] = email
        g.login_status = True
        g.email = email
        session.permanent = True
        return url_for('index')



app.route('/logout')
def logout():
    if 'login_status' in session:
        session.pop('login_status')
        session.pop('email')
        g.login_status = False
        g.email = None
    return redirect(url_for('login'))




@csrf.exempt
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@csrf.exempt
@app.route('/register_ajax1', methods=['GET', 'POST'])
def register_ajax1():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        Verification_Code = Function.create_string()
        string = 'hello'
        if email:
            if emails_db.exist_account(email):
                string = u'您的账户已经注册，请检查邮件是否填写正确！'
            else:
                content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
                t = threading.Thread(target=send_email,args=(app, [email], '民航推荐网站注册', content))
                t.start()
                string = u'邮件已发送，请注意查收！'
        dic = {
            'Code': Verification_Code,
            'string': string
        }
        return jsonify(dic)

@csrf.exempt
@app.route('/register_ajax2', methods=['GET', 'POST'])
def register_ajax2():
    if request.method == 'POST':
        email = request.form.get('email')
        emails_db.add_account(email)
        return url_for('login')




# index函数为航班推荐主页面
@app.route('/', methods=['GET', 'POST'])
def index():
    email = session.get("email")
    login_status = session.get('login_status')
    if login_status and email:
        g.login_status = True
        g.user_id = email
        response = make_response(render_template('index.html'))
        return response
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor()
    print('服务器开始运行')
    app.run(debug=True, port=80, host='127.0.0.1')
    print('服务器关闭')
