import pandas,pickle,threading,multiprocessing,os,random



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
            with open('./files/tasks.pickle', 'ab+') as f:
                pass
        else:
            with open('./files/tasks.pickle', 'ab+') as f:
                pass


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


    def select_planes(self,bcity,date):
        lock = multiprocessing.Lock()
        with lock:
            result,index = [],[]
            city_excel = pandas.read_pickle(self.path)
            a = city_excel.query("到达城市==@bcity") #第一轮（城市）筛选后
            b = [i.split(' ') for i in a['出发时间'].values]
            c = [i for i in range(len(b)) if b[i][0] == date] #第二轮（时间）筛选后
            for i in range(len(c)):
                if c[i][0] == '2022-12-21':
                    index.append(i) #index 为索引列表
            for i in index:
                temp = a.values[i].tolist()
                temp.insert(0, i)
                result.append(temp)
            return result






