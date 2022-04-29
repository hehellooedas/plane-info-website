import pandas,pickle,threading,multiprocessing,os,random
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor


def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

class emails_db:
    def __init__(self,path):
        self.path = path

    def exist_account(self,account):
        emails = pandas.read_excel(self.path,header=1)
        return False

    def add_account(self,account):
        emails = pandas.read_excel(self.path, header=1)






if __name__ == '__main__':
    #df = pandas.DataFrame({'email':['928309386@qq.com']})
    #df.to_excel('./files/emails.xlsx')
    emails = pandas.read_excel('./files/emails.xlsx')
    print(emails.head())
    emails.loc[0] = ['928309386@qq.com']
    #emails.to_excel('./files/emails.xlsx')
    #d = {'email':'928309386@qq.com'}
    #s = pandas.Series(d)

