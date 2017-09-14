# -*- coding: utf-8 -*-

from .instatag import *
import time
import os
import sys
import doctest
import multiprocessing as mu
if __name__=="__main__":
    args=sys.argv
    if len(args)>1:
        if args[1].upper()=="TEST":
            doctest.testfile("test.py",verbose=True)
    else:
        timer_1=time.perf_counter()
        if "insta_data" not in os.listdir():
            os.mkdir("insta_data")
        tag_list=get_tags()
        p=mu.Pool(mu.cpu_count())
        p.map(user_list_gen,tag_list)
        timer_2=time.perf_counter()
        delta_time=timer_2-timer_1
        print("InstaTag Data Generated In "+tisme_convert(delta_time))