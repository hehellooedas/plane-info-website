from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from flask import Flask, render_template, request, url_for, redirect, make_response, session, g, jsonify,abort
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_seasurf import SeaSurf
from flask_apscheduler import APScheduler
from flask_avatars import Avatars
from user_agents import parse
from markupsafe import escape
from flask_caching import Cache
import os, threading, Function,asyncio,json,datetime,time



app = Flask(__name__)
csrf = SeaSurf(app)
# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'wsgi'
os.environ['FLASK_ENV'] = 'development'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', Function.create_string(16))
avatars = Avatars(app)
cache = Cache(app,config={'CACHE_TYPE':'simple'})
Thread_Pool = ThreadPoolExecutor()


# 邮件smtp相关配置
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

emails_db = Function.emails_db()


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



@app.errorhandler(404)
def encounter_404(error):
    return render_template('error.html',error=error)

@app.errorhandler(403)
def encounter_403(error):
    return f'<h3>很抱歉，您被识别为爬虫程序，如检测错误，请刷新浏览器，很抱歉给您带来了不便,请您谅解！<br>{error}</h3>'

@app.template_filter
def judge_Systen():
    return request.cookies.get('system') == 'phone'


@app.get('/login')
@cache.cached(timeout=300,query_string=True)
def login():
    response = make_response(render_template('login.html'))
    agent = parse(request.user_agent.string)
    if agent.is_bot:
        abort(403)
    elif agent.is_mobile:
        response.set_cookie(key='system',value='phone')
    else:
        response.set_cookie(key='system', value='pc')
    if 'login_status' in session and 'email' in session:
        session.pop('login_status')
        session.pop('email')
    return response


@csrf.exempt
@app.route('/login_ajax1', methods=['GET', 'POST'])
def login_ajax():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        Verification_Code = Function.create_string()
        if email and emails_db.exist_account(email):
            content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
            t = threading.Thread(target=send_email, args=(app, [email], '民航推荐网站登录', content))
            t.start()
            string = u'邮件已发送，请注意查收！'
        else:
            string = u'您的账户并未注册，请检查邮件是否填写正确！'
        dic = {
            'Code': Verification_Code,
            'string': string
        }
        return jsonify(dic)


@csrf.exempt
@app.route('/login_ajax2', methods=['GET', 'POST'])
def login_ajax2():
    if request.method == 'POST':
        email = request.form.get('email')
        session['login_status'] = True
        session['email'] = email
        session.permanent = True
        cache.clear()
        return url_for('index')




@csrf.exempt
@app.get('/register')
@cache.cached(timeout=300,query_string=True)
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
                t = threading.Thread(target=send_email, args=(app, [email], '民航推荐网站注册', content))
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
        cache.clear()
        return url_for('login')


# index函数为航班推荐主页面
@app.get('/')
def index():
    email = session.get("email")
    login_status = session.get('login_status')
    if login_status and email:
        return render_template('index.html', email=email,exit_url=request.host_url+url_for('login'))
    else:
        return redirect(url_for('login'))


@csrf.exempt
@app.route('/index_ajax1', methods=['GET', 'POST'])
def index_ajax1():
    if request.method == 'POST':
        acity = request.form.get('acity')
        bcity = request.form.get('bcity')
        date = request.form.get('date')
        plane_db = Function.planes_db(acity)
        a = Process_Pool.submit(plane_db.select_planes,(bcity,date))
        return json.dumps(a.result())


@csrf.exempt
@app.route('/index_ajax2', methods=['GET', 'POST'])
def index_ajax2():
    if request.method == 'POST':
        index = request.form.get('index')#索引
        acity = request.form.get('acity')#出发城市
        adate = request.form.get('daate')#到达城市
        bcity = request.form.get('bcity')#出发日期
        bdate = request.form.get('bdate')#到达日期
        cabin = request.form.get('cabin')#舱室选择
        company = request.form.get('company')#航空公司
        flight_number = request.form.get('flight_number')#航班号
        numbers = request.form.get('numbers')#几个人
        emails = json.loads(request.form.get('emails'))#每个人的邮箱地址
        g.index = index
        g.acity = acity
        g.bcity = bcity
        g.adate = adate
        g.bdate = bdate
        g.numbers = numbers
        g.emails = emails
        g.company = company
        g.flight_number = flight_number
        g.cabin = cabin
        return redirect(url_for('settlement'))




@app.get('/settlement')
def settlement():
    email = session.get("email")
    login_status = session.get('login_status')
    settlement = session.get('settlement')
    if email and login_status and settlement:
        return render_template('settlement.html')
    elif email and login_status:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@csrf.exempt
@app.route('/settlement_ajax', methods=['GET', 'POST'])
def settlement_ajax():
    if request.method == 'POST':
        index = g.get('index')
        acity = g.get('acity')
        bcity = g.get('bcity')
        adate = g.get('adate')
        bdate = g.get('bdate')
        company = g.get('company')
        cabin = g.get('cabin')
        flight_number = g.get('flight_number')
        numbers = g.get('numbers')
        emails = g.get('emails')
        Function.set_task([index,acity,numbers])
        t = threading.Thread(target=Function.set_task,args=([acity,index,numbers],))
        t.start()
        content = f'【民航行程信息】您的机票已于{Function.get_Time()}支付成功。{Function.get_date(adate)} {company} {flight_number}航班' \
                  f'{cabin},{acity}（{Function.get_Szm(acity)}） {Function.get_time(adate)} - {bcity}（{Function.get_Szm(bcity)}）' \
                  f'{Function.get_time(bdate)}。\n航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续' \
                  f'并提前20分钟抵达登机口。乘机人'
        more = f'。详细信息请访问{request.host_url}'
        if len(emails) == 1:
            t = threading.Thread(target=send_email,args=(app,emails,'购票通知',content+emails[0]+more))
            t.start()
        else:
            tasks = [
                (app,[email],'购票信息',content+email+more)
                for email in emails
            ]
            with ThreadPoolExecutor() as pool:
                pool.map(send_email,tasks)
        return redirect(url_for('success'))


@app.get('/success')
def success():
    return render_template('success.html')


def planes_update(Func,time=6):
    scheduler = APScheduler()
    scheduler.init_app(app)
    #定时任务的格式
    scheduler.add_job(func=Func, trigger='interval', hours=time, id='planes_update')
    scheduler.start()
planes_update(Function.planes_Update_Function,4)


if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor(max_workers=5)
    print('服务器开始运行')
    app.run(debug=False, port=80, host='0.0.0.0')
    print('服务器关闭')
