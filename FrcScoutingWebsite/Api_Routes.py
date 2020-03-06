from FrcScoutingWebsite import app, scouters_lib
from flask import jsonify, request
import json

@app.route('/api/v3/CanAcsess',methods=['POST'])
def GetUser():
    reslut = False
    if scouters_lib.get_scouter(request.headers.get('UserName'))!=None:
        reslut = request.headers.get('UserName')
    return jsonify({"CanAcsess":reslut}),200


