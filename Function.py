import pandas, pickle, os, random, time, copy,numpy,numba,json


def delete_log_byhand(keep_file=False):#删除日志
    if keep_file == True:
        open('./files/logs/flask.log','w').close()
    else:
        os.remove('./files/logs/flask.log')


def get_date(date_time:str)->str:#解析日期
    return date_time.split(' ')[0]


def get_time(date_time:str)->str:#解析时间
    return date_time.split(' ')[1]


def get_Time():#获取当前时间
    return time.strftime("%Y-%m-%d", time.localtime())


def get_Szm(city: str) -> str:
    """
    获取当前城市的三字码（常用于机票的一种编码）
    :param city: 城市名
    :return: 三字码
    """
    table = {
        '三亚': "SYX", '上海': "SHA", "北京": "BJS", "南京": "NKG", "厦门": "XMN", "大连": "DLC", "广州": "CAN", "成都": "CTU",
        "昆明": "KMG", "杭州": "HGH", "武汉": "WUH", "济南": "TNA", '深圳': 'SZX', "福州": "FOC", "郑州": "CGO", "西安": "SIA",
        "重庆": "CKG", "长沙": "CSX", "青岛": "TAO",'北海': 'BHY','承德': 'CDE','长春': 'CGQ', '朝阳': 'CHG','常州': 'CZX', '大同': 'DAT',
        '义乌': 'YIW','烟台': 'YNT','扬州': 'YTY','西双版纳': 'JHG','佛山': 'FUO','合肥': 'HFE', '九江': 'JIU', '洛阳': 'LYA','宁波': 'NGB',
        '南阳': 'NNY','南通': 'NTG','南宁': 'NNG', '攀枝花': 'PZI','衢州': 'JUZ','沈阳': 'SHE', '温州': 'WNZ',"天津": "TSN", '无锡': 'WUX',
        '舟山': 'HSN','珠海': 'ZUH', '哈尔滨': 'HRB','乌鲁木齐': 'URC','唐山': 'TVS','襄阳': 'XFN','宜宾': 'YBP'
    }
    return table.get(city)


def judgeCity(city:str):
    """
    判断城市是否有对应文件（在搜索范围内）
    :param city: 要搜索的城市（出发城市）
    :return: 如果不在城市列表中，则返回True
    """
    citylist = ('北京', '成都', '大连', '福州', '广州', '杭州', '济南', '昆明', '南京', '青岛', '三亚', '厦门', '上海', '深圳', '武汉', '西安', '长沙',
               '郑州', '重庆', '天津','北海', '承德', '长春', '朝阳', '常州', '大同', '义乌', '烟台', '扬州', '西双版纳', '佛山', '合肥', '九江',
               '洛阳', '宁波', '南阳', '南通', '南宁', '攀枝花', '衢州', '沈阳', '温州', '无锡', '舟山', '珠海', '哈尔滨', '乌鲁木齐', '唐山', '襄阳','宜宾'
                )
    return city not in citylist


def get_content_single(company, flight_number, acity, bcity, adate, bdate,cabin)->str:
    """
    单程情况下，发送的邮件的内容
    :param company: 航空公司
    :param flight_number: 航班名
    :param acity: 出发城市
    :param bcity: 到达城市
    :param adate: 出发时间
    :param bdate: 到达时间
    :param cabin: 经济舱/公务舱
    :return: 单程邮件内容
    """
    return f'【民航行程信息】您的单程机票已于{get_Time()}支付成功。{get_date(adate)} {company} {flight_number}航班' \
           f'{cabin},{acity}（{get_Szm(acity)}） {get_time(adate)} - {bcity}（{get_Szm(bcity)}）' \
           f'{get_time(bdate)}。\n航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续' \
           f'并提前20分钟抵达登机口。乘机人'



def get_content_double(company1,company2,flight_number1,flight_number2,acity,bcity,adate1,bdate1,adate2,bdate2,cabin1,cabin2)->str:
    """
    往返情况下，发送邮件的内容
    :param company1: 去程航空公司
    :param company2: 返程航空公司
    :param flight_number1: 去程航班名
    :param flight_number2: 返程航班吗
    :param acity: 去程出发城市
    :param bcity: 返程出发城市
    :param adate1: 去程出发时间
    :param bdate1: 去程到达时间
    :param adate2: 返程出发时间
    :param bdate2: 返程到达时间
    :param cabin1: 去程舱室选择
    :param cabin2: 返程舱室选择
    :return: 往返邮件内容
    """
    return f'【民航行程信息】您的往返机票已于{get_Time()}支付成功。往：{get_date(adate1)} {company1} {flight_number1}航班{cabin1},{acity}({get_Szm(acity)})' \
           f' {get_time(adate1)} - {bdate1}({get_Szm(bcity)}) {get_time(bdate1)}。返：{get_date(adate2)} {company2} {flight_number2}航班{cabin2},' \
           f'{bcity}({get_Szm(bcity)}) {get_time(adate2)} - {acity}({get_Szm(acity)}) {get_time(bdate2)}。 \n' \
           f'航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续并提前20分钟抵达登机口。乘机人'



