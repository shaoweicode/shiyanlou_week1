#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:43:50 2018

@author: python
"""

import sys
import csv # 用于写入 csv 文件

from multiprocessing import Process, Queue

import time
# 处理命令行参数类
class Args(object):

    def __init__(self):
        self.args = sys.argv[1:]
        
    def get_path(self):
        path_data = self.args
        try:
            c_path = path_data[path_data.index('-c')+1]
            d_path = path_data[path_data.index('-d')+1]
            o_path = path_data[path_data.index('-o')+1]
        except:
            print("Parameter Error")
        else:
            return [c_path,d_path,o_path] 
# 配置文件类
class Config():

    def __init__(self):
        self.config = self._read_config()
        

    # 配置文件读取内部函数
    def _read_config(self):
        config = {}
        sys_parameters_c = Args()
        config_path =sys_parameters_c.get_path()[0]
        try:
            cfg_file = open(config_path)            
        except:
            raise FileNotFoundError
        else:
            try:
                for line in cfg_file:
                    msg = line.split('=')                
                    config[msg[0].strip()]=float(msg[1].strip())            
                cfg_file.close()
                return config
            except:
                raise TypeError
    
    def get_config(self,item):
        return self.config[item]
          
        """
        补充代码：
        1. 根据参数指定的配置文件路径，读取配置文件信息，并写入到 config 字典中.
        2. 使用 strip() 和 split() 对读取到的配置文件去掉空格以及切分.
        3. 当格式出错时，抛出异常.
        """
# 用户数据类
class UserData(object):

#    def __init__(self):
#        self.userdata = self._read_users_data(queue_1)

    # 用户数据读取内部函数
    def _read_users_data(self,queue_1):
        userdata = []
        sys_parameters_u = Args()
        path =sys_parameters_u.get_path()[1]        
        try:
            file = open (path)
        except:
            raise FileNotFoundError
        else:
            try:
                for row in csv.reader(file):
                    one_piece = [int(row[0]),int(row[1])]
#                    print(one_piece)
                    queue_1.put(one_piece)
                    time.sleep(0.01)
                file.close()
#                return userdata
            except:
                raise TypeError
                
# 税后工资计算类
class IncomeTaxCalculator(object):
    
    def tax(self,tax_money):
        if tax_money<0:
            tax=0
        elif 0<=tax_money<=1500:
            tax = tax_money*0.03
        elif 1500<tax_money<=4500:
            tax = tax_money*0.1-105
        elif 4500<tax_money<=9000:
            tax = tax_money*0.2-555
        elif 9000<tax_money<=35000:
            tax = tax_money*0.25-1005                       
        elif 35000<tax_money<=55000:
            tax = tax_money*0.3-2755
        elif 55000<tax_money<=80000:
            tax = tax_money*0.35-5505            
        elif 80000<tax_money:
            tax = tax_money*0.45-13505
        return tax

    # 计算每位员工的税后工资函数
    def calc_for_all_userdata(self,queue_1,queue_2):
        shuihou_gongzi=[]
        #peizhi wenjian xinxi 
        config_data = Config()
        L_threshold = config_data.get_config('JiShuL')
        H_threshold = config_data.get_config('JiShuH')
        rate = config_data.get_config('YangLao')+\
        config_data.get_config('YiLiao')+config_data.get_config('GongShang')+\
        config_data.get_config('ShiYe')+config_data.get_config('ShengYu')+\
        config_data.get_config('GongJiJin')

        #gongzi xinxi
#        user = UserData()
#        user_salary = user.userdata

#        for item in user_salary:
        while (not(queue_1.empty())):
            num_money = queue_1.get()

            money = num_money[1]
            if money < L_threshold:
                shebao = L_threshold*rate
#                tax_money = money-shebao-3500
#                tax = self.tax(tax_money)
#                money_get = money-shebao-tax
            elif money > H_threshold:                
                shebao = H_threshold*rate
#                tax_money = money-shebao-3500                
#                tax = self.tax(tax_money)
#                money_get = money-shebao-tax
            else:
                shebao = money*rate
            tax_money = money-shebao-3500
            tax = self.tax(tax_money)
            money_get = money-shebao-tax

            num_and_salary = ['{}'.format(num_money[0]),'{}'.format(money),'{:.2f}'.format(shebao),'{:.2f}'.format(tax),'{:.2f}'.format(money_get)]            
#            num_and_salary = [item[0],money,shebao,tax,money_get]
#            shuihou_gongzi.append(num_and_salary)
            print(num_and_salary)
            queue_2.put(num_and_salary)
            
            time.sleep(0.01)
#        return shuihou_gongzi
        
        
        
        
        """
        补充代码：
        1. 计算每位员工的税后工资（扣减个税和社保）.
        2. 注意社保基数的判断.
        3. 将每位员工的税后工资按指定格式返回.
        """

    # 输出 CSV 文件函数
    def export(self,queue_2):
#        result = self.calc_for_all_userdata()
        while (not(queue_2.empty())):
            result = queue_2.get()
            print(result)
            sys_parameters_i = Args()
            path =sys_parameters_i.get_path()[2]         
            with open(path,'w') as f:
                writer = csv.writer(f)
                writer.writerows(result)        
#        print(result)


            


if __name__ == '__main__':
    
    queue1 = Queue()
    queue2 = Queue()
    Userdata = UserData()
    Income = IncomeTaxCalculator()
    
    process1 = Process(target = Userdata._read_users_data(queue1),args=(queue1,))
    process2 = Process(target = Income.calc_for_all_userdata(queue1,queue2),args = (queue1,queue2))
    process3 = Process(target = Income.export(queue2),args = (queue2,))
    
    
    
    process1.start()
    process2.start()
    process3.start()
    
    process1.join()
    process2.join()
    process3.join()   
    process2.terminate()
    process3.terminate()
    

# %run multi_cal.py -c /home/python/shiyanlou_week1/config.cfg -d /home/python/shiyanlou_week1/user.csv -o /home/python/shiyanlou_week1/gongzi.csv

