import pandas as pd

pd.options.display.max_rows = 999


class SaveDataFrame:
    def __init__(self,SpreadSheet_Lib, FireBase_Lib):
        self._privatedf = None
        self.__SpreadSheet_Lib = SpreadSheet_Lib
        self.__FireBase_Lib = FireBase_Lib

    def set_dataframe(self):
        self._privatedf = pd.DataFrame(self.__SpreadSheet_Lib.get_regular_scouting_data() + self.__FireBase_Lib.get_scouting_data())
        if not self._privatedf.empty:
            self._privatedf = self._privatedf.loc[~self._privatedf['comments'].isin(['T'])]
            self._privatedf['comments'] = self._privatedf['comments'].replace(0,"")
            self._privatedf = self._privatedf.sort_values(by=['Team Number','Match Number'],ascending=[True, True])

    def get_dataframe(self):
        return self._privatedf

class SaveDataFrameOfGames:
    def __init__(self,):
        self._privatedf = None
        self.__data_event = None

    def set_dataframe(self,DataFrame,data_event):
        self._privatedf = pd.DataFrame(DataFrame)
        self.__data_event = data_event

    def get_event(self):
        return self.__data_event

    def get_dataframe(self):
        return self._privatedf


class SaveDataFrameOfPitScouting:
    def __init__(self,SpreadSheet_Lib):
        self._privatedf = None
        self.__SpreadSheet_Lib = SpreadSheet_Lib

    def set_dataframe(self):
        self._privatedf = pd.DataFrame(self.__SpreadSheet_Lib.get_all_pit_scouting_data())

    def get_dataframe(self):
        return self._privatedf
