from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from flask import Flask, render_template, request, url_for, redirect, make_response, session, jsonify, abort, g
from flask_mail import Mail, Message
from flask_seasurf import SeaSurf
from flask_apscheduler import APScheduler
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.triggers.interval import IntervalTrigger
from user_agents import parse
from markupsafe import escape
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
import os, logging, Function, numpy, json, time, secrets, datetime

# 引入外置环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)  # 从.env文件引入环境变量

# 日志处理
logging.basicConfig()
file_log_handler = TimedRotatingFileHandler(
    filename='./files/logs/flask.log', encoding='UTF-8', delay=True, backupCount=10, interval=10, when='D'
)
# 设置log格式
file_log_handler.setFormatter(
    logging.Formatter("[%(asctime)s]-[%(levelname)s] [%(funcName)s - %(lineno)s- %(message)s]"))
file_log_handler.setLevel(logging.WARNING)  # 记录warning级别的日志
logging.getLogger().addHandler(file_log_handler)

app = Flask(__name__)  # 创建app (Flask对象)
limiter = Limiter(  # 设置网站访问上限
    app,
    key_func=get_remote_address,
    default_limits=["100000 per day", "2000 per hour"]
)  # 设置单ip访问上限：每天100000次，每小时2000次
csrf = SeaSurf(app)  # csrf防护,只有携带特定请求头（含有正确的加密字符串）的post请求才能被视为合法请求

# 定时任务初始化
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.api_enabled = False
# 设置定时任务
interval = IntervalTrigger(
    hours=6,  # 六小时更新一次数据库
    start_date='2022-4-29 08:00:00',
    end_date='2023-5-31 08:00:00',
    timezone='Asia/Shanghai'
)

open = True  # 确认当前数据库中数据是否能对外开放

# 设置内置环境变量
# 设置jinjs2模板的使用格式
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# 设置session的加密密钥
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe(16))

# 页面缓存初始化
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# 引入进程池与线程池，防止线程/进程被过多创建，保护线程/进程安全
Thread_Pool = ThreadPoolExecutor()  # 线程池
# 往进程池里添加任务会有比线程池更大的开销，因此更多地使用线程池
Process_Pool = ProcessPoolExecutor()  # 进程池(Linux服务器)

# 邮件smtp相关配置
app.config.update(dict(
    DEBUG=False,
    MAIL_SERVER='smtp.qq.com',  # 用于发送邮件的SMTP服务
    MAIL_PORT=465,  # 发信端口
    MAIL_USE_SSL=True,  # 是否使用SSL
    MAIL_USERNAME='xxxxxxxxx@qq.com',  # 发信服务器的用户名/把邮箱地址填到此处
    MAIL_PASSWORD='uhnufypshcmhbejf',  # 发信服务器的密码
    MAIL_DEFAULT_SENDER=('April Zhao', 'xxxxxxxxx@qq.com'),  # 默认的发信人
    JSON_AS_ASCII=False
))
mail = Mail(app)

# 引入存储emails的数据库类
emails_db = Function.emails_db()


# 邮件发送函数
def send_email(info: tuple):
    app, emails, subject, content = info
    # 激活程序上下文,防止邮件发送任务放置到线程池之后当前程序上下文丢失
    with app.app_context():
        msg = Message(
            subject=subject,  # 邮件主题
            recipients=[emails]  # 收件人列表
        )
        msg.body = content + '\n收到请勿回复！若您从未注册民航推荐网，请无视这封邮件，注意不要泄露个人信息！'
        try:
            mail.send(msg)  # 邮件发送
        except:
            # 记录错误信息
            logging.error('邮件发送失败！')


@app.errorhandler(404)  # 访问了错误的url
def encounter_404(error):
    # logging.warning('出现了404')
    return render_template('error.html')


@app.errorhandler(403)  # 检测出访问网站的是爬虫程序
def encounter_403(error):
    logging.warning('出现了403,可能是遇到了爬虫或是csrf令牌错误!')
    return f'<h3>很抱歉，您被识别为爬虫程序，如检测错误，请刷新浏览器，很抱歉给您带来了不便,请您谅解！<br></br>{error}</h3>'


@app.template_filter
def judge_Systen():
    # 判断访问的设备是pc端还是移动端
    return request.cookies.get('system') == 'phone'


