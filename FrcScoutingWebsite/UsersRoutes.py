from FrcScoutingWebsite import app,db,login_manager,salt
from FrcScoutingWebsite.Forms import LoginForm
from flask import render_template, request, url_for, redirect, session, flash
from FrcScoutingWebsite.Libarys.UsersLib import User
from flask_login import login_required, login_user,logout_user,current_user
import bcrypt
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)



@app.route('/Login',methods=['GET','POST'])
def login_page():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.

    """

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.checkpw(str(form.password.data).encode('utf-8'),user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("index_page"))
        db.session.commit()
    return render_template("login.html", form=form)



@app.route('/Logout')
@login_required
def logout_page():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("index_page"))



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            return current_user.is_admin()
        except:
            return False

class MyModel(ModelView):
    column_display_pk = True
    form_columns = ('username','password','authenticated','role') 
    
    def on_model_change(self, form, model, is_created):
        if len(model.password):
            model.password = bcrypt.hashpw(str(model.password).encode('utf-8'),salt)

    def is_accessible(self):
        try:
            return current_user.is_admin()
        except:
            return False

admin = Admin(app,template_mode='bootstrap3',index_view=MyAdminIndexView())
admin.add_view(MyModel(User, db.session))