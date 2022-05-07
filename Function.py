import pandas,pickle,threading,multiprocessing,os,random


def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

# 航班数据更新函数
def planes_Update_Function():
    print('ok')


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
    def __init__(self,path):
        self.path = './files/citys/' + path + '.xlsx'

    def xlsx_to_pickle(self):
        xlsx = pandas.read_excel(self.path)
        xlsx.to_pickle('./files/planes.pickle')

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx('./files/planes.xlsx')


    def select_planes(self):
        pass






