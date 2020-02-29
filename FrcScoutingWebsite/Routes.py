from FrcScoutingWebsite import app, users_lib, settings_lib,Schedule
from flask import render_template, request, url_for, redirect, session
from FrcScoutingWebsite.Forms import LoginForm, SettingsForm

@app.route('/')
@app.route('/home')
def index_page():
    return render_template('index.html')





@app.route("/Matches")
def all_matches_page():
    Schedule_lib = Schedule(settings_lib.get_season(),settings_lib.get_EventCode(),settings_lib.get_tournamentLevel())
    df = Schedule_lib.get_all_matches_in_datafarme()
    df['Match Number'] = df['Match Number'].apply(lambda x: f'<a href="{url_for("match_data",match_numebr=x)}">{x}</a>')
    return render_template('ScoutingData.html',tables=[df.style.hide_index().render()])





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