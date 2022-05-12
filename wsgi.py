from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from flask import Flask, render_template, request, url_for, redirect, make_response, session, g, jsonify, abort
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_seasurf import SeaSurf
from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask_avatars import Avatars
from user_agents import parse
from markupsafe import escape
from flask_caching import Cache
from logging.handlers import TimedRotatingFileHandler
import os, threading,logging,Function


#日志处理
logging.basicConfig()
file_log_handler = TimedRotatingFileHandler(filename='./files/logs/flask.log',encoding='UTF-8',delay=True,backupCount=10,interval=4,when='D')
file_log_handler.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
file_log_handler.setLevel(logging.WARNING)
logging.getLogger().addHandler(file_log_handler)


app = Flask(__name__)
csrf = SeaSurf(app)#csrf防护
scheduler = APScheduler()#定时任务
scheduler.init_app(app)
scheduler.api_enabled = True
interval = IntervalTrigger(
    hours=6,  # 六小时更新一次数据库
    start_date='2022-4-29 08:00:00',
    end_date='2023-5-31 08:00:00',
    timezone='Asia/Shanghai'
)


# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'wsgi'
os.environ['FLASK_ENV'] = 'production'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', Function.create_String(16))
avatars = Avatars(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
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
def send_email(app, emails, subject='EmailTest', content=u'这是一条从民航行程推荐网站发来的邮件(收到请勿回复!)', html=None):
    with app.app_context():
        msg = Message(
            subject=subject,
            sender="928309386@qq.com",
            recipients=emails
        )
        msg.body = content + '\n收到请勿回复！若您从未注册民航推荐网，请无视这封邮件，注意不要泄露个人信息！'
        msg.html = html
        mail.send(msg)
        return True


@app.errorhandler(404)
def encounter_404(error):
    return render_template('error.html')


@app.errorhandler(403)
def encounter_403(error):
    return f'<h3>很抱歉，您被识别为爬虫程序，如检测错误，请刷新浏览器，很抱歉给您带来了不便,请您谅解！<br></br>{error}</h3>'


@app.template_filter
def judge_Systen():
    return request.cookies.get('system') == 'phone'


@app.get('/login')
@cache.cached(timeout=300, query_string=True)
def login():
    response = make_response(render_template('login.html'))
    agent = parse(request.user_agent.string)
    if agent.is_bot:
        abort(403)
    elif agent.is_mobile:
        response.set_cookie(key='system', value='phone')
    else:
        response.set_cookie(key='system', value='pc')
    if 'login_status' in session and 'email' in session:
        session.pop('login_status')
        session.pop('email')
    return response


@csrf.exempt
@app.route('/login_ajax1',methods=['GET','POST'])
def login_ajax():
    email = escape(request.form.get('email'))
    Verification_Code = Function.create_String()
    if email and emails_db.exist_account(email):
        content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
        t = threading.Thread(target=send_email, args=(app, [email], '民航推荐网站登录', content),name='login_thread')
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
@app.post('/login_ajax2')
def login_ajax2():
    email = request.form.get('email')
    session['login_status'] = True
    session['email'] = email
    session.permanent = True
    cache.clear()
    return url_for('index')


@csrf.exempt
@app.get('/register')
@cache.cached(timeout=300, query_string=True)
def register():
    return render_template('register.html')


@csrf.exempt
@app.post('/register_ajax1')
def register_ajax1():
    email = escape(request.form.get('email'))
    Verification_Code = Function.create_String()
    string = 'hello'
    if email:
        if emails_db.exist_account(email):
            string = u'您的账户已经注册，请检查邮件是否填写正确！'
        else:
            content = f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
            t = threading.Thread(target=send_email, args=(app, [email], '民航推荐网站注册', content),name='register_thread')
            t.start()
            string = u'邮件已发送，请注意查收！'
    dic = {
        'Code': Verification_Code,
        'string': string
    }
    return jsonify(dic)


@csrf.exempt
@app.post('/register_ajax2')
def register_ajax2():
    email = request.form.get('email')
    emails_db.add_account(email)
    cache.clear()
    return url_for('login')


# index函数为航班推荐主页面
@csrf.exempt
@app.get('/')
def index():
    email = session.get("email")
    login_status = session.get('login_status')
    if login_status and email:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@csrf.exempt
@app.post('/index_ajax1')  # 单程
def index_ajax1():
    form = request.form
    acity,bcity,date = form.get('acity'),form.get('bcity'),form.get('adate')
    a = Thread_Pool.submit(Function.select_planes, (acity,bcity, date))  # 搜索
    result = a.result()
    if result is False:
        logging.warning('在数据库更新的时候试图访问数据')
        return jsonify({'string': '很抱歉，服务器正在更新中，请稍后再尝试！'})
    if result is None or result == []:
        return jsonify({'string': '很抱歉，暂时没有符合要求的机票'})
    elif len(result) == 1:
        return {
            'common': result,'cost_sort':result,'time_sort':result
        }
    else:
        b = Thread_Pool.submit(Function.sort_planes, result)  # 排序
        cost_sort, time_sort = b.result()
        print(cost_sort)
        # result为搜索后的结构，cost_sort为按价格排序后的结果,time_sort为按时间排序后的结果
        return {
            'common': result, 'cost_sort': cost_sort, 'time_sort': time_sort
        }


@csrf.exempt
@app.post('/index_ajax2')  # 往返
def index_ajax2():
    form = request.form
    print(form)
    acity, bcity, adate, bdate = form.get('acity'), form.get('bcity'), form.get('adate'), form.get('bdate')
    a = Thread_Pool.submit(Function.select_planes, (acity,bcity, adate))
    b = Thread_Pool.submit(Function.select_planes, (bcity,acity, bdate))
    a_result, b_result = a.result(), b.result()
    if a_result is False or b_result is False:
        logging.warning('在数据库更新的时候试图访问数据')
        return jsonify({'string': '很抱歉，服务器正在更新中，请稍后再尝试！'})
    a_len, b_len = len(a_result), len(b_result)
    if a_result is None or a_result == []:
        return jsonify({'string': f'很抱歉，暂时没有从{acity}到{bcity}符合您要求的机票'})
    elif b_result is None or b_result == []:
        return jsonify({'string': f'很抱歉，暂时没有从{bcity}到{acity}符合您要求的机票'})
    elif a_len == 1 and b_len == 1:
        return jsonify({
            'a_common': a_result, 'a_cost_sort': a_result, 'a_time_sort': a_result,
            'b_common': b_result, 'b_cost_sort': b_result, 'b_time_sort': b_result
        })
    elif a_len == 1 and b_len > 1:
        b = Thread_Pool.submit(Function.sort_planes, b_result)
        b_cost_sort, b_time_sort = b.result()
        return jsonify({
            'a_common': a_result, 'a_cost_sort': a_result, 'a_time_sort': a_result,
            'b_common': b_result, 'b_cost_sort': b_cost_sort, 'b_time_sort': b_time_sort
        })
    elif b_len == 1 and a_len > 1:
        a = Thread_Pool.submit(Function.sort_planes, a_result)
        a_cost_sort, a_time_sort = a.result()
        return jsonify({
            'a_common': a_result, 'a_cost_sort': a_cost_sort, 'a_time_sort': a_time_sort,
            'b_common': b_result, 'b_cost_sort': b_result, 'b_time_sort': b_result
        })
    else:
        a = Thread_Pool.submit(Function.sort_planes, a_result)
        b = Thread_Pool.submit(Function.sort_planes, b_result)
        a_cost_sort, a_time_sort = a.result()
        b_cost_sort, b_time_sort = b.result()
        return jsonify({
            'a_common': a_result, 'a_cost_sort': a_cost_sort, 'a_time_sort': a_time_sort,
            'b_common': b_result, 'b_cost_sort': b_cost_sort, 'b_time_sort': b_time_sort
        })


@csrf.exempt
@app.post('/index_ajax3')  # 多程
def index_ajax3():
    informations = request.form.get('informations')
    select_tasks = [
        (information[0],information[1],information[2])
        for information in informations
    ]
    results = []
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(Function.select_planes,task) for task in select_tasks]
        for future in futures:
            results.append(future.result())
    if False in results:
        jsonify({'string': '很抱歉，服务器正在更新中，请稍后再尝试！'})
    for result in results:
        if result is None or result == []:
            return jsonify({'string': f'很抱歉，暂时没有能够满足您所有行程的机票'})
    for i in range(len(results)-1):
        if results[i][6] != select_tasks[i][0] or results[i][7] != select_tasks[i][1]:
            for j in range(i+1,len(results)):
                if results[j][6] == select_tasks[i][0] or results[j][7] == select_tasks[i][1]:
                    temp = results[j]
                    results[j] = results[i]
                    results[i] = temp



