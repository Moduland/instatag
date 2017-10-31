# -*- coding: utf-8 -*-

from .instatag import *
import time
import os
import sys
import doctest
import multiprocessing as mu
tag_list=[]
if __name__=="__main__":
    args=sys.argv
    if len(args)>1:
        if args[1].upper()=="HELP":
            instatag_help()
            sys.exit()
        elif args[1].upper()=="TEST":
            doctest.testfile("test.py",verbose=True)
            sys.exit()
        if len(args) > 2:
            if args[1].upper()=="INPUT":
                tag_list=list(args[2].split(","))
            elif args[1].upper()=="FILE":
                tag_list=get_tags(args[2])
    timer_1=time.time()
    if "insta_data" not in os.listdir():
        os.mkdir("insta_data")
    if len(tag_list)==0:
        tag_list=get_tags()
    p=mu.Pool(mu.cpu_count())
    p.map(user_list_gen,tag_list)
    timer_2=time.time()
    delta_time=int(timer_2-timer_1)
    print("InstaTag Data Generated In "+time_convert(delta_time))