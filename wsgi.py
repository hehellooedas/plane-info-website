from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR,EVENT_JOB_EXECUTED
from flask import Flask, render_template, request, url_for, redirect, make_response, session, jsonify, abort
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_seasurf import SeaSurf
from flask_apscheduler import APScheduler
from flask_avatars import Avatars
from flask_caching import Cache
#from flask_sslify import SSLify
from apscheduler.triggers.interval import IntervalTrigger
from user_agents import parse
from markupsafe import escape
from logging.handlers import TimedRotatingFileHandler
import os, logging, Function,numpy,json,time



# 日志处理
logging.basicConfig()
file_log_handler = TimedRotatingFileHandler(
filename='./files/logs/flask.log', encoding='UTF-8', delay=True,backupCount=10, interval=10, when='D'
)
file_log_handler.setFormatter(logging.Formatter("[%(asctime)s]-[%(levelname)s] [%(funcName)s - %(lineno)s- %(message)s]"))
file_log_handler.setLevel(logging.WARNING)#记录warning级别的日志
logging.getLogger().addHandler(file_log_handler)

app = Flask(__name__)
csrf = SeaSurf(app)  # csrf防护
scheduler = APScheduler()  # 定时任务
scheduler.init_app(app)
scheduler.api_enabled = True
#sslify = SSLify(app)
#app.config['SLACK_WEBHOOK_URL'] = os.environ.get('SLACK_WEBHOOK_URL')
#app.config['SSL_DISABLED'] = False
interval = IntervalTrigger(
    hours=6,  # 六小时更新一次数据库
    start_date='2022-4-29 08:00:00',
    end_date='2023-5-31 08:00:00',
    timezone='Asia/Shanghai'
)
open = True#确认当前数据库中数据是否能对外开放
# 设置内置环境变量
CORS(app, supports_credentials=True)
#os.environ['FLASK_APP'] = 'wsgi'
#os.environ['FLASK_ENV'] = 'development'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', Function.create_String(16))
avatars = Avatars(app)#生成头像
cache = Cache(app, config={'CACHE_TYPE': 'simple'})#页面缓存
Thread_Pool = ThreadPoolExecutor()#线程池

# 邮件smtp相关配置
app.config.update(dict(
    DEBUG=False,
    MAIL_SERVER='smtp.qq.com',  # 用于发送邮件的SMTP服务
    MAIL_PORT=465,  # 发信端口
    MAIL_USE_SSL=True,  # 是否使用SSL
    MAIL_USERNAME='928309386@qq.com',  # 发信服务器的用户名
    MAIL_PASSWORD='uhnufypshcmhbejf',  # 发信服务器的密码
    MAIL_DEFAULT_SENDER=('April Zhao', '928309386@qq.com'),  # 默认的发信人
    JSON_AS_ASCII=False
))
mail = Mail(app)

#存储emails的数据库类
emails_db = Function.emails_db()


# 邮件发送函数
def send_email(info: tuple):
    app, emails, subject, content = info
    with app.app_context():
        msg = Message(
            subject=subject,
            recipients=[emails]
        )
        msg.body = content + '\n收到请勿回复！若您从未注册民航推荐网，请无视这封邮件，注意不要泄露个人信息！'
        try:
            mail.send(msg)
        except:
            logging.error('邮件发送失败！')


@app.errorhandler(404)#访问了错误的url
def encounter_404(error):
    logging.warning('出现了404')
    return render_template('error.html')


@app.errorhandler(403)#检测出访问网站的是爬虫程序
def encounter_403(error):
    logging.warning('出现了403,可能是遇到了爬虫!')
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
        abort(403)#遇到爬虫则返回403
    elif agent.is_mobile:
        response.set_cookie(key='system', value='phone')
    else:
        response.set_cookie(key='system', value='pc')
    if 'login_status' in session and 'email' in session:
        session.pop('login_status')
        session.pop('email')
    return response


@csrf.exempt
@app.post('/login_ajax1')
def login_ajax():
    email = escape(request.form.get('email'))
    Verification_Code = Function.create_String()
    if email and emails_db.exist_account(email):
        Thread_Pool.submit(send_email, (
            app, email, '民航推荐网站登录',
            f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
        ))
        string = u'邮件已发送，请注意查收！'
    else:
        string = u'您的账户并未注册，请检查邮件是否填写正确！'
    return jsonify({
        'Code': Verification_Code,
        'string': string
    })


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
            Thread_Pool.submit(send_email, (
                app, email, '民航推荐网站注册',
                f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
            ))
            string = u'邮件已发送，请注意查收！'
    return jsonify({
        'Code': Verification_Code,
        'string': string
    })


