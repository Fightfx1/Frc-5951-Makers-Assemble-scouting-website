import numpy as np 
import os.path

class Scouter:    
    def __init__(self,ScouterName,MatchestoScouting=[]):
        self.Scouter_Name = ScouterName
        self.Matches_to_Scouting = np.array(MatchestoScouting)

class Scouters:
    def __init__(self,path_to_scouters_lib,EventCode):
        self.__lib_path = path_to_scouters_lib
        self.__path_to_scouters_lib = str(path_to_scouters_lib) + EventCode + ".npy"
        self.EventCode = EventCode
        if not os.path.isfile(self.__path_to_scouters_lib ): 
            self.Remove_All()

        self.__scouters_list = np.load(self.__path_to_scouters_lib,allow_pickle=True).tolist()

    def update_event_code(self,EventCode):
        self.__path_to_scouters_lib = self.__lib_path + EventCode + ".npy"
        self.EventCode = EventCode
        if not os.path.isfile(self.__path_to_scouters_lib): 
            self.Remove_All()
        
        self.__scouters_list = np.load(self.__path_to_scouters_lib,allow_pickle=True).tolist()

    def __update_the_file(self):
        np.save(self.__path_to_scouters_lib,self.__scouters_list)

    def add_new_scouter(self,Scouter_Name,Matches_to_Scouting=[]):
        if not Scouter_Name in (obj.Scouter_Name for obj in self.__scouters_list):
            self.__scouters_list.append(Scouter(Scouter_Name,Matches_to_Scouting))
            self.__update_the_file()

    def __get_scouter(self,Scouter_Name):
        return next((x for x in self.__scouters_list if x.Scouter_Name == Scouter_Name), None)

    def get_all_scouters_names(self):
        return [scouter.Scouter_Name for scouter in self.__scouters_list]

    def delete_scouter(self,ScouterName):
        scouter = self.__get_scouter(ScouterName)
        if scouter == None: return
        self.__scouters_list.remove(scouter)
        self.__update_the_file()


    def update_scouter_matches(self,Scouter_Name,Matches_to_Scouting):
        scouter = self.__get_scouter(Scouter_Name)
        
        if scouter == None: return
        
        scouter.Matches_to_Scouting = Matches_to_Scouting
        self.__update_the_file()
    
    def get_all_scouters(self):
        return self.__scouters_list
    
    def Remove_All(self):
        np.save(self.__path_to_scouters_lib,[])
