import numpy as np
import os.path
from FrcScoutingWebsite.Libarys.FmsLib import Schedule as Schedule_Lib

class ScoutingScheduleSave:
    def __init__(self,path_to_Schedules):
        self.__path_to_Schedules = path_to_Schedules
        
        if not os.path.isfile(self.__path_to_Schedules ): 
            self.Remove_All()

        self.__Schedules = np.load(self.__path_to_Schedules,allow_pickle=True).tolist()
        
    def update_Schedules(self,df,scouters,scouting_sc):
        self.data_r = scouting_sc.data_r
        Schedule = {}
        
        for name in scouters:
            df_for_scouter = df.loc[(df['Red1'] == name) | (df['Red2'] == name) | (df['Red3'] == name) | (df['Blue1'] == name) | (df['Blue2'] == name) | (df['Blue3'] == name)]
            index = 0
            def get_col_name(index, scouter_name):
                row = df_for_scouter.iloc[[index]]
                index+=1
                if row['Red1'].values[0] == scouter_name:
                    return "Red1"
                elif row['Red2'].values[0] == scouter_name:
                    return "Red2"
                elif row['Red3'].values[0]  == scouter_name:
                    return "Red3"
                elif row['Blue1'].values[0]  == scouter_name:
                    return "Blue1"
                elif row['Blue2'].values[0]  == scouter_name:
                    return "Blue2"
                elif row['Blue3'].values[0]  == scouter_name:
                    return "Blue3"
                return "IDK"
            
            Schedule_ForName = [{"StartMatch":int(i+0.5),"Col":get_col_name(index,name),"LastMatch":int(i+5.5)} for i in df_for_scouter.index]
            
            _data = [scouting_sc.fix_match(i+1,scouting_sc.get_red_and_blue_teams_at_match(i)) for i in range(len(self.data_r))]
            
            def get_matches(StartMatch,LastMatch,ColName):
                return [{"Match Number":_data[i]['Match Number'],"Team Number":_data[i][ColName]}  for i in range(StartMatch,LastMatch)]
                
            matches = [get_matches(turn['StartMatch'],turn['LastMatch'], turn['Col']) for turn in Schedule_ForName]
            Schedule[name] = matches
            
        self.__Schedules = Schedule
        self.__update()
        
    def __update(self):
        np.save(self.__path_to_Schedules,self.__Schedules)


    def get_Schedules(self):
        return self.__Schedules
    
    def Remove_All(self):
        np.save(self.__path_to_Schedules,[])

