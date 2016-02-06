import gt_app.gts_settings as settings
from flask import Blueprint, render_template, abort, request, redirect, flash
from flask import url_for
from jinja2 import TemplateNotFound
from flask import current_app, session
from models import User, Project, ProjectMemberKey
from models import NotUniqueException
from forms import RegistrationForm, RecaptchaRegistrationForm, LoginForm
from forms import ChangePasswordForm, CreateProjectForm, AddProjectMemberForm
from forms import PrjLoginForm
from flask.ext.login import login_user, login_required
from flask.ext.login import logout_user, current_user
from flask.ext.mail import Message, Mail
from bson.objectid import ObjectId
from multiprocessing import Lock
import utils
from utils import csrf_protect


lock = Lock()

account_views = Blueprint('account', __name__, template_folder='templates',  static_folder='static')

@account_views.route('/signup', methods=['GET','POST'])
def signup():
    debug_set = current_app.config["DEBUG"]   # settings.DEBUG
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> signup() "
    error = None
    
    if settings.RECAPTCHA_ENABLED:
        form = RecaptchaRegistrationForm()
    else:
        form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User.create(username=form.email.data, email=form.email.data,
            firstname=form.firstname.data, middlename=form.middlename.data, 
            lastname=form.lastname.data, password=form.password.data)
        if user is not None:
            user.save()
            flash('Thanks for registering')
            # TODO: Send a validation email.
            return render_template('signup_done.html')
        else:
            error = 'Your email has been already used! Use new email address.'
        
    return render_template('signup.html', form=form, error=error)
    
    
@account_views.route('/login', methods=['GET','POST'])
#@account_views.route('/', alias=True)
def login():
    debug_set = current_app.config["DEBUG"]   # settings.DEBUG
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> login() "
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        email = form.email.data
        password = form.password.data
        user = User.get_with_username(email)

        if user and user.is_active() and not user.is_anonymous():
            if user.authenticate(password):
                login_user(user)
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for(".list_projects"))
            else:
                error = "Your username or password is not valid"
                
    return render_template("login.html", form=form, error=error)


@account_views.route('/logout')
@login_required
def logout():
    logout_user()
    #return render_template('logout.html')  
    return redirect('/')


@account_views.route('/prjlogin', methods=['GET','POST'])
def prj_login():
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> prj_login() "
    error = None
    form = PrjLoginForm()
    print "=====> form: ", form
    if form.validate_on_submit():
        prj_id = form.prj_id.data
        email = form.email.data
        print "=====> prj_id: ",  prj_id
        member = Project.get_project_member(prj_id, email)
        if member is None:
            # This user is not a member of this project
            error = "We can not find your account in this project."
        else:
            # This user is a member and login is successful.
            # Then, set the user's session for 'prj_login' = true
            print 'prj_login(), login successful'
            session['prj_login'] = 'true' 
            return redirect(url_for('dstore.list_member_data', prj_id=prj_id,  mem_email=email))
            
    return render_template("prj_login.html", form=form, error=error)   
    

@account_views.route('/prjlogout', methods=['GET','POST'])
def prj_logout():
    session['prj_login'] = 'false'
    return redirect( url_for('account.prj_login')) 
    

@account_views.route('/userprofile')
@login_required
def view_userprofile():
    return render_template('userprofile.html')  
    

@account_views.route('/projects')
@login_required
def list_projects():
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> list_projects() "
    firstname = current_user.firstname
    lastname = current_user.lastname
    # user's project list
    proj_list = Project.get_projects_for_username(current_user.username)
    return render_template("project_list.html", prj_list=proj_list)


@account_views.route('/verifyemailappkey')
@login_required
def verify_email_appkey():
    return render_template("verify_email_appkey.html")


@account_views.route('/changepassword', methods=['GET','POST'])
@login_required
def change_password():
    '''
    Change a user's password
    '''
    #form = ChangePasswordForm(request.form)
    #if request.method == 'POST' and form.validate():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.update_password(form.new_password.data)
            current_user.save()
            flash("Your password has been updated.", category='index_page')
            return redirect(url_for('.list_projects'))
        else:
            flash("Your password does not match.", category='error')
            return render_template('change_password.html', form=form)    
    return render_template('change_password.html', form=form)


