from FrcScoutingWebsite import app, scouters_lib
from flask import jsonify, request

@app.route('/api/v3/CanAcsess/',methods=['POST'])
def GetUser():
    return jsonify({"CanAcsess":scouters_lib.get_scouter(request.headers.get('UserName'))!=None})


