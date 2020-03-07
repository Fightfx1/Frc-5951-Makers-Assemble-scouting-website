from flask import Flask
from flask_bootstrap import Bootstrap
from FrcScoutingWebsite.Libarys.UsersLib import Users_Lib
from FrcScoutingWebsite.Libarys.SettingsLib import Settings
from FrcScoutingWebsite.Libarys.FmsLib import Schedule
from FrcScoutingWebsite.Libarys.DataFrame import SaveDataFrame, SaveDataFrameOfGames
from FrcScoutingWebsite.Libarys.SpredSheetLib import SpreadSheetLib
from FrcScoutingWebsite.Libarys.ScoutersLib.Scouters_Lib import Scouters
from FrcScoutingWebsite.Libarys.FireBaseLib import FireBase_Lib
from FrcScoutingWebsite.Libarys.ScoutersSchedule.SaveScotersDataFrame import ScoutingScheduleSave
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.testing = False
bootstrap = Bootstrap(app)

users_lib = Users_Lib("FrcScoutingWebsite/JsonFiles/UsersLogininfo.json")
settings_lib = Settings('FrcScoutingWebsite/JsonFiles/settings.json')
scouters_lib = Scouters('FrcScoutingWebsite/Libarys/ScoutersLib/', settings_lib.get_EventCode())


SpreadSheet_Lib = SpreadSheetLib({
  "type": "service_account",
  "project_id": "quixotic-bonito-264311",
  "private_key_id": "bef3520e6b3fc25b9dfe662962959821480990d3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4kjNYF39dFI9/\ncPAqe3bzw8FDASiv0PjNZ3mQPeYkh9DjrpjvBUci5au1n4OSNKNxjru/LoCqKrY8\nE/uQbhpD0ENnyGXCQl6ZaE2ul+cz5caQyEMpfcFUo6286TB9YVjohJGRRbZZQNrV\ngAk7Mp64u1twFRXEjdU0+uKVb/O2vigMGu/XDpyi3qIrbdHW1fCKCG2MjCV551V3\ntomH6ci1CBrYA60e4Ep27H6wgboW3xuMwBxAtg/ZySmu1SvGDhYypU/x3ysAJvyf\nC1VjORDVwLp5j+KFnqMB3YHsgMkOmVV8vBIrMtyBcSNPZsA0ZopU0d6rya5I9cQG\nI9XHrOlNAgMBAAECggEAAP85K8akt3n+9G9FvNUB5XsvNg9xitGUJnfinjbXYWci\nZ7hvtwrOQZAAB3EfItEJ+PkOZo/3vfORHG33M+aEWc1sL8lTU2NMY4O+t6y2YP9i\nvTF3u2ekfbKMo7KWwnaeJlNg/enkfELva6vPYPR7CwBoFAjpHzCs8CZSxv/dzyTh\ncwPw6iXTRPt3KQtcmp3j8lOBDeQhFN0stOw6HhHAu1gVQrI1IZUWwPnZf23F4tTz\nF7dQ5AB8ZIOizELu5WJhF439bMvft4QG/8aVI+3wQb6axXdufaXyj8H7f339HJSI\nUU8C8Cb0uZbcUr6cdz03NDvQmeq6TONIWbZqVXXuwQKBgQDtTVuA+8qUNxHwtvqM\nvhc9vWgSHLWPHQnXtueB3+ZOsyHd/L5zCCmvkkgGjrC6f2Y2bI3npZ0+2gmzQmjl\nPG31FFA10AsO71UBU2NHclGud8QLbYRQNUpa9NTQQQ6IVEUW8E6MvR6nSWedt/5H\nWncjmex8283kFJePk7NSZTeiuQKBgQDHHTMwmaVbuV6rTQWacg9JD44AwWxNVACD\nd9ErmaTiy8vEP3OiYFEedkkCDhhdKmSzeCBpKrv3U50/iYtB+BILeKssXaKQNpwY\nXVCcwddXBpWfFgXRK9qjYflSl5Giqq1EcuEMixUFGISF4H6879xHTyGGKiQhQyIC\njV2tavGBNQKBgDSRbHHYVXob8Pd4MWy4N4HP0Zwhi/7WGfYVaJeWt/g7Kod4k9/7\nsPBZ4WbCeVf3HPd1eMIWKA1iU7/IOGB/0IP4KgShv7FhR11x0Y5kPr/9fApkCmmS\nRJR9pB82Kjf9Iwj/1wbKZl38nt2LguLfoYDbek32i1e5UBHYUGMyVO7RAoGACLj/\nwBZLByykuA5ku3JZtxKmXuQaUXznlNrP4AAYGBNjdtJsx2U+yH3YDu39JT+xL6eI\ni/LiTyBrmBf3cMlkSPpdTVFAyN6LkgmseWGIhHh2X4TAdnxcVKH7ISIgsCaX9pKt\nxzXkkteTHqZKBw7e8ITH7C+2a3qcZ843l1xC/i0CgYAvDBAVdQhkfhHjGLsY5rhZ\nkUXyEueH8d8aozh2wyjXBjSELMoOut06Lp7tjSoMHIMB2iC0ykbYm4igH6H8pRqk\nG4QXMnO2p8yX0CxLxbueunO02aQxjUSAbPN5qarayT+Ad88tbKev7JH57E1owVqU\n7pkll1KuBqTnYeQeeCgJ1Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "mainservice@quixotic-bonito-264311.iam.gserviceaccount.com",
  "client_id": "117483937402590852702",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mainservice%40quixotic-bonito-264311.iam.gserviceaccount.com"
})
fire_base_lib = FireBase_Lib('FrcScoutingWebsite/JsonFiles/serviceUser.json')

save_data_frame = SaveDataFrame(SpreadSheet_Lib,fire_base_lib)
SaveDataFrameOf_Games = SaveDataFrameOfGames()

scouting_schedule_save = ScoutingScheduleSave("FrcScoutingWebsite/Libarys/ScoutersSchedule/Schedules.npy")




from FrcScoutingWebsite import Routes
from FrcScoutingWebsite import match_data_route
from FrcScoutingWebsite import Api_Routes