@account_views.route('/projects/add', methods=['GET','POST'])
@login_required
def create_project():
    #with lock:
    #form = CreateProjectForm(request.form)
    #if request.method == 'POST' and form.validate_on_submit():
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> create_project() "
        #print "=====> is_private() :", form.is_private.data

    form = CreateProjectForm()
    if form.validate_on_submit():
        new_proj = Project(prj_name=form.name.data, prj_desc=form.desc.data,
            is_private=form.is_private.data, owner=current_user.get_id())
        prj_id = new_proj.save()
        # Add a user as an owner of a project
        proj = Project.get_project_for_projectid(prj_id)
        print 'project.is_private 2:', proj.is_private
        owner_name = current_user.firstname + ' ' + current_user.lastname
        proj.add_member(name=owner_name, email=current_user.get_id(), 
            role=Project.ROLE_OWNER)
        flash("New project has been created.", category='index_page')
        # Generate a project owner's appkey & save it to ProjectMemberKey coll.
        #keygen = KeyGenerator()
        #key = keygen.getkey(settings.APPKEY_LENGTH)
        key = utils.generate_key()
        prjmemkey = ProjectMemberKey(prj_id=proj.prj_id, appkey=key, 
            member_email=proj.owner)
        prjmemkey.save()
        return redirect(url_for('.list_projects'))

    return render_template('create_project.html', form=form)


@account_views.route('/projects/<prj_id>', methods=['GET','POST'])
@login_required    
def view_project(prj_id):
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> view_project() "
    prj = Project.get_project_for_projectid(prj_id)
    # Read Application Setting to check a project type    
    if settings.SINGLE_PROJECT_MODE and settings.USE_SINGLE_PROJECT_FORM:
        isPublished = True
    else:
        isPublished = False
    
    if prj is not None and (prj.owner == current_user.username):
        memkeys = ProjectMemberKey.get_memberkeys_for_project(prj_id)
        return render_template('project_details.html', prj=prj, memkeys=memkeys,
            isPublished=isPublished)
    
    return render_template('404.html')
    

@account_views.route('/projects/<prj_id>/members/add', methods=['GET','POST'])
@login_required    
def add_project_member(prj_id):
    #form = AddProjectMemberForm(request.form)
    #if request.method == 'POST' and form.validate():
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> add_project_member() "
    form = AddProjectMemberForm()
    if form.validate_on_submit():
        try:
            # Add new member to project
            proj = Project.get_project_for_projectid(prj_id)
            proj.add_member(name=form.name.data, email=form.email.data, 
                role=Project.ROLE_MEMBER)
            # Create an appkey for the new member
            
            key = utils.generate_key(settings.APPKEY_LENGTH)
            prjmemkey = ProjectMemberKey(prj_id=proj.prj_id, appkey=key, 
                member_email=form.email.data)
            prjmemkey.save()
            flash("New member has been added.")
            return redirect(url_for('.view_project', prj_id=prj_id))   
        except NotUniqueException:
            flash("The member email already exists. Can not add it.", 
                category="error")
            return render_template('add_project_member.html', form=form, 
                prj_id=prj_id)
        else:
            print 'Another exception is raised.'
    # if method is GET, show a form.        
    return render_template('add_project_member.html', form=form, prj_id=prj_id)    
    

@account_views.route('/projects/<prj_id>/members/<member_email>/delete', 
    methods=['GET'])
@login_required    
def delete_project_member(prj_id, member_email):
    proj = Project.get_project_for_projectid(prj_id)
    proj.delete_member(member_email)
    return redirect(url_for('.view_project', prj_id=prj_id))    
    
    
@account_views.route('/projects/<prj_id>/members/<member_email>/newappkey', 
    methods=['GET'])
@login_required
def generate_newappkey(prj_id, member_email):
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> generate_newappkey() "
    key = utils.generate_key(settings.APPKEY_LENGTH)
    prjmemkey = ProjectMemberKey(prj_id=prj_id, member_email=member_email,
        appkey=key)
    prjmemkey.save()
    return redirect(url_for('.view_project', prj_id=prj_id))  


@account_views.route('/projects/<prj_id>/members/<member_email>/emailappkey', 
    methods=['GET'])
@login_required     
def email_appkey(prj_id, member_email):
    debug_set = current_app.config["DEBUG"]
    if debug_set == True :
        print "\n\n\n==========> account->views.py -> email_appkey() "
    memkey = ProjectMemberKey.find_one(prj_id=prj_id, member_email=member_email)
    if settings.MAIL_SERVER:
        mail = Mail(current_app._get_current_object())
        message = Message("Your new appkey for 4k mobile app",
            sender='fourkayproject@gmail.com',
            recipients=[member_email])
        message.body = ( 'Project ID: %s \nAppkey: %s' % 
            (prj_id, memkey.appkey) )
        mail.send(message)
        flash("New appkey has been send to your email.", category='info')
    else:
        flash("Can not email because email server is not availalbe. " +  
            "Contact administrator", category='error')
            
    return redirect(url_for('.view_project', prj_id=prj_id))  
    
    
    


