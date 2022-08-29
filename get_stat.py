import urllib
import json
import glob
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

resp_text = urllib.request.urlopen('https://xn--d1aqf.xn--p1ai/ajax/itm_weekly_report.php').read().decode('UTF-8')
json_obj = json.loads(resp_text)

dates = json_obj['dates'][::-1]
creditors = json_obj['creditors']
regions = json_obj['regions']

mainResults=[0, 0, 0, 0, 0, 0, 0]
estates=[]
amountOfLoans=[]

creditorsResults = {}
for creditor in creditors:
    creditorsResults[creditor] =  [0, 0, 0, 0, 0, 0, 0]

regionsResults ={}
for region in regions:
    regionsResults[region] =  [0, 0, 0, 0, 0, 0, 0]

for date in dates:
    resp_text = urllib.request.urlopen('https://xn--d1aqf.xn--p1ai/ajax/itm_weekly_report.php?reportType=creditor&date=' + date).read().decode('UTF-8')
    json_obj_creditors = json.loads(resp_text)
    resp_text = urllib.request.urlopen('https://xn--d1aqf.xn--p1ai/ajax/itm_weekly_report.php?reportType=region&date=' + date).read().decode('UTF-8')
    json_obj_regions = json.loads(resp_text)
    # собираем общие данные для итоговых значений
    tmp = [x.replace(" ", "").replace(",",".") for x in json_obj_creditors['data'][0]] 
    mainResults=[ mainResults[0] + int(tmp[2]),
                  mainResults[1] + int(tmp[3]),
                  mainResults[2] + int(tmp[4]),
                  mainResults[3] + int(tmp[5]),
                  mainResults[4] + float(tmp[6]), 
                  mainResults[5] + int(tmp[7]),
                  mainResults[6] + float(tmp[8])]
    # считаем количество выданных ипотек за неделю 
    estates.append(int(tmp[7]))
    # считаем сумму выданных ипотек за неделю 
    amountOfLoans.append(float(tmp[8]))
    
    # собираем данные по банкам 
    for dat in json_obj_creditors['data']:
        if dat[0]!='Итого' and dat[1] == '':
            old = creditorsResults[dat[0]]
            new = [x.replace(" ", "").replace(",",".") for x in dat]
            creditorsResults[dat[0]] = [old[0] + int(new[2]),
                                        old[1] + int(new[3]),
                                        old[2] + int(new[4]),
                                        old[3] + int(new[5]),
                                        old[4] + float(new[6]), 
                                        old[5] + int(new[7]),
                                        old[6] + float(new[8])]
    
    # собираем данные по регионам 
    for dat in json_obj_regions['data']:
        if dat[0]!='Итого' and dat[1] == '':
            old = regionsResults[dat[0]]
            new = [x.replace(" ", "").replace(",",".") for x in dat]
            regionsResults[dat[0]] = [old[0] + int(new[2]),
                                        old[1] + int(new[3]),
                                        old[2] + int(new[4]),
                                        old[3] + int(new[5]),
                                        old[4] + float(new[6]), 
                                        old[5] + int(new[7]),
                                        old[6] + float(new[8])]
print(creditorsResults)
print()
print(regionsResults)
print()

headers = [x.replace(" ", "\r") for x in json_obj_regions['header']['main']]    
headers.pop(0) # Убираем лишние хидера
headers.pop(0)
print(tabulate([mainResults], headers=headers)) # выводим таблицу



# выводим таблицу по банкам
headers.insert(0, "Банк")
final = []
for key, value in creditorsResults.items():
    value.insert(0, key)

print(tabulate(sorted(creditorsResults.values(), key = lambda x: float(x[7]),
                      reverse=True), headers=headers)) 


# выводим таблицу по регионам
headers[0]='Регион'
final = []
for key, value in regionsResults.items():
    value.insert(0, key)

print(tabulate(sorted(regionsResults.values(), key = lambda x: float(x[7]),
                      reverse=True), headers=headers)) 


plt.figure(figsize=(10,10), dpi=120)
plt.bar(dates, estates)
#plt.title('Количество выданных кредитов по неделям')
plt.xlabel('Неделя', fontsize=10)
plt.ylabel('Количество выданных кредитов, шт.', fontsize=10)
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,10), dpi=120)
plt.bar(dates, amountOfLoans)
#plt.title('Сумма выданных кредитов по неделям')
plt.xlabel('Неделя', fontsize=10)
plt.ylabel('Сумма, млн.руб.', fontsize=10)
plt.xticks(rotation=45)
plt.show()

displayDict = {}
for k, v in creditorsResults.items(): 
    displayDict[k]=v[6]
displayDict = dict(sorted(displayDict.items(), key=lambda item: item[1], reverse=True))
plt.figure(figsize=(22,10), dpi=120)
plt.bar(displayDict.keys(), displayDict.values())
#plt.title('Сумма выданных кредитов по банкам')
plt.xlabel('Банк', fontsize=10)
plt.ylabel('Сумма, млн.руб.', fontsize=10)
plt.xticks(rotation=90, fontsize=10)
plt.show()

displayDict = {}
for k, v in creditorsResults.items(): 
    displayDict[k]=v[5]
displayDict = dict(sorted(displayDict.items(), key=lambda item: item[1], reverse=True))
plt.figure(figsize=(22,10), dpi=120)
plt.bar(displayDict.keys(), displayDict.values())
#plt.title('Количество выданных кредитов по банкам')
plt.xlabel('Банк', fontsize=10)
plt.ylabel('Количество, шт.', fontsize=10)
plt.xticks(rotation=90, fontsize=10)
plt.show()


displayDict = {}
for k, v in regionsResults.items(): 
    displayDict[k]=v[6]
displayDict = dict(sorted(displayDict.items(), key=lambda item: item[1], reverse=True))
plt.figure(figsize=(22,10), dpi=120)
plt.bar(displayDict.keys(), displayDict.values())
#plt.title('Сумма выданных кредитов по регионам')
plt.xlabel('Регион', fontsize=10)
plt.ylabel('Сумма, млн.руб.', fontsize=10)
plt.xticks(rotation=90, fontsize=10)
plt.show()

displayDict = {}
for k, v in regionsResults.items(): 
    displayDict[k]=v[5]
displayDict = dict(sorted(displayDict.items(), key=lambda item: item[1], reverse=True))
plt.figure(figsize=(22,10), dpi=120)
plt.bar(displayDict.keys(), displayDict.values())
#plt.title('Количество выданных кредитов по регионам')
plt.xlabel('Регион', fontsize=10)
plt.ylabel('Количество, шт.', fontsize=10)
plt.xticks(rotation=90, fontsize=10)
plt.show()
