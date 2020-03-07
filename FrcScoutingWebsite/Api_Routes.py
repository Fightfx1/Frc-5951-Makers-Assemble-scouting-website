from FrcScoutingWebsite import app, scouters_lib,settings_lib,Schedule,scouting_schedule_save
from flask import jsonify, request, Response
import json

@app.route('/api/v3/CanAcsess',methods=['POST'])
def GetUser():
    reslut = False
    if scouters_lib.get_scouter(request.headers.get('UserName'))!=None:
        reslut = request.headers.get('UserName')
    return jsonify({"CanAcsess":reslut}),200




@app.route('/api/v3/GetSchedule/<UserName>',methods=['GET'])
def get_Schedule(UserName):
    Schedules = scouting_schedule_save.get_Schedules()
    if UserName in Schedules:
        return jsonify(Schedules[UserName])
    return jsonify({}),404
    
@app.route('/api/v3/GetMatchSchedule/<UserName>',methods=['GET'])
def get_match_schedule(UserName):
    Schedules = scouting_schedule_save.get_Schedules()
    if UserName in Schedules:
        return jsonify(Schedules[UserName])
    return jsonify({}),404