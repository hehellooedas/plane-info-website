import pandas, pickle, os, random, time, copy,numpy,threading,numba,json


def delete_log_byhand():
    os.remove('./files/logs/flask.log')

def get_date(date_time:str)->str:
    return date_time.split(' ')[0]


def get_time(date_time:str)->str:
    return date_time.split(' ')[1]


def get_Time():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_Szm(city: str) -> str:
    table = {
        '三亚': "SYX", '上海': "SHA", "北京": "BJS", "南京": "NKG", "厦门": "XMN", "大连": "DLC", "广州": "CAN", "成都": "CTU",
        "昆明": "KMG", "杭州": "HGH", "武汉": "WUH", "济南": "TNA", '深圳': 'SZX', "福州": "FOC", "郑州": "CGO", "西安": "SIA",
        "重庆": "CKG", "长沙": "CSX", "青岛": "TAO"
    }
    return table.get(city)


def get_content(company, flight_number, acity, bcity, adate, bdate)->str:
    return f'【民航行程信息】您的机票已于{get_Time()}支付成功。{get_date(adate)} {company} {flight_number}航班' \
           f'经济舱,{acity}（{get_Szm(acity)}） {get_time(adate)} - {bcity}（{get_Szm(bcity)}）' \
           f'{get_time(bdate)}。\n航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续' \
           f'并提前20分钟抵达登机口。乘机人'


def create_String(n=6)->str:
    """
    Generate random string
    :param n:int
    :return:a random string
    """
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))


def set_task(arr: list):
    if os.path.exists('./files/tasks.pickle'):
        if os.path.getsize('./files/tasks.pickle'):
            with open('./files/tasks.pickle', 'rb+') as f:
                a = pickle.load(f)
                a.append(arr)
                pickle.dump(a, f)
        else:
            with open('./files/tasks.pickle', 'rb+') as f:
                pickle.dump(arr, f)
    else:
        with open('./files/tasks.pickle', 'wb+') as f:
            pickle.dump(arr, f)



# 航班数据更新函数
def planes_Update_Function():
    if os.path.exists('./files/tasks.pickle') and os.path.getsize('./files/tasks.pickle') != 0:
        with open('./files/tasks.pickle', 'rb+') as f:
            tasks = pickle.load(f)
            for i in tasks:
                city, index, numbers = i
                information = pandas.read_pickle(f'./files/citys/{city}.pickle')
                information['余座'].values[index] -= numbers#航班余座减少
                pandas.to_pickle(f'./files/citys/{city}.pickle')
            f.truncate()  # 完成所有task之后，清空这个写有任务的pickle文件


@numba.jit(nopython=True,cache=True,nogil=True)#采用numba的LLVM编译器编译优化排序算法
def sort_planes_cost(result)->tuple:#按价格升序
    for i in range(len(result) - 1):
        index = i
        for j in range(i+1, len(result)):
            if result[index][8] > result[j][8]:
                index = j
        if index != i:
            temp = numpy.copy(result[index])
            result[i] = result[index]
            result[index] = temp
    cost_sort_Economics = numpy.copy(result)  # 申请一段内存单独存储排序后的结果
    for i in range(len(result) - 1):
        index = i
        for j in range(i+1, len(result)):
            if result[index][9] > result[j][9]:
                index = j
        if index != i:
            temp = numpy.copy(result[index])
            result[i] = result[index]
            result[index] = temp
    return cost_sort_Economics,result




def sort_planes_time(result: list) -> tuple:#按时间排序
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
        city_excel = pandas.read_pickle('./files/citys/' + acity + '.pickle')
    except:
        return False
    a = city_excel.query("到达城市==@bcity")  # 第一轮（城市）筛选后
    if len(a) == 0:
        return None
    b = [i.split(' ')[0] for i in a['出发时间'].values]
    index = [i for i in range(len(b)) if b[i] == date]  # 第二轮（时间）筛选后,index为符合条件的索引
    if not index or index == []:
        return None
    z = a.iloc[index].values
    for i in range(len(z)):
        result.append(numpy.insert(z[i], 0, index[i],axis=0).tolist())
    return result


def select_plane():
    ...



class emails_db:
    def __init__(self):
        self.path = './files/emails.pickle'

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx('./files/emails.xlsx')

    def exist_account(self, account: str):  # 查
        emails = pandas.read_pickle(self.path)
        return [account] in emails.values

    def add_account(self, account: str):  # 增
        lock = threading.Lock()
        with lock:
            try:
                emails = pandas.read_pickle(self.path)
            except:
                time.sleep(3)
                emails = pandas.read_pickle(self.path)
            a = pandas.DataFrame({'email': account}, index=[0])
            pandas.concat([emails, a], axis=0, ignore_index=True).to_pickle(self.path)

    def delete_account(self,account:str): #删
        lock = threading.Lock()
        with lock:
            a = pandas.read_pickle(self.path)
            a.drop(a.query("email==@bcity").index,inplace=True)
            a.to_pickle(self.path)


    def __str__(self):
        emails = pandas.read_pickle(self.path)
        return (emails)
    def __repr__(self):
        emails = pandas.read_pickle(self.path)
        return (emails.values)



if __name__ == '__main__':
    delete_log_byhand()

