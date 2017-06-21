# -*- coding: utf-8 -*-

from .instatag import *
import time
import os
if __name__=="__main__":
    timer_1=time.perf_counter()
    if "insta_data" not in os.listdir():
        os.mkdir("insta_data")
    tag_list=get_tags()
    p=mu.Pool(mu.cpu_count())
    p.map(user_list_gen,tag_list)
    timer_2=time.perf_counter()
    delta_time=timer_2-timer_1
    print("InstaTag Data Generated In "+time_convert(delta_time))