@app.before_request  # 每次收到请求前检验是否已经登录
def before_request():
    g.email = session.get("email")
    g.login_status = session.get('login_status')
    # 设置session的过期时间
    session.permanent = True
    # 20分钟后刷新页面则自动退出登录
    app.permanent_session_lifetime = datetime.timedelta(minutes=20)


@app.get('/login')  # 登录界面
@cache.cached(timeout=3000, query_string=True)  # 设置缓存
def login():
    #a test
    response = make_response(render_template('login.html'))
    agent = parse(request.user_agent.string)
    if agent.is_bot:
        abort(403)  # 遇到爬虫则返回403
    elif agent.is_mobile:  # 检验是否是移动端
        response.set_cookie(key='system', value='phone', httponly=True)
    else:  # 不是移动端则判定为桌面端
        response.set_cookie(key='system', value='pc', httponly=True)
    # 进入登录（login）界面自动解除登录状态
    # 为保证数据安全，在login页面将主动清除购票和登录信息
    session.clear()
    return response


@app.post('/login_ajax1')  # 登录发送按钮
def login_ajax():
    email = escape(request.form.get('email'))  # 使用escape转义
    Verification_Code = Function.create_String()  # 产生随机字符串作为验证码
    if email and emails_db.exist_account(email):
        Thread_Pool.submit(send_email, (
            app, email, '民航推荐网站登录',
            f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
        ))  # 把发送邮件的任务放入线程池(队列)
        string = '0'  # 邮件发送成功
    else:
        string = '1'  # 用户还未注册
    return jsonify({
        'Code': Verification_Code,
        'string': string
    })


@app.post('/login_ajax2')  # 登录成功
def login_ajax2():
    email = request.form.get('email')
    session['login_status'] = True
    session['email'] = email
    cache.clear()  # 清理缓存
    return request.host_url  # 返回url，交给前端跳转


@app.get('/register')  # 注册界面
@cache.cached(timeout=3000, query_string=True)  # 设置缓存
def register():
    return render_template('register.html')


@app.post('/register_ajax1')  # 注册发送按钮
def register_ajax1():
    email = escape(request.form.get('email'))
    Verification_Code = Function.create_String()
    string = 'hello'
    if email:
        if emails_db.exist_account(email):
            string = '1'  # 提示邮件已注册
        else:
            Thread_Pool.submit(send_email, (
                app, email, '民航推荐网站注册',
                f'【民航】动态密码{Verification_Code}，您正在登录民航官网，验证码五分钟内有效。'
            ))  # 把发送邮件的任务放入线程池
            string = '0'  # 提示已经发送验证码
    return jsonify({
        'Code': Verification_Code,
        'string': string
    })


@app.post('/register_ajax2')  # 注册成功
def register_ajax2():
    email = escape(request.form.get('email'))
    # 把用户信息记录到“数据库”
    emails_db.add_account(email)
    cache.clear()  # 清理缓存
    return url_for('login')  # 返回url，交给前端跳转


# index函数为航班推荐主页面
@app.get('/')  # 主页面
@limiter.limit("50/second", override_defaults=True, error_message='sorry you have too many requests')
def index():
    # 只有登录后的用户才能访问机票查询界面（主界面）
    if g.login_status and g.email:
        return render_template('index.html', url=request.host_url + 'login')
    else:
        # 若未登录则重定向到登录（login）界面
        return redirect(url_for('login'))



