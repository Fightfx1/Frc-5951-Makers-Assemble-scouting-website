import requests
import pandas as pd
import math

pd.options.display.max_rows = 999

class Schedule:
    def __init__(self, season="",eventCode="",tournamentLevel="",Exel_File=None):    
        
        if not Exel_File is None:
            self.__df = pd.read_csv(Exel_File)
        
        else:
            self.__df = None
            self._season = season
            self._eventCode = eventCode
            
            headers = {"Authorization":"Basic ZmlnaHRmeDE6Q0M1MkI0MzctMkZDQy00MDRELTkwQUYtOTU4MUJCMDcxQTY3",'Accept': 'application/json'}
            __url__ = "https://frc-api.firstinspires.org/v2.0/"
            r_url = f"{__url__}{season}/schedule/{eventCode}?tournamentLevel={tournamentLevel}"
            r = requests.get(r_url,headers=headers)
            
            self.data_r = r.json()['Schedule']
 
    def get_red_and_blue_teams_at_match(self,matchNumber):
        red_teams = []
        blue_teams = []

        if matchNumber < len(self.data_r):
            for team in self.data_r[matchNumber]['teams']:
                if "Red" in team['station']:
                    red_teams.append(team)
                elif "Blue" in team['station']:
                    blue_teams.append(team)

        return red_teams,blue_teams
    
    def __fix_match(self,matchNumber,red_teams,blue_teams):
        json_data = {"Match Number": matchNumber}
        
        for team in red_teams + blue_teams:
            json_data[team['station']] = team['teamNumber']
        
        return json_data
    
    def fix_match(self,matchNumber,teams):
        red_teams,blue_teams = teams
        json_data = {"Match Number": matchNumber}
        
        for team in red_teams + blue_teams:
            json_data[team['station']] = team['teamNumber']
        
        return json_data

    def get_all_matches_in_datafarme(self):
        _data = []
        for i in range(len(self.data_r)):
            red,blue = self.get_red_and_blue_teams_at_match(i)
            _data.append(self.__fix_match(i+1,red,blue))
        
        df = pd.DataFrame(_data)
        return df
    
    def __create_scouters_cards(self,scouters):
        scouters_cards = []
        for scouter in scouters:
            scouters_cards.append({"Name":scouter,"CountThatDid":0})
        return scouters_cards

    def __get_new_team(self,scouters,lastgroup):
        def help_for_sort(val):
            return val['CountThatDid']

        scouters.sort(key=help_for_sort, reverse=False)
        
        team = []
        i = 0

        for scouter in scouters:
            if scouter['Name'] not in lastgroup and i < 6:
                i+=1
                team.append(scouter['Name'])
                scouter['CountThatDid']+=6
        return team
                           
    def __append_scouters(self,df,scouters,last_group):
        i = 5
        for match_number in range(len(df)):
            if i == 5:
                scouters_team = self.__get_new_team(scouters,last_group)
                df.loc[match_number-0.5] = [f"{match_number+1}-{match_number+6}"] + (scouters_team)
                last_group = scouters_team
                i = 0
            else:
                i = i + 1
        self.__lastgroup = last_group

    def Get_Scouting_Schedule(self,scouters,last_group=[]):
        self.__lastgroup = []
        if not self.__df is None:
            scouters = self.__create_scouters_cards(scouters) # create scouters cards
            self.__append_scouters(self.__df,scouters,last_group)
            self.__df = self.__df.sort_index()
            return self.__df,self.__lastgroup
        
        
        df = self.get_all_matches_in_datafarme()
        scouters = self.__create_scouters_cards(scouters) # create scouters cards
        self.__append_scouters(df,scouters,last_group)
        df = df.sort_index()
        return df,self.__lastgroup
        

def get_team_avatar(teamNumber,season):
    headers = {"Authorization":"Basic ZmlnaHRmeDE6Q0M1MkI0MzctMkZDQy00MDRELTkwQUYtOTU4MUJCMDcxQTY3",'Accept': 'application/json'}
    __url__ = f"https://frc-api.firstinspires.org/v2.0/{season}/avatars?teamNumber={teamNumber}"
    try:
        r = requests.get(__url__,headers=headers)
        return r.json()['teams'][0]['encodedAvatar']
    except:
        return ""

