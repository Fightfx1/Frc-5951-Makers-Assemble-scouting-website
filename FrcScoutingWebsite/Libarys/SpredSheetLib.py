import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

class SpreadSheetLib:
    def __init__(self,service_account):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.__creds = ServiceAccountCredentials._from_parsed_json_keyfile(service_account,scope)
        self.__google_client = gspread.authorize(self.__creds)
    
    def __relogin(self):
        if self.__creds.access_token_expired:
            self.__google_client.login()  # refreshes the token

    def __get_regular_scouting(self):
        self.__relogin()

        sheet = self.__google_client.open_by_url("https://docs.google.com/spreadsheets/d/1RF1m07AgCVAa-0XP0c7f0wLWHBzYFDNdohhXc2TDYVs/edit#gid=1287437129").sheet1
        return sheet.get_all_records()

    def __get_pit_scouting(self):
        self.__relogin
        sheet = self.__google_client.open_by_url('https://docs.google.com/spreadsheets/d/14A1vXw86u7yMlFb0Gfc9zUPA9SFZsS6qP2pLDPnM-o4/edit#gid=32160033').sheet1
        return sheet.get_all_records()

    def __fix_data_regular_scouting(self,data):
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

            "Tried_To_Climb":data['האם הרובוט ניסה לטפס?'] == "TRUE",
            "Succeeded_Climb":data['האם הצליח לטפס?']== "TRUE",
            "Generator Switch Level":data['האם באר הטיפוס מאוזן?'] == "TRUE",
            "Park":data['האם הרובוט חנה באזור הנדנדה?'] == "TRUE",
            "Was_Broken_or_dc":data['האם הרובוט הפסיק לעבוד/נשבר/איבד תקשורת באמצע המקצה?'] == "TRUE",
            "comments":data["הערות (הגנה, טיפוס זוגי וכו')"]

        }

        return fixed_data
    
    def __fix_all_regular_scouting_data(self,data_to_fix):
        return  [self.__fix_data_regular_scouting(i) for i in np.array(data_to_fix)]
 
    def get_regular_scouting_data(self):
        return self.__fix_all_regular_scouting_data(self.__get_regular_scouting())

    def __fix_pit_scouting_data(self,data):
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
    
    def __fix_all_pit_scouting(self,data):
        return [self.__fix_pit_scouting_data(i) for i in np.array(data)]
    
    def get_all_pit_scouting_data(self):
        return self.__fix_all_pit_scouting(self.__get_pit_scouting())

