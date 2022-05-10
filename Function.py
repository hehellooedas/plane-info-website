import pandas,pickle,threading,multiprocessing,os,random,time

def get_date(date_time):
    return date_time.split(' ')[0]
def get_time(date_time):
    return date_time.split(' ')[1]


def get_Time():
    return time.strftime("%Y-%m-%d",time.localtime())

def get_Szm(city):
    table = {
        '三亚':"SYX",'上海':"SHA","北京": "BJS","南京": "NKG","厦门": "XMN","大连": "DLC","广州": "CAN","成都": "CTU",
        "昆明": "KMG","杭州": "HGH","武汉": "WUH","济南": "TNA",'深圳': 'SZX',"福州": "FOC","郑州": "CGO","西安": "SIA",
        "重庆": "CKG","长沙": "CSX","青岛": "TAO"
    }
    return table.get(city)


def create_string(n=6):
    """
    Generate random string
    :param n:int
    :return:a random string
    """
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))


def set_task(arr):
    if os.path.exists('./files/tasks.pickle'):
        if os.path.getsize('./files/tasks.pickle'):
            with open('./files/tasks.pickle', 'rb+') as f:
                a = pickle.load(f)
                a.append(arr)
                pickle.dump(a,f)
        else:
            with open('./files/tasks.pickle', 'rb+') as f:
                pickle.dump(arr,f)
    else:
        with open('./files/tasks.pickle','wb+') as f:
            pickle.dump(arr,f)



# 航班数据更新函数
def planes_Update_Function():
    if os.path.exists('./files/tasks.pickle') and os.path.getsize('./files/tasks.pickle') != 0:
        with open('./files/tasks.pickle','rb+') as f:
            tasks = pickle.load(f)
            for i in tasks:
                city,index,numbers = i
                information = pandas.read_pickle(f'./files/citys/{city}.pickle')
                information['余座'].values[index] -= numbers
                pandas.to_pickle(f'./files/citys/{city}.pickle')
            f.truncate()



class emails_db:
    def __init__(self):
        self.path = './files/emails.pickle'

    def xlsx_to_pickle(self):
        xlsx = pandas.read_excel(self.path)
        xlsx.to_pickle('./files/emails.pickle')

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx('./files/emails.xlsx')

    def exist_account(self,account): # 查
        emails = pandas.read_pickle(self.path)
        return [account] in emails.values

    def add_account(self,account): # 增
        emails = pandas.read_pickle(self.path)
        a = pandas.DataFrame({'email':account},index=[0])
        pandas.concat([emails,a],axis=0,ignore_index=True).to_pickle(self.path)

    def __str__(self):
        emails = pandas.read_pickle(self.path)
        return (emails)



class planes_db:
    def __init__(self,city):
        self.city = city
        self.path = './files/citys/' + city + '.pickle'

    def xlsx_to_pickle(self):
        xlsx = pandas.read_excel(self.path)
        xlsx.to_pickle(f'./files/citys/{self.city}.pickle')

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx(f'./files/citys/{self.city}.xlsx',index=False)


    def select_planes(self,info:tuple):
        bcity,date = info
        lock = multiprocessing.Lock()
        with lock:
            result = []
            city_excel = pandas.read_pickle(self.path)
            a = city_excel.query("到达城市==@bcity") #第一轮（城市）筛选后
            b = [i.split(' ')[0] for i in a['出发时间'].values]
            index = [i for i in range(len(b)) if b[i] == date] #第二轮（时间）筛选后,index为符合条件的索引
            for i in index:
                temp = a.values[i].tolist()
                temp.insert(0, i)
                result.append(temp)
            return result




