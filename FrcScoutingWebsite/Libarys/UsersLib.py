import json

class Users_Lib:
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
    
    def Login(self,username,password):
        user_model = {"UserName":username,"Pass":password,"id":1}
        return user_model in self.__json_data['Users']