@app.post('/index_ajax1')  # 单程
def index_ajax1():
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    form = request.form
    acity, bcity, date = form.get('acity'), form.get('bcity'), form.get('adate')
    if not all([acity, bcity, date]) or Function.judgeCity(acity) or Function.judgeCity(bcity):
        # 如果数据不完成/出发城市（到达城市）不在搜索范围内，则直接返回None，不再消耗服务器资源去搜索
        return jsonify({'string': '1'})
    a = Thread_Pool.submit(Function.select_planes, (acity, bcity, date))  # 搜索
    result = a.result()
    if result is False:
        return jsonify({'string': '0'})
    if result is None or result == []:
        return jsonify({'string': '1'})
    elif len(result) == 1:
        result = json.dumps(result, ensure_ascii=False)
        return {
            'string': '2', 'common': result, 'economy_class': result, 'First_class': result, 'go_sort': result,
            'arrival_sort': result
        }
    else:
        c = Thread_Pool.submit(Function.sort_planes_time, result)  # 按时间排序
        try:
            b = Thread_Pool.submit(Function.sort_planes_cost, numpy.array(result))  # 按价格排序
            economy_class, First_class = b.result()
            economy_class, First_class = economy_class.tolist(), First_class.tolist()
        except:
            b = Thread_Pool.submit(Function.sort_planes_cost_replace,result)
            economy_class, First_class = b.result()
        go_sort, arrival_sort = c.result()
        return jsonify({
            'string': '2', 'common': json.dumps(result, ensure_ascii=False),
            'economy_class': json.dumps(economy_class, ensure_ascii=False),
            'First_class': json.dumps(First_class, ensure_ascii=False),
            'go_sort': go_sort,
            'arrival_sort': arrival_sort
        })



@app.post('/index_ajax2')  # 往返
def index_ajax2():
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    form = request.form
    acity, bcity, adate, bdate = form.get('acity'), form.get('bcity'), form.get('adate'), form.get('bdate')
    if not all([acity, bcity, adate, bdate]) or Function.judgeCity(acity) or Function.judgeCity(bcity):
        return None
    a_result, b_result = Thread_Pool.map(Function.select_planes, [(acity, bcity, adate), (bcity, acity, bdate)])
    if a_result is False or b_result is False:
        # 搜索过程出现错误时，提示服务器端错误信息
        logging.warning('服务器端搜索机票出现错误！')
        return jsonify({'string': '0'})
    a_len, b_len = len(a_result), len(b_result)
    if a_result is None or a_result == []:
        # 往返（双程）其中有往程是没有机票信息的
        return jsonify({'string': '1'})
    elif b_result is None or b_result == []:
        # 往返（双程）其中有返程是没有机票信息的
        return jsonify({'string': '1'})
    elif a_len == 1 and b_len == 1:
        # 二者都只有一条记录，则无需排序，直接返回
        a_result, b_result = json.dumps(a_result, ensure_ascii=False), json.dumps(b_result, ensure_ascii=False)
        return jsonify({
            'string': '2', 'a_common': json.dumps(a_result, ensure_ascii=False), 'a_economy_class': b_result,
            'a_First_class': a_result, 'a_go_sort': a_result, 'a_arrival_sort': a_result,
            'b_common': b_result, 'b_economy_class': b_result, 'b_First_class': b_result,
            'b_go_sort': b_result, 'b_arrival_sort': b_result
        })
    elif a_len == 1 and b_len > 1:
        # 往程只有一条记录，往程无需排序，只需要返程排序即可，减少服务器CPU运算压力
        b = Thread_Pool.submit(Function.sort_planes_time, b_result)
        try:
            a = Thread_Pool.submit(Function.sort_planes_cost, numpy.array(b_result))
            b_economy_class, b_First_class = a.result()
            b_economy_class, b_First_class = b_economy_class.tolist(), b_First_class.tolist()
        except:
            a = Thread_Pool.submit(Function.sort_planes_cost_replace, b_result)
            b_economy_class, b_First_class = a.result()
        b_go_sort, b_arrival_sort = b.result()
        a_result, b_result = json.dumps(a_result, ensure_ascii=False), json.dumps(b_result, ensure_ascii=False)
        return jsonify({
            'string': '2', 'a_common': a_result, 'a_economy_class': a_result,
            'a_First_class': a_result, 'a_go_sort': a_result, 'a_arrival_sort': a_result, 'b_common': b_result,
            'b_economy_class': json.dumps(b_economy_class, ensure_ascii=False),
            'b_First_class': json.dumps(b_First_class, ensure_ascii=False),
            'b_go_sort': b_go_sort,
            'b_arrival_sort': b_arrival_sort
        })
    elif b_len == 1 and a_len > 1:
        # 返往程只有一条记录，返程无需排序，只需要往程排序即可，减少服务器CPU运算压力
        b = Thread_Pool.submit(Function.sort_planes_time, a_result)
        try:
            a = Thread_Pool.submit(Function.sort_planes_cost, numpy.array(a_result))
            a_economy_class, a_First_class = a.result()
            a_economy_class, a_First_class = a_economy_class.tolist(), a_First_class.tolist()
        except:
            a = Thread_Pool.submit(Function.sort_planes_cost_replace, a_result)
            a_economy_class, a_First_class = a.result()
        a_go_sort, a_arrival_sort = b.result()
        a_result, b_result = json.dumps(a_result, ensure_ascii=False), json.dumps(b_result, ensure_ascii=False)
        return jsonify({
            'string': '2', 'a_common': a_result,
            'a_economy_class': json.dumps(a_economy_class, ensure_ascii=False),
            'a_First_class': json.dumps(a_First_class, ensure_ascii=False),
            'a_go_sort': a_go_sort,
            'a_arrival_sort': a_arrival_sort,
            'b_common': b_result, 'b_economy_class': b_result, 'b_First_class': b_result, 'b_go_sort': b_result,
            'b_arrival_sort': b_result
        })
    else:
        # 往返程都有多条记录，二者使用进程池同时排序
        c, d = Thread_Pool.map(Function.sort_planes_time, [a_result, b_result])
        try:
            a, b = Thread_Pool.map(Function.sort_planes_cost, [numpy.array(a_result), numpy.array(b_result)])
            a_economy_class, a_First_class = a
            b_economy_class, b_First_class = b
            a_economy_class, a_First_class = a_economy_class.tolist(), a_First_class.tolist()
            b_economy_class, b_First_class = b_economy_class.tolist(), b_First_class.tolist()
        except:
            a, b = Thread_Pool.map(Function.sort_planes_cost_replace, [a_result, b_result])
            a_economy_class, a_First_class = a
            b_economy_class, b_First_class = b
        a_go_sort, a_arrival_sort = c
        b_go_sort, b_arrival_sort = d
        return jsonify({
            'string': '2', 'a_common': json.dumps(a_result, ensure_ascii=False),
            'a_economy_class': json.dumps(a_economy_class, ensure_ascii=False),
            'a_First_class': json.dumps(a_First_class, ensure_ascii=False),
            'a_go_sort': a_go_sort,
            'a_arrival_sort': a_arrival_sort,
            'b_common': json.dumps(b_result, ensure_ascii=False),
            'b_economy_class': json.dumps(b_economy_class, ensure_ascii=False),
            'b_First_class': json.dumps(b_First_class, ensure_ascii=False),
            'b_go_sort': b_go_sort,
            'b_arrival_sort': b_arrival_sort
        })



