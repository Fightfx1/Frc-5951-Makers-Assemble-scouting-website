import json

class Settings:
    def __init__(self,path_to_json_settings):
        self.__path_to_file = path_to_json_settings
        self.__get_data()
        
    def __update(self):
        with open(self.__path_to_file,'w') as file:
            json.dump(self.__json_data,file)
            file.close()

    def __get_data(self):
        with open(self.__path_to_file,'r') as file:
            self.__json_data = json.load(file)
            file.close()



    def get_EventCode(self):
        return self.__json_data['EventCode']

    def set_EventCode(self, EventCode):
        self.__json_data['EventCode'] = EventCode
        self.__update()

    def get_tournamentLevel(self):
        return self.__json_data['tournamentLevel']
    def set_tournamentLevel(self,tournamentLevel):
        self.__json_data['tournamentLevel'] = tournamentLevel
        self.__update()

    def get_season(self):
        return self.__json_data['season']
    def set_season(self,season):
        self.__json_data['season'] = season
        self.__update()
    
    def create_scouting_team(self,team_name):
        if team_name not in self.__json_data['Scouters_Teams']:
            self.__json_data['Scouters_Teams'][team_name] = []
            self.__update()
    def remove_scouting_team(self,team_name):
        if team_name in self.__json_data['Scouters_Teams']:
            del self.__json_data['Scouters_Teams'][team_name]
            self.__update()
    def add_scouter_to_team(self,team_name,scouter):
        if team_name in self.__json_data['Scouters_Teams']:
            self.__json_data['Scouters_Teams'][team_name].append(scouter)
            self.__update()
    def add_scouters_to_team(self,team_name,scouters):
        if team_name in self.__json_data['Scouters_Teams']:
            self.__json_data['Scouters_Teams'][team_name].extend(scouters)
            self.__update()
    def remove_scouter_from_team(self,team_name,scouter_name):
        if team_name in self.__json_data['Scouters_Teams'] and scouter_name in self.__json_data['Scouters_Teams'][team_name]:
            self.__json_data['Scouters_Teams'][team_name].remove(scouter_name)
            self.__update()