# -*- coding: utf-8 -*-

import requests
import time
import socket
import io
from bs4 import BeautifulSoup
from random import randint
import multiprocessing as mu
import os
import sys
DEBUG=True

def tag_url_maker(tag):
    return "http://www.instagram.com/explore/tags/"+tag
def post_url_maker(post_hash):
    return "https://www.instagram.com/p/"+post_hash

def step_2_url_maker(name):
    return "http://www.instagram.com/"+name+"/media/"
def print_line(number=30,char="-"):
    '''
    This function print line in screen
    :param number: number of items in each line
    :param char: each char of line
    :return: None
    '''
    line=""
    for i in range(number):
        line=line+char
    print(line)


def zero_insert(input_string):
    '''
    This function get a string as input if input is one digit add a zero
    :param input_string: input digit az string
    :type input_string:str
    :return: modified output as str
    '''
    if len(input_string)==1:
        return "0"+input_string
    return input_string

def time_convert(input_data):
    '''
    This function convert input_sec  from sec to DD,HH,MM,SS Format
    :param input_data: input time
    :type input_data:int
    :return: converted time as string
    '''
    input_sec=input_data
    input_minute=input_sec//60
    input_sec=int(input_sec-input_minute*60)
    input_hour=input_minute//60
    input_minute=int(input_minute-input_hour*60)
    input_day=int(input_hour//24)
    input_hour=int(input_hour-input_day*24)
    return zero_insert(str(input_day))+" days, "+zero_insert(str(input_hour))+" hour, "+zero_insert(str(input_minute))+" minutes, "+zero_insert(str(input_sec))+" seconds"

def get_html(url,max_delay=15):
    '''
    This function extract raw_html file
    :param url: url
    :type url:str
    :return: html data
    '''
    time.sleep(create_random_sleep(max_time=max_delay))
    if internet()==True:
        new_session=requests.session()
        new_session.cookies.clear()
        raw_html=new_session.get(url)
        new_session.close()
        raw_data=raw_html.text
        if "No posts yet." in raw_data:
            print("Invalid Tag")
            sys.exit()
        return raw_data
    else:
        print("Error In Internet")
        pass

def internet(host="8.8.8.8", port=53, timeout=50):
    """
    Check Internet Connections.
    :param  host: the host that check connection to
    :param  port: port that check connection with
    :param  timeout: times that check the connnection
    :type host:str
    :type port:int
    :type timeout:int
    :return bool: True if Connection is Stable
    >>> internet() # if there is stable internet connection
    True
    >>> internet() # if there is no stable internet connection
    False
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False
def create_random_sleep(index=1,min_time=5,max_time=60):
    '''
    This function generate sleep time with random processes
    :param index: index to determine first page  and messages(index = 0 is for first page)
    :param min_time: minimum time of sleep
    :param max_time: maximum time of sleep
    :type index:int
    :type min_time:int
    :type max_time:int
    :return: time of sleep as integer (a number between max and min)
    '''
    if index==0:
        time_sleep = 5
        if DEBUG==True:
            print("Wait "+str(time_sleep)+" sec for first search . . .")
    else:
        time_sleep = randint(min_time, max_time)
        if DEBUG==True:
            print("Wait "+str(time_sleep)+" sec for next search . . .")
    if DEBUG==True:
        print_line(70,"*")
    return time_sleep

def post_list_gen(tag,index=0):
    '''
    This function extract instagram post_link
    :param tag: hashtag
    :param index: index for resume search
    :type tag:str
    :type index:int
    :return: post links as a list
    '''
    try:
        print("Page Extracting . . .")
        post_list = []
        tag_url = tag_url_maker(tag)
        raw_file = get_html(tag_url)
        while(index!=-1):
            index=raw_file.find('"code":',index+7,len(raw_file))
            length=raw_file[index:].find(',')
            post=raw_file[index+9:index+length-1]
            if len(post)<50:
                post_list.append(post)
        return post_list
    except Exception as ex:
        return post_list

def step_2_gen(name_list,tag):
    '''
    This function extract 2nd users (from 1st users follower and following list)
    :param name_list: 1st users id
    :param tag: hashtag
    :type name:list
    :type tag:str
    :return: None
    '''
    try:
        file=io.open("insta_data/users_2_"+tag+".txt","a",encoding="utf-8")
        user_list=[]
        for i in range(len(name_list)):
            print("ID : "+name_list[i])
            user_url=step_2_url_maker(name_list[i])
            raw_html=get_html(user_url,max_delay=8)
            raw_file = BeautifulSoup(raw_html, "html.parser").prettify()
            if raw_file.find('"more_available": false')!=-1:
                print("Account is private")
                continue
            index=0
            while (index != -1):
                index = raw_file.find('"username":', index + 13, len(raw_file))
                length = raw_file[index:].find('}')
                user = raw_file[index + 13:index + length - 1]
                if user[-1] == '"':
                    user = user[:-1]
                user = user.encode("utf-8")
                if len(user) < 50 and user not in user_list and user!=name_list[i]:
                    file.write(str(user, encoding="utf-8") + "\n")
                    user_list.append(user)
            print(str(len(user_list))+" ID Extracted")
    except Exception as ex:
        print(str(ex))



def user_list_gen(tag):
    '''
    This function extract user_list for each tag in first step and then run step_2_gen for second users
    :param tag: hastag
    :type tag:str
    :return: None
    '''
    try:
        hash_list = post_list_gen(tag)
        file=io.open("insta_data/users_1_"+tag+".txt","a",encoding="utf-8")
        user_list=[]
        for i in range(len(hash_list)):
            print("Code : "+hash_list[i])
            user_url = post_url_maker(hash_list[i])
            raw_html = get_html(user_url)
            raw_file=BeautifulSoup(raw_html,"html.parser").prettify()
            index = 0
            while(index!=-1):
                index=raw_file.find('"username":',index+13,len(raw_file))
                length=raw_file[index:].find('}')
                user=raw_file[index+13:index+length-1]
                if user[-1]=='"':
                    user=user[:-1]
                if len(user)<50 and (user not in user_list):
                    user_list.append(user)
                    user = user.encode("utf-8")
                    file.write(str(user,encoding="utf-8")+"\n")

        step_2_gen(user_list,tag)
        file.close()
    except Exception as ex:
        print(str(ex))
        step_2_gen(user_list, tag)

def get_tags():
    '''
    This function read tags from a comma seperated file (tags.tf)
    :return: Tags as a list
    '''
    try:
        if "tags.tf" in os.listdir():
            file=io.open("tags.tf","r",encoding="utf-8")
            contain=file.read()
            return contain.split(",")
        else:
            print("No Tag")
            sys.exit()
    except Exception as e:
        print("Error In Tags")
        sys.exit()

