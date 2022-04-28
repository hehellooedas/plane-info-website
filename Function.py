import pandas,pickle,threading,multiprocessing,os,random
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

def create_string():
    return random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6)

def exist_account(account):
    pass