@app.post('/index_ajax31')  # ajax3系列为多程
def index_ajax3():
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    informations = json.loads(request.form.get('informations'))
    session['informations'] = informations  # 将多程的城市和时间信息记录在session里
    session['st'] = '3'
    session['num'] = 1  # num记录当前是第几程
    a = Thread_Pool.submit(Function.select_planes, informations[0])
    result = a.result()
    if result is False:
        return jsonify({'string': '0'})
    if result is None or result == []:
        return jsonify({'string': '1'})
    elif len(result) == 1:
        result = json.dumps(result, ensure_ascii=False)
        return {
            'string': '2', 'common': result, 'economy_class': result, 'First_class': result, 'go_sort': result,
            'arrival_sort': result
        }
    else:
        c = Process_Pool.submit(Function.sort_planes_time, result)  # 按时间排序
        try:
            b = Process_Pool.submit(Function.sort_planes_cost, numpy.array(result))  # 按价格排序
            economy_class, First_class = b.result()
            economy_class, First_class = economy_class.tolist(), First_class.tolist()
        except:
            b = Process_Pool.submit(Function.sort_planes_cost_replace, result)  # 按价格排序
            economy_class, First_class = b.result()
        go_sort, arrival_sort = c.result()
        return jsonify({
            'string': '2', 'common': json.dumps(result, ensure_ascii=False),
            'economy_class': json.dumps(economy_class, ensure_ascii=False),
            'First_class': json.dumps(First_class, ensure_ascii=False),
            'go_sort': go_sort,
            'arrival_sort': arrival_sort
        })



