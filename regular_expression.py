#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd
import pprint
import csv


# In[389]:


with open(r'D:\\phonebook_raw.csv', encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
    
    
def get_info(contact_list):    
    new_contact = []
    for contact in contact_list:
        full_name = ",".join(contact[:3])
        result = re.sub(r'[\s]',',', full_name)
        new_contact.append(result)

    data = pd.DataFrame(new_contact)
    data1 = data[0].str.split(',',expand=True).copy()
    headers = data1.iloc[0]
    data1 = data1[1:]
    data1.columns = headers
    data1 = data1.iloc[:, :-2]


    new_info = []
    for contact in contact_list:
        full_info = ",".join(contact[3:])
        new_info.append(full_info)

    data_inf = pd.DataFrame(new_info)
    data1_inf = data_inf[0].str.split(',',expand=True).copy()
    headers_inf = data1_inf.iloc[0]
    data1_inf = data1_inf[1:]
    data1_inf.columns = headers_inf
    data1_inf = data1_inf.iloc[:, :-1]
    
    data_common = pd.concat([data1, data1_inf], axis = 1)
    sub_phone = r'+7(\3)\6-\8-\10 \12\13'
    phone_pattern = '(8|\+7)\s*(\(*)([0-9]{3})(\)*)(\s*|\-*)([0-9]{3})(\s*|\-*)([0-9]{2})(\s*|\-*)([0-9]{2})\s*(\(*)([а-я]{3}\.)*\s*(\d{4})*(\))*'
    norm_numbers = []
    for ph in list(data_common['phone']):
        phone_pattern = re.compile(phone_pattern)
        changed_phone = phone_pattern.sub(sub_phone, ph)
        norm_numbers.append(changed_phone)    
        data_phone = pd.DataFrame({'phone':norm_numbers})
        
    del data_common['phone']
    data_common = data_common.reset_index(drop=True)
    
    data_common1 = pd.concat([data_common, data_phone], axis = 1)
    
    return data_common1



def unioin_data(data_common1):
    data_new = data_common1.groupby('lastname').max().reset_index()
    return data_new


def write_data(data_new):
    with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data_new)


# In[ ]:




