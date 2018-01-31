#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 00:50:14 2018

@author: python
"""

import sys

def tax_cal(num,salary):
    tax_money = salary*(1-0.165)-3500
    if tax_money<0:
        tax=0
    elif 0<=tax_money<=1500:
        tax = tax_money*0.03
    elif 1500<tax_money<=4500:
        tax = tax_money*0.1-105
    elif 4500<tax_money<=9500:
        tax = tax_money*0.2-555
    elif 9000<tax_money<=35000:
        tax = tax_money*0.25-1005            
    elif 35000<tax_money<=55000:
        tax = tax_money*0.3-2755
    elif 55000<tax_money<=80000:
        tax = tax_money*0.35-5505            
    elif 80000<tax_money:
        tax = tax_money*0.45
    after_salary = salary*(1-0.165)-tax
    print('{}:{:.2f}'.format(num,after_salary))

if len(sys.argv)==1:
    print("Parameter Error")
else:
    for para in sys.argv[1:]:
        try:            
            num = int(para.split(':')[0])
            salary = int(para.split(':')[1])
        except:
            print("Parameter Error")
        else:
            tax_cal(num,salary)
            

            
    