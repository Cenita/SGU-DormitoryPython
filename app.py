from flask import Flask,request
from functools import wraps
from WaterEleAPI import *
import json
import requests
app = Flask(__name__)
data ={
    'status':200,
    'content':""
}


@app.route('/getBase',methods=['POST'])
def base():
    try:
        roomName = request.get_json().get('roomName')
        buildingId = request.get_json().get('buildingId')
    except Exception:
        data['status']=400
        data['content']='请填写房间名和建筑名'
        return json.dumps(data)
    if roomName and buildingId:
        try:
            result = getBaseInformation(buildingId,roomName)
            data['status'] = 200
            data['content']=result
            return json.dumps(data)
        except Exception:
            data['status'] = 400
            data['content'] = '爬虫发生出错请重试或者联系管理者解决'
            return json.dumps(data)
    else:
        data['status']=400
        data['content']='请填写房间名和建筑名'
        return json.dumps(data)

@app.route('/check/<type>',methods=['POST'])
def check(type):
    infor = request.get_json()
    data = {}
    if infor == None:
        data['status'] = 400
        data['content'] = '请填写房间名和建筑名'
        return json.dumps(data)
    roomName = infor.get('roomName')
    buildingId = infor.get('buildingId')
    start_time = infor.get('start_time')
    end_time = infor.get('end_time')
    if roomName and buildingId:
        if start_time and end_time:
            if type:
                if type=='eleCharge':
                    pageName = 'findFillLogDelView'
                elif type=='waterCharge':
                    pageName = 'findFillLogWaterView'
                elif type=='eleUsed':
                    pageName = 'findUsedQuantityDelEleView'
                elif type=='waterUsed':
                    pageName = 'findUsedQuantityWaterView'
                try:
                    result = checkDate(buildingId,roomName,pageName,start_time,end_time)
                    data['status']=200
                    data['content']=result
                    return json.dumps(data)
                except Exception:
                    data['status'] = 400
                    data['content'] = '爬虫发生出错请重试或者联系管理者解决'
                    return json.dumps(data)
            else:
                data['status'] = 400
                data['content'] = '请填写类型'
                return json.dumps(data)
        else:
            data['status'] = 400
            data['content'] = '请填写开始时间和结束时间'
            return json.dumps(data)
    else:
        data['status'] = 400
        data['content'] = '请填写房间名和建筑名'
        return json.dumps(data)



if __name__ == '__main__':
    app.run(port=2223,host='0.0.0.0')
