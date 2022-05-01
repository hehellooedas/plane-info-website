import pandas,pickle,threading,multiprocessing,os,random
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor


def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

class emails_db:
    def __init__(self,path):
        self.path = path

    def exist_account(self,account): # 查
        emails = pandas.read_excel(self.path)
        return [account] in emails.values

    def add_account(self,account): # 增
        emails = pandas.read_excel(self.path)
        a = pandas.DataFrame({'email':account},index=[0])
        pandas.concat([emails,a],axis=0,ignore_index=True).to_excel(self.path,index=False)


class planes:
    def __init__(self,path):
        self.path = path





if __name__ == '__main__':
    #a = pandas.DataFrame({'email':'928309386@qq.com'},index=[1])
    #a.to_excel('./files/emails.xlsx',index=False)
    a = pandas.read_excel('./files/emails.xlsx')
    x = '928309386@qq.com'
    print([x] in a.values)
    row_num = len(a.index.values)
    print(row_num)

