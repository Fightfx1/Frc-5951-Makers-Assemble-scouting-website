import firebase_admin
from firebase_admin import firestore, credentials


class FireBase_Lib:
    def __init__(self,service_account_path_file):
        self.__cred = credentials.Certificate(service_account_path_file)
        self.__update_auth()
        self.__db = firestore.client()
    
    def __update_auth(self):
        if(not len(firebase_admin._apps)):
            firebase_admin.initialize_app(self.__cred)

    def __fix_match(self,match):
        match = match['Match']
        # "Tried_To_Climb":match['EndGame']['Tried_To_Climb'],"Succeeded_Climb":match['EndGame']['Succeeded_Climb'],
        json_data = {
                "Match Number": match['match'],
                "Team Number": match['TeamNumber'],
                "color": match['color'],

                "Starting_Power_Cells":match['Autonomous']['Starting_Number_Of_Power_Cells'],
                "A_Hole":match['Autonomous']['Hole'],
                "A_Hex":match['Autonomous']['Hex'],
                "A_Low":match['Autonomous']['Low'],
                "Cross_Line":match['Autonomous']['Cross_Line'],

                "Spin_Wheel":match['teleop']['Spin_Wheel'],
                "Spin by color":match['teleop']['Color'],
                "T_Hole":match['teleop']['Hole'],
                "T_Hex":match['teleop']['Hex'],
                "T_Low":match['teleop']['Low'],

                "Tried_To_Climb":match['EndGame']['Tried_To_Climb'],
                "Succeeded_Climb":match['EndGame']['Succeeded_Climb'],
                "Generator Switch Level": match['EndGame']['Generator_Switch_Level'],
                "Park":match['EndGame']['Park'],
                "Was_Broken_or_dc":match['EndGame']['Was_Broken_or_dc'],
                
                "comments": match['comments'],
        }
        return json_data

    def get_scouting_data(self):
        self.__update_auth()
        All_Matches = self.__db.collection(u'ScoutingData').stream()
        return [self.__fix_match(match.to_dict()) for match in All_Matches]
    


