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
import os, threading, Function



app = Flask(__name__)
csrf = SeaSurf(app)
# 设置内置环境变量
CORS(app, supports_credentials=True)
os.environ['FLASK_APP'] = 'wsgi'
os.environ['FLASK_ENV'] = 'development'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = os.getenv('SECRET_KEY', Function.create_String(16))
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
def send_email(app, emails, subject='EmailTest', content=u'这是一条从民航行程推荐网站发来的邮件(收到请勿回复!)',html=None):
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
@app.route('/login_ajax1', methods=['POST'])
def login_ajax():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        Verification_Code = Function.create_String()
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
@app.route('/login_ajax2', methods=['POST'])
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
@app.route('/register_ajax1', methods=['POST'])
def register_ajax1():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        Verification_Code = Function.create_String()
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
@app.route('/register_ajax2', methods=['POST'])
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
@app.post('/index_ajax1')
def index_ajax1():
    if request.method == 'POST':
        acity = request.form.get('acity')
        bcity = request.form.get('bcity')
        date = request.form.get('date')
        plane_db = Function.planes_db(acity)
        a = Thread_Pool.submit(plane_db.select_planes,(bcity,date))#搜索
        result = a.result()
        if result is None or result == []:
            return jsonify({'string':'很抱歉，暂时没有符合要求的机票'})
        elif len(result) == 1:
            return {
                'common':result
            }
        else:
            b = Process_Pool.submit(plane_db.sort_planes,result)#排序
            cost_sort,time_sort = b.result()
            return {
                'common':result,'cost_sort':cost_sort,'time_sort':time_sort
            }


@csrf.exempt
@app.post('index_ajax2')
def index_ajax2():
    if request.method == 'POST':
        acity = request.form.get('acity')
        bcity = request.form.get('bcity')
        adate = request.form.get('adate')
        bdate = request.form.get('bdate')
        a_plane_db = Function.planes_db(acity)
        b_plane_db = Function.planes_db(acity)
        a = Thread_Pool.submit(a_plane_db.select_planes,(bcity,adate))
        b = Thread_Pool.submit(a_plane_db.select_planes,(acity,bdate))
        a_result,b_result = a.result(),b.result()
        a_len,b_len = len(a_result),len(b_result)
        if a_result is None or b_result is None or a_result == [] or b_result == []:
            return jsonify({'string':'很抱歉，暂时没有符合要求的机票'})
        elif a_len==1 and b_len==1:
            return {'a_common':a_result,'b_common':b_result}
        elif a_len==1 and b_len>1:
            b = Process_Pool.submit(b_plane_db.sort_planes,b_result)
            b_cost_sort,b_time_sort = b.result()
            return {'a_common':a_result,'b_common':b_result,'b_cost_sort':b_cost_sort,'b_time_sort':b_time_sort}
        elif b_len==1 and a_len>1:
            a = Process_Pool.submit(a_plane_db.sort_planes,a_result)
            a_cost_sort,a_time_sort = a.result()
            return {'a_common':a_result,'a_cost_sort':a_cost_sort,'a_time_sort':a_time_sort,'b_comon':b_result}
        else:
            a = Process_Pool.submit(a_plane_db.sort_planes, a_result)
            b = Process_Pool.submit(b_plane_db.sort_planes, b_result)
            a_cost_sort, a_time_sort = a.result()
            b_cost_sort, b_time_sort = b.result()
            return {'a_common':a_result,'a_cost_sort':a_cost_sort,'a_time_sort':a_time_sort,
                    'b_common':b_result,'b_cost_sort':b_cost_sort,'b_time_sort':b_time_sort
                }

@csrf.exempt
@app.post('index_ajax3')
def index_ajax3():
    if request.method == 'POST':
        nums = request.form.get('nums')
        ...





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
@app.route('/settlement_ajax1', methods=['POST'])
def settlement_ajax1():
    if request.method == 'POST':
        index = g.get('index')
        table = g.get('table')
        cabin = g.get('cabin')
        numbers = g.get('numbers')
        emails = g.get('emails')
        table = g.get('table')
        for i in table:
            if i[0]==index:
                company = i[1]
                flight_number = i[3]
                acity = i[8]
                bcity = i[9]
                adate = i[5]
                bdate = i[6]
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