@app.post('/index_ajax32')  # 多程
def index_ajax32():
    num = session['num']
    session['num'] += 1  # table索引加一
    table = json.loads(request.form.get('table'))
    session[f'table{num}'] = table  # 将当前信息记录下来
    adate = table[5]
    informations = session.get('informations')
    if open is False:
        logging.warning('数据库更新时试图访问数据!')
        return jsonify({'string': '0'})
    a = Thread_Pool.submit(Function.select_planes, informations[num])
    result = a.result()
    if result is False:
        return jsonify({'string': '0'})
    if result is None or result == []:
        return jsonify({'string': '1'})
    if len(result) == 1 and Function.judgeDate(adate, result[0][4]):
        result = json.dumps(result, ensure_ascii=False)
        return {
            'string': '2', 'common': result, 'economy_class': result,
            'First_class': result, 'go_sort': result, 'arrival_sort': result
        }
    else:
        results = []
        for i in result:
            if Function.judgeDate(adate, i[4]):
                results.append(i)
        c = Process_Pool.submit(Function.sort_planes_time, results)  # 按时间排序
        try:
            b = Process_Pool.submit(Function.sort_planes_cost, numpy.array(results))  # 按价格排序
            economy_class, First_class = b.result()
            economy_class, First_class = economy_class.tolist(), First_class.tolist()
        except:
            b = Process_Pool.submit(Function.sort_planes_cost_replace, results)  # 按价格排序
            economy_class, First_class = b.result()
        go_sort, arrival_sort = c.result()
        return jsonify({
            'string': '2', 'common': json.dumps(results, ensure_ascii=False),
            'economy_class': json.dumps(economy_class, ensure_ascii=False),
            'First_class': json.dumps(First_class, ensure_ascii=False),
            'go_sort': go_sort,
            'arrival_sort': arrival_sort
        })



@app.delete('/index_ajax33')
def index_ajax33(): #清空存储在session的缓存数据
    if session.get('num'):
        # 清空多程的session缓存
        num = session.get('num')
        for i in range(1,num+1):
            if session.get(f'table{num}'):
                session.pop(f'table{num}')
    if session.get('tables'):
        #清空整合后多程的session缓存
        session.pop('tables')
    if session.get('table'):
        #清空单程或往返的缓存
        session.pop('table')
    return 'success'



@app.post('/index_ajax4')  # 结算按钮
def index_ajax4():
    form = request.form
    # 将用户确定的信息暂时存储到session里
    st = form.get('st')
    if st == '1' or st == '2':  # 单程或往返
        session['st'] = st
        session['table'] = form.get('table')
    else:  # 多程
        num = session['num']
        table = json.loads(form.get('table'))
        session[f'table{num}'] = table
    session['settlement'] = True  # 设置结算（settlement）页面为可进页面
    return url_for('settlement', _external=True)


@app.post('/settlement_ajax')  # 将数据传给结算页面
def settlement_ajax():
    # st记录用户选择：1代表单程，2代表往返，3代表多程
    st = session.get('st')
    email = session.get('email')
    if st == '3':
        # 多程结算成功后把数据整合成一个二维列表
        num = session.get('num')
        tables = []
        for i in range(num):
            tables.append(session.get(f'table{i + 1}'))
        session['tables'] = tables
        session.pop('informations')  # 弹出城市和时间信息
        return jsonify({
            'st': st, 'table': json.dumps(tables), 'email': email
        })
    else:
        return jsonify({
            'st': st, 'table': session.get('table'), 'email': email
        })


