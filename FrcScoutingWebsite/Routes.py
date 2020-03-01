from FrcScoutingWebsite import app, users_lib, settings_lib,Schedule, SaveDataFrameOf_Games
from flask import render_template, request, url_for, redirect, session
from FrcScoutingWebsite.Forms import LoginForm, SettingsForm

@app.route('/')
@app.route('/home')
def index_page():
    return render_template('index.html')

@app.route("/Matches")
def all_matches_page():
    def make_click_able(df):
        df['Match Number'] = df['Match Number'].apply(lambda x: f'<a href="{url_for("match_data",match_numebr=x)}">{x}</a>')
        df['Blue1'] = df['Blue1'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
        df['Blue2'] = df['Blue2'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
        df['Blue3'] = df['Blue3'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
        df['Red1'] = df['Red1'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
        df['Red2'] = df['Red2'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
        df['Red3'] = df['Red3'].apply(lambda x: f'<a href="{url_for("team_info_page",TeamNumber=x)}">{x}</a>')
    
    # ===========================================speed up network shit============================================================
    if SaveDataFrameOf_Games.get_dataframe is None:
        Schedule_lib = Schedule(settings_lib.get_season(),settings_lib.get_EventCode(),settings_lib.get_tournamentLevel())
        df = Schedule_lib.get_all_matches_in_datafarme()
        make_click_able(df)
        SaveDataFrameOf_Games.set_dataframe(df,settings_lib.get_EventCode())
    
    elif not SaveDataFrameOf_Games.get_event() is None and SaveDataFrameOf_Games.get_event() == settings_lib.get_EventCode():
        df = SaveDataFrameOf_Games.get_dataframe()
    
    else:
        Schedule_lib = Schedule(settings_lib.get_season(),settings_lib.get_EventCode(),settings_lib.get_tournamentLevel())
        df = Schedule_lib.get_all_matches_in_datafarme()
        make_click_able(df)
        SaveDataFrameOf_Games.set_dataframe(df,settings_lib.get_EventCode())
    # =============================================================================================================================
    

    def color_blue_at_blue(val):
        return 'background-color: #EEEEFF; color: #3F51B5'
    def color_blue_at_red(val):
        return 'background-color: #FFEEEE; color: #3F51B5'

    
    s = df.style.applymap(color_blue_at_blue,subset=['Blue1','Blue2','Blue3'])
    s = s.applymap(color_blue_at_red,subset=['Red1','Red2','Red3'])
    
    
    return render_template('ScoutingData.html',tables=[s.hide_index().render()])


 


@app.route('/SettingsPage',methods=['GET','POST'])
def settings_page():
    settings_form = SettingsForm()

    if request.method == "POST" and settings_form.validate_on_submit and  settings_form.is_submitted():
        settings_lib.set_EventCode(str(settings_form.EventCode.data))
        settings_lib.set_season(str(settings_form.Season.data))
        settings_lib.set_tournamentLevel(str(settings_form.tournamentLevel.data))
       
    settings_form.EventCode.data = settings_lib.get_EventCode()
    settings_form.tournamentLevel.data = settings_lib.get_tournamentLevel()
    settings_form.Season.data = settings_lib.get_season()

    return render_template('settings.html',settings_form=settings_form)


@app.route('/Login',methods=['GET','POST'])
def login_page():
    login_form = LoginForm()
    
    if request.method == "POST" and login_form.validate_on_submit and login_form.is_submitted():
        if users_lib.Login(login_form.username.data,login_form.password.data):
            session['logged_in'] = True
            return redirect(url_for("index_page"))

    return render_template('login.html',form=login_form)

@app.route('/Logout')
def logout_page():
    session['logged_in'] = False
    return render_template('index.html') 