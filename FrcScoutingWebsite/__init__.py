from flask import Flask
from flask_bootstrap import Bootstrap
from FrcScoutingWebsite.Libarys.SettingsLib import Settings
from FrcScoutingWebsite.Libarys.FmsLib import Schedule
from FrcScoutingWebsite.Libarys.DataFrame import SaveDataFrame, SaveDataFrameOfGames,SaveDataFrameOfPitScouting
from FrcScoutingWebsite.Libarys.SpredSheetLib import SpreadSheetLib
from FrcScoutingWebsite.Libarys.ScoutersLib.Scouters_Lib import Scouters
from FrcScoutingWebsite.Libarys.FireBaseLib import FireBase_Lib
from FrcScoutingWebsite.Libarys.ScoutersSchedule.SaveScotersDataFrame import ScoutingScheduleSave
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import bcrypt

app = Flask(__name__,static_folder='static',static_url_path='/static')








app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.testing = False
bootstrap = Bootstrap(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usersdb.sqlite'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
salt = bcrypt.gensalt()





settings_lib = Settings('FrcScoutingWebsite/JsonFiles/settings.json')
scouters_lib = Scouters('FrcScoutingWebsite/Libarys/ScoutersLib/', settings_lib.get_EventCode())


SpreadSheet_Lib = SpreadSheetLib({
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
})
fire_base_lib = FireBase_Lib('FrcScoutingWebsite/JsonFiles/serviceUser.json')
save_data_frame_pit_scouting = SaveDataFrameOfPitScouting(SpreadSheet_Lib)
save_data_frame = SaveDataFrame(SpreadSheet_Lib,fire_base_lib)
SaveDataFrameOf_Games = SaveDataFrameOfGames()

scouting_schedule_save = ScoutingScheduleSave("FrcScoutingWebsite/Libarys/ScoutersSchedule/Schedules.npy")




from FrcScoutingWebsite import Routes
from FrcScoutingWebsite import match_data_route
from FrcScoutingWebsite import Api_Routes
from FrcScoutingWebsite import UsersRoutes