@app.route('/settlement', methods=['GET', 'POST'])  # 结算界面
def settlement():
    settlement = session.get('settlement')
    if g.email and g.login_status and settlement:
        email = g.email
        st = session.get('st')
        if request.method == 'POST':  # 支付按钮
            emails = json.loads(request.form.get('emails'))  # 获取乘客邮箱地址列表
            emails.append(email)  # 把当前登录用户的邮箱地址加入到列表中
            people = 0  # 人数
            if st == '1':  # 单程
                table = json.loads(session.get('table'))
                cabin = '经济舱' if table[-1] == 'j' else '公务舱'  # 判断是经济舱还是公务舱
                for each_email in emails:
                    if each_email != '':
                        people += 1
                        Thread_Pool.submit(send_email, (app, each_email, '购票通知', Function.get_content_single(
                            table[1], table[2], table[6], table[7], table[4], table[5], cabin
                        ) + f'{email}。详细信息请访问{request.host_url}'))
                Function.set_task([table[6], table[0], people])
            elif st == '2':  # 往返
                table = json.loads(session.get('table'))
                cabin1 = '经济舱' if table[0][-1] == 'j' else '公务舱'
                cabin2 = '经济舱' if table[1][-1] == 'j' else '公务舱'
                # 设置任务
                for each_email in emails:
                    if each_email != '':
                        people += 1
                        Thread_Pool.submit(send_email, (app, each_email, '购票通知', Function.get_content_double(
                            table[0][1], table[1][1], table[0][2], table[1][2], table[0][6], table[0][7], table[0][4],
                            table[1][4], table[0][5], table[1][5], cabin1, cabin2
                        ) + f'{email}。详细信息请访问{request.host_url}'))
                Function.set_task([table[0][6], table[0][0], people])
                Function.set_task([table[1][6], table[1][0], people])
            elif st == '3':  # 多程
                tables = session.get('tables')
                num = len(tables)
                for each_email in emails:
                    if each_email != '':
                        people += 1
                        Thread_Pool.submit(send_email, (
                            app, each_email, '购票通知', Function.get_content_multiply(num, tables, email, request.host_url)
                        ))
                for table in tables:
                    Function.set_task([table[6], table[0], people])
            else:  # st被篡改,csrf防护被攻破
                logging.warning('非法访问,外部(疑似爬虫或攻击)发送了post请求！')
                abort(404)
            # 回到login登录界面后，会主动退出登录并清除所有购票以及登录信息，及时清空所有缓存
            return url_for('login', _external=True)
        return render_template('settlement.html')
    elif g.email and g.login_status:  # 已登录，但是没有通过“预定”审核
        return redirect(url_for('index'))
    else:  # 用户未登录则直接跳回登录界面
        return redirect(url_for('login'))


@app.delete('/settlement_ajax')  # 返回页面
def delete_info():
    st = session.get('st')
    if st == '1' or st == '2':
        # 如果当前是单程或往返，则删除table缓存
        session.pop('table')
    elif st == '3':
        # 如果是多程，则要删除合并之后的tables缓存以及几程数num
        session.pop('tables')
        session.pop('num')
    session.pop('st')
    session.pop('settlement')  # 取消返回后用户访问结算（settlement）的权限
    return request.host_url


@csrf.exempt  # csrf审查豁免
@app.get('/wait')
@cache.cached(timeout=86400)
def wait():
    # 为搜索时动画页面注册函数
    if g.login_status and g.email:
        return render_template('wait.html')
    else:
        # 未登录则无法访问动画页面
        abort(404)


@scheduler.task(trigger=interval, name='plane_update', id='1')
def plane_update():
    global open  # 将更改全局变量open
    open = False  # 更新数据库时暂停搜索服务
    logging.info('数据库开始更新~')
    time.sleep(1)  # 缓一缓(阻塞线程)
    try:
        Function.planes_Update_Function()  # 执行数据库更新函数
    except:
        logging.warning('机票信息更新出现错误！')
    open = True  # 更新结束后重新开启搜索服务


@scheduler.task(trigger='interval', days=5, name='delete_log', id='2')
def delete_log():
    # 执行日志删除函数
    try:
        Function.delete_log_byhand(keep_file=True)
    except:
        Function.delete_log_byhand(keep_file=False)


# 定时任务出错函数
def listen_error(event):
    if event.job_id == '1':
        global open
        open = True
        logging.error('数据库更新时出现了错误!')
    else:
        logging.error('删除日志时出现了错误！')


# 定时任务完成函数
def finished_task(event):
    if event.job_id == '1':
        logging.info('数据库已完成更新！')
    else:
        logging.info('日志已自动删除！')


# 监听定时任务，遇到报错时记录错误
scheduler.add_listener(listen_error, mask=EVENT_JOB_ERROR)
# 监听定时任务，定时任务执行后记录执行信息
scheduler.add_listener(finished_task, mask=EVENT_JOB_EXECUTED)
# 启动定时任务
scheduler.start()

if __name__ == '__main__':
    Process_Pool = ProcessPoolExecutor()  # 进程池(Windows)
    # scheduler.start()
    print('服务器开始运行')
    app.run(port=8000, host='0.0.0.0', load_dotenv=True)
    print('服务器关闭')
