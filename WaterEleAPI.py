from bs4 import BeautifulSoup
import re
import requests
import random

def realizeDiv(html,divname,eleName='div'):
    soup = BeautifulSoup(html, features='lxml')
    rechange = soup.find(eleName, id=divname).find('tbody',attrs={'class':"tableBody"}).findAll('tr')
    rechange_list = []
    for i in rechange:
        re_list = []
        for j in i.findAll('td'):
            re_list.append(j.get_text().strip())
        rechange_list.append(re_list)
    return rechange_list

def loginPage(buID,rname):
    ss = requests.session()
    data = {
        "buildingId": buID,
        "roomName": rname,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    ss.post("http://210.38.192.120:8080/sdms-select/webSelect/roomFillLogView.do", data=data)
    return ss



def getBaseInformation(buID,rname):
    ss = loginPage(buID,rname)
    html = ss.get("http://210.38.192.120:8080/sdms-select/webSelect/welcome2.jsp").text
    # 充值
    rechange = realizeDiv(html, "fillDiv")
    # 水费使用情况
    water = realizeDiv(html, "usedWaterDiv")
    # 电费使用情况
    ele = realizeDiv(html, 'usedEleDiv')

    total = {
        "rechange_record": rechange,
        "water": water,
        "ele": ele
    }
    return total



def checkDate(buID,rname,pageName,start_time,end_time):
    ss = loginPage(buID,rname)
    data = {
        "beginTime":start_time,
        "endTime":end_time,
        "ec_crd":100,
        "ec_p":1
    }
    html = ss.get("http://210.38.192.120:8080/sdms-select/webSelect/{}.do?beginTime={}&endTime={}&ec_crd=100&ec_p=1".format(pageName,start_time,end_time)).text
    return realizeDiv(html,'ec_table',eleName='table')