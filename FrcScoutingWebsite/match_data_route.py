from FrcScoutingWebsite import app,save_data_frame, SpreadSheet_Lib,save_data_frame_pit_scouting,db
from flask import render_template
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from flask_login import login_required, login_user,logout_user,current_user
from FrcScoutingWebsite.Libarys.UsersLib import Logs
from FrcScoutingWebsite.Libarys.FmsLib import get_team_avatar
matplotlib.use('Agg')   # פותר בעיה במחשבים שרצים במערכת הפעלה מקינטוש או מחשבים שרצים ב86 ביט

class plots_class:
    Climb_Plot = None
    Balls_Plot = None
    Auton_Balls_Plot = None
    roullte_Plot = None
    broken_or_dc_plot = None

class Text_Boxes:
    def __init__(self,df,TeamNumber):
        self.Telep_Avg_Of_Balls_Hole = np.around(df.T_Hole.mean())
        self.Telep_Avg_Of_Balls_Hex = np.around(df.T_Hex.mean())
        self.Telep_Avg_Of_Balls_Low = np.around(df.T_Low.mean())

        self.Autonomous_Avg_Of_Balls_Hole = np.ceil(df.A_Hole.mean())
        self.Autonomous_Avg_Of_Balls_Hex = np.ceil(df.A_Hex.mean())
        self.Autonomous_Avg_Of_Balls_Low = np.ceil(df.A_Low.mean())

        if df.T_Hole.sum() >= df.T_Hex.sum() and df.T_Hole.sum() > df.T_Low.sum():
            self.whenshot_teleop = (f"Team mostly shoots to the Hole target at teleop")
        elif df.T_Hole.sum() <= df.T_Hex.sum() and df.T_Hex.sum() >  df.T_Low.sum():
            self.whenshot_teleop = (f"Team mostly shoots to the Hex target at teleop")
        else:
            self.whenshot_teleop = (f"Team mostly shoots to the Low target at teleop")
        
        if df.A_Hole.sum() >= df.A_Hex.sum() and df.A_Hole.sum() > df.A_Low.sum():
            self.whereshot_autonomuous = (f"Team mostly shoots to the Hole target at autonomuous")
        elif df.A_Hole.sum() <= df.A_Hex.sum() and df.A_Hex.sum() > df.A_Low.sum():
            self.whereshot_autonomuous = (f"Team mostly shoots to the Hex target at autonomuous")
        else:
           self.whereshot_autonomuous = (f"Team mostly shoots to the Low at target at autonomuous")

        self.Header1 = "About The Robot:"
        self.__pit_scouting_data(TeamNumber)
        self.Header2 = "Some Statistic info:"
        self.Header3 = "More Info "
        self.Header4 = "Robot Options"
    def __pit_scouting_data(self,TeamNumber):
        
        df = save_data_frame_pit_scouting.get_dataframe()
        
        if df is None:
            new_log = Logs(username=current_user.username,action="setup database in Pit Scouting")
            db.session.add(new_log)
            db.session.commit()
            save_data_frame_pit_scouting.set_dataframe()
            df = save_data_frame_pit_scouting.get_dataframe()
        
        if df.empty:
            return
        
        df = df[df['TeamNumber'] == int(TeamNumber)]
        
        if df.empty:
            return
        
        self.Weight =str(df['Weight'].values[0])
        self.Propulsion_type = str(df['Propulsion_type'].values[0])
        self.Paddle_conversion = str(df['Paddle_conversion'].values[0])
        self.Amount_of_propulsion_engines = str(df['Amount_of_propulsion_engines'].values[0])
        self.Move_down_roll = str(df['Move_down_roll'].values[0])
        self.can_do_deffend = str(df['can_do_deffend'].values[0])
        self.route_options= str(df['route_options'].values[0])
        self.where_shoting = str(df['where_shoting'].values[0])
        self.from_were_he_can_shot = str(df['from_were_he_can_shot'].values[0])
        self.can_make_rollet = str(df['can_make_rollet'].values[0])
        self.have_auton = str(df['have_auton'].values[0])
        self.where_he_can_climb = str(df['where_he_can_climb'].values[0])
        self.can_move_on_bar = str(df['can_move_on_bar'].values[0])
        self.can_climb_with_more_robots = str(df['can_climb_with_more_robots'].values[0])
        
