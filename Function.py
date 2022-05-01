import pandas,pickle,threading,multiprocessing,os,random


def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

class emails_db:
    def __init__(self,path):
        self.path = path

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
        pandas.concat([emails,a],axis=0,ignore_index=True).to_excel(self.path,index=False)

    def __str__(self):
        emails = pandas.read_pickle(self.path)
        return (emails)



class planes_db:
    def __init__(self,path):
        self.path = path

    def xlsx_to_pickle(self):
        xlsx = pandas.read_excel(self.path)
        xlsx.to_pickle('./files/planes.pickle')

    def pickle_to_xlsx(self):
        pickle = pandas.read_pickle(self.path)
        pickle.to_xlsx('./files/planes.xlsx')

    def change_planes(self,n):
        pass

    def select_planes(self):
        pass






if __name__ == '__main__':
    a = pandas.read_excel('./files/planes.xlsx')
    a.to_pickle('./files/planes.pickle')

