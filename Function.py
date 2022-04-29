import pandas,pickle,threading,multiprocessing,os,random
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

def create_string(n=6):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', n))

def exist_account(account):
    pass