def get_content_multiply(num,tables,email,url):
    """
    多程情况下，邮件内容
    :param num:几程
    :param tables:二维数组，二维数组里每个一位数组都是航班信息
    :param email: 购票者邮件
    :param url: 航班推荐网站网址
    :return: 邮件内容
    """
    content = f'【民航行程信息】您的多程机票已于{get_Time()}支付成功。\n'
    for i in range(num):
        cabin = '经济舱' if tables[i][-1]=='j' else '公务舱'
        table = tables[i]
        content += f'第{i+1}程：{get_date(tables[i][0])} {table[1]} {table[2]}航班 {cabin},{table[6]}（{get_Szm(table[6])}）{get_time(table[4])} - ' \
                   f'{table[7]}（{get_Szm(table[7])}）{get_time(table[5])}\n'
    content += f'航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续' \
           f'并提前20分钟抵达登机口。乘机人{email}。详细信息请访问{url}'
    return content




def create_String(n:int=6)->str:#生成随机字符串
    """
    Generate random string
    :param n:int
    :return:a random string
    """
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))



def set_task(arr: list):
    """
    设置任务函数，每成功购票一次，就会设置任务
    :param arr: 购票的航班信息。例：[目标城市，目标索引，人数]
    :return: None
    """
    if os.path.exists('./files/tasks.pickle'):
        if os.path.getsize('./files/tasks.pickle'):
            with open('./files/tasks.pickle', 'rb+') as f:
                a = pickle.load(f)
                f.truncate()
            with open('./files/tasks.pickle', 'rb+') as f:
                a.append(arr)
                pickle.dump(a, f)
        else:
            with open('./files/tasks.pickle', 'rb+') as f:
                pickle.dump([arr], f)
    else:
        with open('./files/tasks.pickle', 'wb+') as f:
            pickle.dump([arr], f)



def planes_Update_Function():
    """
    航班数据更新函数，每隔6小时执行一次，对以购票的信息更新数据库中的航班余座信息
    :return: None
    """
    if os.path.exists('./files/tasks.pickle') and os.path.getsize('./files/tasks.pickle') != 0:
        with open('./files/tasks.pickle', 'rb+') as f:
            tasks = pickle.load(f)
            for task in tasks:
                city, index, numbers = task
                information = pandas.read_pickle(f'./files/citys/{city}.pickle')
                information['余座'].values[index] -= numbers#航班余座减少
                pandas.to_pickle(f'./files/citys/{city}.pickle')
            f.truncate()  # 完成所有task之后，清空这个写有任务的pickle文件



@numba.jit(nopython=True,cache=True,nogil=True)#采用numba的LLVM编译器编译优化排序算法
def sort_planes_cost(result)->tuple:#按价格升序
    """
    航班信息按照价格排序
    :param result: 航班信息
    :return:元组，第一项是按照经济舱价格升序，第二项是按照公务舱价格升序
    """
    for i in range(len(result) - 1):
        index = i
        for j in range(i+1, len(result)):
            if len(str(result[index][8])) > len(str(result[j][8])) or \
                    (len(str(result[index][8])) == len(str(result[j][8])) and str(result[index][8]) > str(result[j][8])):
                index = j
        if index != i:
            temp = numpy.copy(result[index])
            result[index] = result[i]
            result[i] = temp
    cost_sort_Economics = numpy.copy(result)  # 申请一段内存单独存储排序后的结果
    for i in range(len(result) - 1):
        index = i
        for j in range(i+1, len(result)):
            if len(str(result[index][9])) > len(str(result[j][9])) or \
                    (len(str(result[index][9])) == len(result[j][9]) and str(result[index][9]) > str(result[j][9])):
                index = j
        if index != i:
            temp = numpy.copy(result[index])
            result[index] = result[i]
            result[i] = temp
    return cost_sort_Economics,result


def sort_planes_cost_replace(result):
    """
        航班信息按照价格排序(若LLVM编译器报错，则使用Python原生代码运行)
        :param result: 航班信息
        :return:元组，第一项是按照经济舱价格升序，第二项是按照公务舱价格升序
        """
    length = len(result)
    for i in range(length-1):
        index = i
        for j in range(i+1,length):
            if result[index][8] > result[j][8]:
                index = j
        if index != i:
            result[index],result[i] = result[i],result[index]
    cost_sort_Economics = copy.deepcopy(result)
    for i in range(length-1):
        index = i
        for j in range(i+1,length):
            if result[index][9] > result[j][9]:
                index = j
        if index != i:
            result[index],result[i] = result[i],result[index]
    return cost_sort_Economics,result