@app.get('/settlement')  # 结算
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
@app.post('/settlement_ajax1')  # 单程结算
def settlement_ajax1():
    table = request.form.get('table')
    index, company, flight_number, acity, bcity, adate, bdate = table[0], table[1], table[2], table[6], table[7], table[
        4], table[5]
    numbers = request.form.get('numbers')
    emails = request.form.get('emails')
    Function.set_task([index, acity, numbers])
    t = threading.Thread(target=Function.set_task, args=([acity, index, numbers],))
    t.start()
    content = Function.get_content(company, flight_number, acity, bcity, adate, bdate)
    more = f'。详细信息请访问{request.host_url}'
    if len(emails) == 1:
        t = threading.Thread(target=send_email, args=(app, emails, '购票通知', content + emails[0] + more),name='settlement_thread')
        t.start()
    else:
        tasks = [
            (app, [email], '购票信息', content + email + more)
            for email in emails
        ]
        with ThreadPoolExecutor() as pool:
            pool.map(send_email, tasks)
    return redirect(url_for('success'))


@csrf.exempt
@app.route('/settlement_ajax2', methods=['POST'])  # 往返结算
def settlement_ajax2():
    pass
    form = request.form
    table1, table2 = form.get('table1'), form.get('table2')
    index1, index2 = form.get('index1'), form.get('index2')
    ...


@app.get('/success')
def success():
    return render_template('success.html')


@scheduler.task(trigger=interval, name='plane_update',id='plane_update')
def plane_update():
    Function.planes_Update_Function()

@scheduler.task(trigger='interval',days=2,name='delete_log',id='delete_log')
def delete_log():
    os.remove('./files/flask.log')

def my_listener(event):
    if event.exception:
        print("任务出错了,调度器已终止执行！")
        logging.error("任务出错了,调度器已终止执行")
        scheduler.shutdown()
scheduler.add_listener(my_listener, mask=EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor(max_workers=5)
    scheduler.start()
    print('服务器开始运行')
    app.run(debug=False, port=80, host='0.0.0.0')
    print('服务器关闭')
