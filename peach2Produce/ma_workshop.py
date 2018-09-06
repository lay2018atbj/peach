# -*- coding:utf-8 -*-
from app import application
from flask import url_for, render_template, request,redirect
import json
from datamodels import CollectedDatas, CollectedDataSeria
from models import RobotInfo, AgvPos
import datetime
import time

@application.route('/ma_workshorp/overview')
def ma_workshop_overview():
    if ("workplace_id" in request.args):
        workplace_id = request.args["workplace_id"]
    else:
        workplace_id = 1
    robotModels = RobotInfo.query.filter_by(factoryId=workplace_id).all()
    return render_template('manage/workshopoverview.html', titlename='车间视图', robotModels=robotModels)


@application.route('/ma_workshop/dataview/<int:id>')
def ma_workshop_dataview(id):
    data = CollectedDatas.query.filter_by(devid=application.config['DEVICES'][id]['uniqueid']).limit(1000).all()
    vdatas = []
    edatas = []
    tdatas = []
    for col in data[::-1]:
        vdatas.append([time.mktime(col.time.timetuple())*1000, col.voltage])
        edatas.append([time.mktime(col.time.timetuple())*1000, col.electricity])
        tdatas.append([time.mktime(col.time.timetuple())*1000, col.temperature])
    data = dict()
    data['v'] = vdatas
    data['e'] = edatas
    data['t'] = tdatas
    return render_template('manage/workshopdataview.html', titlename='数据视图', id=id, thousandData=data)


@application.route('/ma_workshop/getCollectedDatas/<int:id>')
def ma_workshop_getCollectedDatas(id):
    # devid是一个16位的标识符 不是在config的id
    data = None
    if id in application.config['DEVICES'] and application.config['DEVICES'][id]['status'] == 'normal':
        data = CollectedDatas.query.filter_by(devid=application.config['DEVICES'][id]['uniqueid']).first()
    if not data:
        data = CollectedDatas(datetime.datetime.now(), 1, 0, 0, 0)
    return json.dumps(data, default=CollectedDataSeria)


@application.route('/ma_workshop/getAgvPos', methods=['GET'])
def ma_workshop_getAgvPose():
    re = AgvPos.query.first()
    result = []
    if re:
        result.append(re.pos_X)
        result.append(re.pos_Y)
        #cd = CollectedDatas.query.first()
        ##if cd and cd.electricity != 0 and cd.voltage != 0:
        ##    r = RobotInfo.query.filter_by(RobotInfo.uniqueid == cd.devid).first()
        ##    result.append(r.pos_X)
        ##    result.append(r.pos_Y)
        ##else:
        result.append(0)
        result.append(0)
    return json.dumps(result)

@application.route('/ma_workshop/searchHistoryDatas',methods=['POST'])
def ma_workshop_searchHistoryDatas():
    if request.form['startTime'] and request.form['devId']:
        reTime = {}
        reTime['startTime'] = request.form['startTime']
        reTime['endTime'] = request.form['endTime']
        id = int(request.form['devId'])
        query = CollectedDatas.query.filter_by(devid=application.config['DEVICES'][id]['uniqueid'])
        startTime = datetime.datetime.strptime(reTime['startTime'], '%Y-%m-%d %H:%M:%S')
        if reTime['endTime']:
            data = query.filter(CollectedDatas.time.between(startTime ,datetime.datetime.strptime(reTime['endTime'], '%Y-%m-%d %H:%M:%S'))).all()
        else:
            reTime['endTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = query.filter(CollectedDatas.time.between(startTime,
                                                            datetime.datetime.now())).all()
        vdatas = []
        edatas = []
        tdatas = []
        for col in data[::-1]:
            vdatas.append([time.mktime(col.time.timetuple()) * 1000, col.voltage])
            edatas.append([time.mktime(col.time.timetuple()) * 1000, col.electricity])
            tdatas.append([time.mktime(col.time.timetuple()) * 1000, col.temperature])
        data = dict()
        data['v'] = vdatas
        data['e'] = edatas
        data['t'] = tdatas
    else:
        return redirect(url_for('ma_index_index'))
    return render_template('manage/datasearchresult.html', titlename = '历史采集数据', reTime=reTime,reData=data,id=id)