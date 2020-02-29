from FrcScoutingWebsite.Libarys.SpredSheetLib import get_spreadsheet_data
import pandas as pd

pd.options.display.max_rows = 999


class SaveDataFrame:
    def __init__(self):
        self._privatedf = None

    def set_dataframe(self):
        self._privatedf = pd.DataFrame(get_spreadsheet_data())

    def get_dataframe(self):
        return self._privatedf