@csrf.exempt
@app.post('/register_ajax2')
def register_ajax2():
    email = request.form.get('email')
    Thread_Pool.submit(emails_db.add_account,email)
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
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    form = request.form
    acity, bcity, date = form.get('acity'), form.get('bcity'), form.get('adate')
    a = Thread_Pool.submit(Function.select_planes, (acity, bcity, date))  # 搜索
    result = a.result()
    if result is False:
        return jsonify({'string': '0'})
    if result is None or result == []:
        return jsonify({'string': '1'})
    elif len(result) == 1:
        result = json.dumps(result,ensure_ascii=False)
        return {
            'string':'2','common': result,'economy_class':result,'First_class':result,'go_sort':result,'arrival_sort':result
        }
    else:
        b = Thread_Pool.submit(Function.sort_planes_cost, numpy.array(result))  # 排序
        c = Thread_Pool.submit(Function.sort_planes_time,result)
        economy_class,First_class = b.result()
        go_sort,arrival_sort = c.result()
        return jsonify({
            'string':'2','common': json.dumps(result,ensure_ascii=False),
            'economy_class':json.dumps(economy_class.tolist(),ensure_ascii=False),
            'First_class':json.dumps(First_class.tolist(),ensure_ascii=False),
            'go_sort':go_sort,
            'arrival_sort':arrival_sort
        })


@csrf.exempt
@app.post('/index_ajax2')  # 往返
def index_ajax2():
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    form = request.form
    acity, bcity, adate, bdate = form.get('acity'), form.get('bcity'), form.get('adate'), form.get('bdate')
    a_result, b_result = Thread_Pool.map(Function.select_planes,[(acity, bcity, adate),(bcity, acity, bdate)])
    if a_result is False or b_result is False:
        return jsonify({'string': '0'})
    a_len, b_len = len(a_result), len(b_result)
    if a_result is None or a_result == []:
        return jsonify({'string': '1'})
    elif b_result is None or b_result == []:
        return jsonify({'string': '1'})
    elif a_len == 1 and b_len == 1:
        a_result,b_result = json.dumps(a_result,ensure_ascii=False),json.dumps(b_result,ensure_ascii=False)
        return jsonify({
            'string':'2','a_common': json.dumps(a_result,ensure_ascii=False),'a_economy_class':b_result,
            'a_First_class':a_result,'a_go_sort':a_result,'a_arrival_sort':a_result,
            'b_common': b_result, 'b_economy_class':b_result,'b_First_class':b_result,
            'b_go_sort':b_result,'b_arrival_sort':b_result
        })
    elif a_len == 1 and b_len > 1:
        a = Thread_Pool.submit(Function.sort_planes_cost,numpy.array(b_result))
        b = Thread_Pool.submit(Function.sort_planes_time,b_result)
        b_economy_class, b_First_class = a.result()
        b_go_sort,b_arrival_sort = b.result()
        a_result, b_result = json.dumps(a_result, ensure_ascii=False), json.dumps(b_result, ensure_ascii=False)
        return jsonify({
            'string':'2','a_common': a_result, 'a_economy_class':a_result,
            'a_First_class':a_result,'a_go_sort':a_result,'a_arrival_sort':a_result,'b_common': b_result,
            'b_economy_class':json.dumps(b_economy_class.tolist(),ensure_ascii=False),
            'b_First_class':json.dumps(b_First_class.tplist(),ensure_ascii=False),
            'b_go_sort':b_go_sort,
            'b_arrival_sort':b_arrival_sort
        })
    elif b_len == 1 and a_len > 1:
        a = Thread_Pool.submit(Function.sort_planes_cost, numpy.array(a_result))
        b = Thread_Pool.submit(Function.sort_planes_time, a_result)
        a_economy_class,a_First_class = a.result()
        a_go_sort,a_arrival_sort = b.result()
        a_result, b_result = json.dumps(a_result, ensure_ascii=False), json.dumps(b_result, ensure_ascii=False)
        return jsonify({
            'string':'2','a_common': a_result,
            'a_economy_class':json.dumps(a_economy_class.tolist(),ensure_ascii=False),
            'a_First_class':json.dumps(a_First_class.tolist(),ensure_ascii=False),
            'a_go_sort':a_go_sort,
            'a_arrival_sort':a_arrival_sort,
            'b_common': b_result, 'b_economy_class':b_result,'b_First_class':b_result,'b_go_sort':b_result,'b_arrival_sort':b_result
        })
    else:
        a,b = Process_Pool.map(Function.sort_planes_cost,[numpy.array(a_result),numpy.array(b_result)])
        c,d = Process_Pool.map(Function.sort_planes_time,[a_result,b_result])
        a_economy_class, a_First_class = a
        a_go_sort, a_arrival_sort = c
        b_economy_class, b_First_class = b
        b_go_sort, b_arrival_sort = d
        return jsonify({
            'string':'2','a_common': json.dumps(a_result, ensure_ascii=False),
            'a_economy_class':json.dumps(a_economy_class.tolist(),ensure_ascii=False),
            'a_First_class':json.dumps(a_First_class.tolist(),ensure_ascii=False),
            'a_go_sort':a_go_sort,
            'a_arrival_sort':a_arrival_sort,
            'b_common': json.dumps(b_result, ensure_ascii=False),
            'b_economy_class':json.dumps(b_economy_class.tolist(),ensure_ascii=False),
            'b_First_class':json.dumps(b_First_class.tolist(),ensure_ascii=False),
            'b_go_sort':b_go_sort,
            'b_arrival_sort':b_arrival_sort
        })