def sort_planes_time(result: list) -> tuple:#按时间排序
    """
    航班信息按照时间排序
    :param result: 二维数组：航班信息
    :return: 元组，第一项是按照出发时间排序，第二项是按照到达时间排序
    """
    t = [(lambda x:[int(x[0]),int(x[1])])(i[4].split(' ')[1].split(':')[0:2]) for i in result]#建立时间的映像
    for i in range(len(result) - 1):#选择排序
        index = i
        for j in range(i+1, len(result)):
            if t[index][0] > t[j][0] or (t[index][0] == t[j][0] and t[index][1] > t[j][1]):
                index = j
        if index != i:
            t[i],t[index] = t[index],t[i]
            result[i],result[index] = result[index],result[i]
    time_go_sort = copy.deepcopy(result)
    t = [(lambda x:[int(x[0]),int(x[1])])(i[5].split(' ')[1].split(':')[0:2]) for i in result]
    for i in range(len(result) - 1):
        index = i
        for j in range(i+1, len(result)):
            if t[index][0] > t[j][0] or (t[index][0] == t[j][0] and t[index][1] > t[j][1]):
                index = j
        if index != i:
            t[i], t[index] = t[index], t[i]
            result[i], result[index] = result[index], result[i]
    return json.dumps(time_go_sort,ensure_ascii=False),json.dumps(result,ensure_ascii=False)



def select_planes(info: tuple):
    """
    :param info:出发城市，到达城市，出发日期
    :return: 正常情况下返回搜索到的结果，没搜索到返回None，数据库在更新返回False
    """
    acity,bcity, date = info
    result = []
    try:
        # 试图打开城市航班信息文件
        city_excel = pandas.read_pickle('./files/citys/' + acity + '.pickle')
    except:
        # 若打开失败则直接返回
        return False
    a = city_excel.query("到达城市==@bcity")  # 第一轮（城市）筛选后
    # 若未能查找出相关信息，则返回None
    if len(a) == 0:
        return None
    b = [i.split(' ')[0] for i in a['出发时间'].values]
    index = [i for i in range(len(b)) if b[i] == date]  # 第二轮（时间）筛选后,index为符合条件的索引
    if not index or index == []:
        return None
    z = a.iloc[index].values
    for i in range(len(z)):
        # 把筛选后的结果变成Python列表追加到结果列表中
        result.append(numpy.insert(z[i], 0, index[i],axis=0).tolist())
    return result



def judgeDate(adate:str,bdate:str)->bool:
    """
    判断当前出发时间是前一程的到达时间之后至少120分钟
    :param adate:前一程到达时间
    :param bdate: 当前的出发时间
    :return: 判断是否满足要求
    """
    a,b = adate.split(' '),bdate.split(' ')
    if b[0] > a[0]:
        return True
    elif b[0] < a[0]:
        return False
    else:
        if b[1] <= a[1]:
            return False
        else:
            hour = int(a[1].split(':')[0])+2
            other = a[1][2:]
            new = str(hour) + other
            if b[1] >= new:
                return True



class emails_db:
    def __init__(self):
        self.path = './files/emails.pickle'

    def _pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx('./files/emails.xlsx')

    def exist_account(self, account: str):  # 查
        emails = pandas.read_pickle(self.path)
        return [account] in emails.values

    def add_account(self, account: str):  # 增
        try:
            emails = pandas.read_pickle(self.path)
        except:
            time.sleep(3)
            emails = pandas.read_pickle(self.path)
        a = pandas.DataFrame({'email': account}, index=[0])
        pandas.concat([emails, a], axis=0, ignore_index=True).to_pickle(self.path)

    def delete_account(self,account:str): #删
        a = pandas.read_pickle(self.path)
        a.drop(a.query("email==@account").index,inplace=True)
        a.to_pickle(self.path)



    def __str__(self):
        emails = pandas.read_pickle(self.path)
        return (emails)
    def __repr__(self):
        emails = pandas.read_pickle(self.path)
        return (emails.values)



def _delete_email_account(account):
    path = './files/emails.pickle'
    a = pandas.read_pickle(path)
    a.drop(a.query("email==@account").index, inplace=True)
    a.to_pickle(path)



def _check_tasks_pickle():
    with open('./files/tasks.pickle','rb+') as f:
        print(pickle.load(f))


if __name__ == '__main__':
    print(judgeCity('北京'))