# פעולת עיצוב אשר משנה את שמות הקטגרויות בטבלה
def fix_columns_names(df):
    columns = df.columns.values
    columns = [
        ('Before Game',"Match Number"),('Before Game',"Team Number"),('Before Game',"color"),
        ("Autonomous","Starting Power Cells"),('Autonomous',"Hole"),('Autonomous',"Hex"),('Autonomous',"Low"),
        ('Autonomous',"Cross_Line"),
        ("Teleop","Spin_Wheel"),("Teleop","Spin by color"),("Teleop","Hole"),("Teleop","Hex"),("Teleop","Low"),
        ("End Game","Tried To Climb"),("End Game","Succeeded Climb"),("End Game","Generator Switch Level"),("End Game","Park"),("End Game","Disconnect or Was broken"),("End Game","comments")
    ]

    columns = pd.MultiIndex.from_tuples(columns)    
    df.columns = columns


@app.route("/MatchData/<match_numebr>")
@login_required
def match_data(match_numebr):
    df = save_data_frame.get_dataframe()
    
    if df is None:
        new_log = Logs(username=current_user.username,action="setup database in MatchData")
        db.session.add(new_log)
        db.session.commit()
        save_data_frame.set_dataframe()
        df = save_data_frame.get_dataframe()

    if df.empty:
        return render_template('MatchData.html',tables=[df.style.hide_index().render()])

    df = df.loc[df['Match Number'] == int(match_numebr)]
    
    if df.empty:
        return render_template('MatchData.html',tables=[df.style.hide_index().render()])
    def color_blue_at_blue(val):
        return 'background-color: #EEEEFF;'
    def color_blue_at_red(val):
        return 'background-color: #FFEEEE;'
    def color_false_true(val):
        color = 'black'
        if val == True and type(val) is bool:
            color = 'green'
        elif val == False and type(val) is bool:
            color = 'red'
        elif val == "BLUE":
            color = 'blue'
        elif val == "RED":
            color = 'red'

        return 'color: %s' % color
    df_red_teams = df.loc[df['color'] == "RED"]
    df_blue_teams = df.loc[df['color'] == "BLUE"]


    fix_columns_names(df_blue_teams)
    fix_columns_names(df_red_teams)
    
    return render_template('MatchData.html',tables=[(df_red_teams.style.applymap(color_false_true).applymap(color_blue_at_red).hide_index().render(), "Red teams"),(df_blue_teams.style.applymap(color_false_true).applymap(color_blue_at_blue).hide_index().render(),"Blue teams")])



# הפעולה מחזירה גרף על ידי החבילה מאט פלוט ליב היא עושה זאת על ידי ראפרנס בזיכרון
def render_plot(): 
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    buffer = b''.join(img)
    b2 = base64.b64encode(buffer)
    plt.clf()
    plt.close()
    return b2.decode('utf-8')




@app.route('/EventStatus')
@login_required
def Event_Status_page():
    df = save_data_frame.get_dataframe()
    
    if df is None:
        
        new_log = Logs(username=current_user.username,action="setup database in EventStatus")
        db.session.add(new_log)
        db.session.commit()

        save_data_frame.set_dataframe()
        df = save_data_frame.get_dataframe()

    if df.empty:
        return render_template('EventStatus.html',plot1=None)

    df = df.groupby('Team Number')['T_Hole','T_Hex','T_Low'].mean()

    print(df)
    df = df.sort_values(by=['T_Hex','T_Hole','T_Low'])
    ax = df.plot(kind='barh',colormap='jet',figsize=(20,30),zorder=2, width=0.5,align='center',linestyle=':')
    for p in ax.patches:
        plt.text(p.get_x() + p.get_width()+0.019, p.get_y()+0.017,str(np.ceil(p.get_width())))
    plot1 = render_plot()
    return render_template('EventStatus.html',plot1=plot1)


