import pandas,pickle,threading,multiprocessing,os,random
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor


def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

class emails_db:
    def __init__(self,path):
        self.path = path

    def exist_account(self,account): # 查
        emails = pandas.read_excel(self.path,header=1)
        return False

    def add_account(self,account): # 增
        emails = pandas.read_excel(self.path, header=1)


class planes:
    def __init__(self,path):
        self.path = path





if __name__ == '__main__':
    #a = pandas.DataFrame({'email':'928309386@qq.com'},index=[1])
    #a.to_excel('./files/emails.xlsx')
    a = pandas.read_excel('./files/emails.xlsx')
    a.loc[3] = ['888888888@qq.com']
    a.loc[4] = ['11111111@qq.com']
    a.to_excel('./files/emails.xlsx')
