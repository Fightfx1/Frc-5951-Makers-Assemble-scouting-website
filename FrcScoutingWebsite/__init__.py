from flask import Flask
from flask_bootstrap import Bootstrap
from FrcScoutingWebsite.Libarys.UsersLib import Users_Lib
from FrcScoutingWebsite.Libarys.SettingsLib import Settings
from FrcScoutingWebsite.Libarys.FmsLib import Schedule
from FrcScoutingWebsite.Libarys.DataFrame import SaveDataFrame
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

bootstrap = Bootstrap(app)

users_lib = Users_Lib("FrcScoutingWebsite/JsonFiles/UsersLogininfo.json")
settings_lib = Settings('FrcScoutingWebsite/JsonFiles/settings.json')
save_data_frame = SaveDataFrame()
from FrcScoutingWebsite import Routes
from FrcScoutingWebsite import match_data_route