def create_plot_for_climb(df):
    df.loc[(df['Tried_To_Climb'] == True) | (df['Succeeded_Climb'] == True) | (df['Park'] == True)]['Succeeded_Climb'].value_counts(dropna=True).plot.pie(shadow=True,autopct='%1.2f%%',legend=True, colormap='jet').add_artist(plt.Circle((0,0),0.70,fc='white'))
    return render_plot() 
def create_plot_for_balls(df):
    df.plot(y=['T_Hole','T_Hex','T_Low'],x='Match Number',kind='line', colormap='jet', marker='.',markersize=10,title="Teleop balls plot")
    return render_plot()
def create_plot_for_auton_balls(df):
    df.plot(y=['A_Hole','A_Hex','A_Low'],x='Match Number',kind='line', colormap='jet', marker='.',markersize=10,title="autonomous balls plot")
    return render_plot()
def create_plot_for_roullte(df):
    df['Spin by color'].value_counts(dropna=True).plot.pie(shadow=True,autopct='%1.2f%%',legend=True, colormap='jet').add_artist(plt.Circle((0,0),0.70,fc='white'))
    graff1 = render_plot()
    df['Spin by color'].value_counts(dropna=True).plot.pie(shadow=True,autopct='%1.2f%%',legend=True, colormap='jet').add_artist(plt.Circle((0,0),0.70,fc='white'))
    return graff1,render_plot()
def create_broken_or_dc_plot(df):
    df['Was_Broken_or_dc'].value_counts(dropna=True).plot.pie(shadow=True,autopct='%1.2f%%',legend=True, colormap='jet').add_artist(plt.Circle((0,0),0.70,fc='white'))
    return render_plot()


@app.route('/GameData/TeamInfo/<TeamNumber>',methods=['GET', 'POST'])
@login_required
def team_info_page(TeamNumber):
    
    


    def color_false_true(val):
        color = 'black'
        if val == True and type(val) is bool:
            color = 'green'
        elif val == False and type(val) is bool:
            color = 'red'
        elif val == "BLUE":
            color = 'blue'
        elif val == "RED":
            color = 'red'

        return 'color: %s' % color



    df = save_data_frame.get_dataframe()
    
    if df is None:
        new_log = Logs(username=current_user.username,action="setup database in TeamInfo")
        db.session.add(new_log)
        db.session.commit()
        save_data_frame.set_dataframe()
        df = save_data_frame.get_dataframe()

    if df.empty:
        return render_template('TeamInfo.html',tables=[df.style.hide_index().render()])

    TeamNumber = int(TeamNumber)
    df = df.loc[df['Team Number'] == TeamNumber]
    # df = df.sort_values(by ='Match Number')

    plots = plots_class
    plots.Climb_Plot = create_plot_for_climb(df)
    plots.Balls_Plot = create_plot_for_balls(df)
    plots.Auton_Balls_Plot =create_plot_for_auton_balls(df)
    plots.roullte_Plot = create_plot_for_roullte(df)
    plots.broken_or_dc_plot = create_broken_or_dc_plot(df)
    text_boxs = Text_Boxes(df,TeamNumber)
    
    team_Avatar=get_team_avatar(TeamNumber,2020)
    fix_columns_names(df)
    return render_template('TeamInfo.html',tables=[df.style.applymap(color_false_true).hide_index().render()],plots=plots,text_boxs=text_boxs,TeamName="FRC #"+str(TeamNumber),team_Avatar=team_Avatar)