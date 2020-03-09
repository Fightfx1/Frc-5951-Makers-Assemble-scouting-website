from FrcScoutingWebsite import app, settings_lib,Schedule, SaveDataFrameOf_Games,scouters_lib, scouting_schedule_save,save_data_frame_pit_scouting,save_data_frame
from flask import render_template, request, url_for, redirect, session, flash
from FrcScoutingWebsite.Forms import LoginForm, SettingsForm,AddMemberToTeam_Form
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, login_user,logout_user,current_user


UPLOAD_FOLDER = 'FrcScoutingWebsite/MatchesFile'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/static/<path>')
def static_file(path):
  return app.send_static_file(path)

@app.route('/')
@app.route('/home')
def index_page():
    return render_template('index.html')




@app.route("/Matches")
@login_required
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
@login_required
def settings_page():
    settings_form = SettingsForm()

    if request.method == "POST" and settings_form.validate_on_submit and  settings_form.is_submitted():
        if request.form.get('submit') != None:
            settings_lib.set_EventCode(str(settings_form.EventCode.data))
            settings_lib.set_season(str(settings_form.Season.data))
            settings_lib.set_tournamentLevel(str(settings_form.tournamentLevel.data))
            settings_lib.set_to_use_file(settings_form.useFileYesNo.data)
        
        
        elif request.form.get('Upload') != None:

            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                file.save(os.path.join(UPLOAD_FOLDER, "ScTrain.csv"))

        elif request.form.get('Realod') != None:
            save_data_frame_pit_scouting.set_dataframe()
            save_data_frame.set_dataframe()
        
        return redirect(url_for("settings_page"))
       
    settings_form.EventCode.data = settings_lib.get_EventCode()
    settings_form.tournamentLevel.data = settings_lib.get_tournamentLevel()
    settings_form.Season.data = settings_lib.get_season()
    settings_form.useFileYesNo.data = settings_lib.get_to_use_file()

    return render_template('settings.html',settings_form=settings_form)

@app.route('/ScoutingSchedule',methods=['GET','POST'])
@login_required
def Schedule_Page():
    if len(scouters_lib.get_all_scouters_names()) < 12:
        return render_template('Massege.html',Msg="Minimum 12 scouters to Create Schedule")
    if settings_lib.get_to_use_file():
        scouting_sc = Schedule(Exel_File="FrcScoutingWebsite/MatchesFile/ScTrain.csv")  
    else:
        scouting_sc = Schedule(settings_lib.get_season(),settings_lib.get_EventCode(),settings_lib.get_tournamentLevel())
    
    df,last_group = scouting_sc.Get_Scouting_Schedule(scouters_lib.get_all_scouters_names(),settings_lib.get_last_group())
    settings_lib.set_last_group(last_group)

    if request.method == 'POST':
        if request.form.get('submit_button') == "publish scouting schedule":
            scouting_schedule_save.update_Schedules(df,scouters_lib.get_all_scouters_names(),scouting_sc)
            return redirect(url_for("Schedule_Page"))


    s = df.style.hide_index()
    def color_blue_at_blue(val):
        return 'background-color: #EEEEFF; color: #3F51B5'
    def color_blue_at_red(val):
        return 'background-color: #FFEEEE; color: #3F51B5'

    
    s = df.style.applymap(color_blue_at_blue,subset=['Blue1','Blue2','Blue3'])
    s = s.applymap(color_blue_at_red,subset=['Red1','Red2','Red3'])

    return render_template('ScoutingSchedule.html',tables=[s.hide_index().render()])

@app.route('/Scouters_setup',methods=['GET','POST'])
@login_required
def scouters_setup_page():
    if scouters_lib.EventCode != settings_lib.get_EventCode():
        scouters_lib.update_event_code(settings_lib.get_EventCode())
    add_scouter_form = AddMemberToTeam_Form()
    if request.method == "POST":
        if add_scouter_form.is_submitted() and add_scouter_form.validate_on_submit and 'submit' in request.form:
            scouters_lib.add_new_scouter(add_scouter_form.MemberName.data)
        elif request.form.get('Names') is not None:
            scouters_lib.delete_scouter(request.form.get('Names'))
        return redirect(url_for('scouters_setup_page'))
        
    return render_template('scouters_setup_page.html',ScoutersNames=scouters_lib.get_all_scouters_names(),districName="District: "+str(settings_lib.get_EventCode()).capitalize(),add_scouter_form=add_scouter_form)