@csrf.exempt
@app.post('/index_ajax3')  # 多程
def index_ajax3():
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    informations = json.loads(request.form.get('informations'))
    n = len(informations)
    results = [result for result in Thread_Pool.map(Function.select_planes
    ,[(information[0], information[1], information[2]) for information in informations])]
    if False in results:
        jsonify({'string': '0'})
    if [] in results or None in results:
        return jsonify({'string': '1'})
    a = Process_Pool.map(Function.sort_planes_cost,[numpy.array(i) for i in results])

    #for i in range(n-1):
        #for j in range(i,n):
            #if results[j][6] == informations[i][0] and results[j][7] == informations[i][1]:
                #results[i],results[j] = results[j],results[i]
                #return


@csrf.exempt
@app.post('/index_ajax4')
def index_ajax4():
    response = make_response(redirect(url_for('settlement')))
    session['st'] = request.form.get('st')
    session['table'] = request.form.get('table')
    session['cabin'] = request.form.get('cabin')
    session['settlement'] = True
    return response


@csrf.exempt
@app.route('/settlement',methods=['GET','POST'])  # 结算
def settlement():
    email = session.get("email")
    login_status = session.get('login_status')
    settlement = session.get('settlement')
    if email and login_status and settlement:
        st = session.get('st')
        table = session.get('table')
        cabin = session.get('cabin')
        if request.method == 'POST':
            emails = json.loads(request.form.get('emails'))
            if st == '1':
                Thread_Pool.submit(Function.set_task,[table[6], table[0], len(emails)])
                for i in emails:
                    Thread_Pool.submit(send_email, (app, i, '购票通知', Function.get_content(
                        table[1],table[2],table[6],table[7],table[4],table[5]
                    ) + emails[0] + f'。详细信息请访问{request.host_url}'))
            elif st == '2':
                Thread_Pool.submit(Function.set_task, [table[0][6], table[0][0], len(emails)])
                Thread_Pool.submit(Function.set_task, [table[1][6], table[1][0], len(emails)])
                for i in emails:
                    ...
            elif st == '3':
                n = len(table)
                ...
            else:
                logging.warning('非法访问！')
                abort(404)
            return redirect(url_for('success'))
        data = {
            'email':email,'table':table,'cabin':cabin,'st':st
        }
        return render_template('settlement.html',**data)
    elif email and login_status:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))



    #Thread_Pool.submit(Function.set_task,[acity, index, numbers])
    #content = Function.get_content(company, flight_number, acity, bcity, adate, bdate)
    #more = f'。详细信息请访问{request.host_url}'
    #if len(emails) == 1:
        #Thread_Pool.submit(send_email,(app, emails, '购票通知', content + emails[0] + more))
    #else:
        #tasks = [
            #(app, [email], '购票信息', content + email + more)
            #for email in emails
        #]
        #with ThreadPoolExecutor() as pool:
            #pool.map(send_email, tasks)
    #return redirect(url_for('success'))




@app.get('/success')
def success():
    if session.get('login_status'):
        return render_template('success.html')
    else:
        return redirect(url_for('login'))

@app.get('/wait')
@cache.cached()
def wait():
    if session.get('login_status'):
        return render_template('wait.html')
    else:
        return redirect(url_for('login'))

@scheduler.task(trigger=interval, name='plane_update', id='1')
def plane_update():
    global open
    open = False #更新数据库时暂停搜索服务
    logging.info('数据库开始更新~')
    time.sleep(1)
    Function.planes_Update_Function()
    open = True #更新结束后重新开启搜索服务


@scheduler.task(trigger='interval', days=5, name='delete_log', id='2')
def delete_log():
    Function.delete_log_byhand()


def listen_error(event):
    if event.job_id == '1':
        logging.error('数据库更新时出现了错误!')
    else:
        logging.error('删除日志时出现了错误！')

def finished_task(event):
    if event.job_id == '1':
        logging.info('数据库已完成更新！')
    else:
        logging.info('日志已自动删除！')

scheduler.add_listener(listen_error,mask=EVENT_JOB_ERROR)
scheduler.add_listener(finished_task,mask=EVENT_JOB_EXECUTED)


if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor()#进程池
    scheduler.start()
    print('服务器开始运行')
    app.run(port=80, host='0.0.0.0')
    print('服务器关闭')
