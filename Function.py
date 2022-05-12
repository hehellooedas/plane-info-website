import pandas, pickle, threading, multiprocessing, os, random, time, copy,fcntl


def hello():
    print('hello')

def get_date(date_time):
    return date_time.split(' ')[0]


def get_time(date_time):
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


def get_content(company, flight_number, acity, bcity, adate, bdate):
    return f'【民航行程信息】您的机票已于{get_Time()}支付成功。{get_date(adate)} {company} {flight_number}航班' \
           f'经济舱,{acity}（{get_Szm(acity)}） {get_time(adate)} - {bcity}（{get_Szm(bcity)}）' \
           f'{get_time(bdate)}。\n航班将于起飞前45分钟截止办理乘机手续，为避免耽误您的行程，请您预留足够的时间办理乘机手续' \
           f'并提前20分钟抵达登机口。乘机人'


def create_String(n=6):
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
                information['余座'].values[index] -= numbers
                pandas.to_pickle(f'./files/citys/{city}.pickle')
            f.truncate()  # 完成所有task之后，清空这个pickle文件


def sort_planes(result: list) -> tuple:
    for i in range(len(result) - 1):
        for j in range(1, len(result)):
            if result[i][8] > result[j][8]:
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
    cost_sort = copy.deepcopy(result)  # 申请一段内存单独存储排序后的结果
    t = [i[4].split(' ')[1].split(':')[0:2] for i in result]
    for i in t:
        i[0] = int(i[0])
        i[1] = int(i[1])
    for i in range(len(result) - 1):
        for j in range(1, len(result)):
            if t[i][0] > t[j][0] or (t[i][0] == t[j][0] and t[i][1] > t[j][1]):
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
    return (cost_sort, result)


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
        emails = pandas.read_pickle(self.path)
        a = pandas.DataFrame({'email': account}, index=[0])
        pandas.concat([emails, a], axis=0, ignore_index=True).to_pickle(self.path)

    def __str__(self):
        emails = pandas.read_pickle(self.path)
        return (emails)


class planes_db:
    def __init__(self, city):
        self.city = city
        self.path = './files/citys/' + city + '.pickle'

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx(f'./files/citys/{self.city}.xlsx', index=False)

    def select_planes(self, info: tuple) -> list | None:
        bcity, date = info
        result = []
        city_excel = pandas.read_pickle(self.path)
        a = city_excel.query("到达城市==@bcity")  # 第一轮（城市）筛选后
        b = [i.split(' ')[0] for i in a['出发时间'].values]
        index = [i for i in range(len(b)) if b[i] == date]  # 第二轮（时间）筛选后,index为符合条件的索引
        if not index:
            return
        for i in index:
            temp = a.values[i].tolist()
            if temp[-1] > 0:
                temp.insert(0, i)
                result.append(temp)
        return result

