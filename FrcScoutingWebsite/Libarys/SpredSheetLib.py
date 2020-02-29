import gspread
from oauth2client.service_account import ServiceAccountCredentials

api_json_file = {
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
}


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials._from_parsed_json_keyfile(api_json_file,scope)
client = gspread.authorize(creds)



# Regular Scouting Get Data from google sheets.
# ==================================================

# return all speradsheet of regular scouting data
def get_spreadsheet_data():
    if creds.access_token_expired:
      client.login()  # refreshes the token
    
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RF1m07AgCVAa-0XP0c7f0wLWHBzYFDNdohhXc2TDYVs/edit#gid=1287437129").sheet1
    
    return fix_all_regular_scouting_data(sheet.get_all_records())

def fix_all_regular_scouting_data(data):
    all_regular_scouting = []
    for team in data:
        all_regular_scouting.append(fix_data_regular_scouting(team))
    
    
    return all_regular_scouting


def fix_data_regular_scouting(data):
    fixed_data = {

        "Match Number":data['מקצה'],
        "Team Number":data['מספר קבוצה'],
        "color": data['ברית'],

        
        "Starting_Power_Cells":data['עם כמה כדורים הרובוט התחיל?'],
        "A_Hole":int(data['כדורים לחור במשושה (אוטונומי)']),
        "A_Hex":int(data['כדורים למשושה (אוטונומי)']),
        "A_Low":int(data['כדורים לנמוך (אוטונומי)']),
        "Cross_Line":data['הרובוט עבר את הקו באוטנומי?'] == "TRUE",



        
        "Spin_Wheel":data['רולטה לפי סיבובים'] == "TRUE",
        "Spin by color":data['רולטה לפי צבע'] == "TRUE",
        "T_Hole":int(data['כדורים לחור במשושה (טלאופ)']),
        "T_Hex":int(data['כדורים למשושה (טלאופ)']),
        "T_Low":int(data['כדורים לנמוך (טלאופ)']),
                
        "Climb":data['האם טיפס?'] == "TRUE",
        "Generator Switch Level":data['האם באר הטיפוס מאוזן?'] == "TRUE",
        "Park":data['האם הרובוט חנה באזור הנדנדה?'] == "TRUE",
        "Was_Broken_or_dc":data['האם הרובוט הפסיק לעבוד/נשבר/איבד תקשורת באמצע המקצה?'] == "TRUE",
        "comments":data["הערות (הגנה, טיפוס זוגי וכו')"]

    }
    return fixed_data

# block end =========================================

# Pit Scouting Get Data Form Google sheets.
# ==========================================

def fix_pit_scouting_data(data):
    fixed_data = {
        "TeamNumber":data['מספר קבוצה'],
        "Weight":data['כמה הרובוט שוקל? (ק"ג)'],
        "Propulsion_type":data['סוג הנעה?'],
        "Paddle_conversion":data['המרה בהנעה?'],
        "Amount_of_propulsion_engines":data['כמות מנועים בהנעה? (לכל צד)'],
        "Move_down_roll":data['עובר מתחת לרולטה?'],
        "can_do_deffend":data['יכול לעשות הגנה?'],
        "have_auton":data['יש אוטונומי?'],
        "route_options":data['אופציות למסלולים באוטונומי?'],
        "where_shoting":data['לאן יורה?'],
        "from_were_he_can_shot":data['מאיפה יכול לירות במגרש?'],
        "can_make_rollet":data['יכול לעשות רולטה?'],
        "can_climb":data['יכול לטפס?'],
        "where_he_can_climb":data['איפה יכול לטפס?'],
        "can_move_on_bar":data['יכול לזוז על המוט? (מערכת שינוע)'],
        "can_climb_with_more_robots":data['יכול לטפס עם עוד רובוט?'],
        "Comments":data['הערות']
    }
    return fixed_data

def fix_all_pit_scouting_data(data):
    fixed = []
    for team in data:
        fixed.append(fix_pit_scouting_data(team))

    return fixed

def get_pit_scouting_data():
    if creds.access_token_expired:
      client.login()  # refreshes the token

    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/14A1vXw86u7yMlFb0Gfc9zUPA9SFZsS6qP2pLDPnM-o4/edit#gid=32160033').sheet1

    return fix_all_pit_scouting_data(sheet.get_all_records())

def find_row_by_team_number_pitscouting(TeamNumber):
    if creds.access_token_expired:
      client.login()  # refreshes the token
    
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/14A1vXw86u7yMlFb0Gfc9zUPA9SFZsS6qP2pLDPnM-o4/edit#gid=32160033').sheet1
    
    for data in sheet.get_all_records():
        if(str(data['מספר קבוצה']) == TeamNumber):
            return fix_pit_scouting_data(data)
    return {}


# block end ============================================

