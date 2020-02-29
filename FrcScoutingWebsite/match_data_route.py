from FrcScoutingWebsite import app,save_data_frame
from flask import render_template
import pandas as pd

# פעולת עיצוב אשר משנה את שמות הקטגרויות בטבלה
def fix_columns_names(df):
    columns = df.columns.values
    columns = [
        ('Before Game',"Match Number"),('Before Game',"Team Number"),('Before Game',"color"),
        ("Autonomous","Starting Power Cells"),('Autonomous',"A_Hole"),('Autonomous',"A_Hex"),('Autonomous',"A_Low"),
        ('Autonomous',"Cross_Line"),
        ("Teleop","Spin_Wheel"),("Teleop","Spin by color"),("Teleop","T_Hole"),("Teleop","T_Hex"),("Teleop","T_Low"),
        ("End Game","Climb",),("End Game","Generator Switch Level"),("End Game","Park"),("End Game","Disconnect or Was broken"),("End Game","comments")
    ]

    columns = pd.MultiIndex.from_tuples(columns)    
    df.columns = columns


@app.route("/MatchData/<match_numebr>")
def match_data(match_numebr):
    df = save_data_frame.get_dataframe()
    
    if df is None:
        save_data_frame.set_dataframe()
        df = save_data_frame.get_dataframe()

    if df.empty:
        return render_template('MatchData.html',tables=[df.style.hide_index().render()])

    df = df.loc[(df['Match Number'] == int(match_numebr)) & (~df['comments'].isin(['T']))]
    df['comments'] = df['comments'].replace(0,"")

    fix_columns_names(df)
    return render_template('MatchData.html',tables=[df.style.hide_index().render()])