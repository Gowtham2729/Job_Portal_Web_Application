from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db, login_manager
from .models import User, Job
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import Blueprint

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        new_user = User(name=form.name.data, email=form.email.data,
                        phone=form.phone.data, password=hashed_pw, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

import requests
from flask import render_template, request
from flask_login import login_required, current_user

from .forms import PostJobForm  # make sure this is imported at the top

@main.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    form = PostJobForm()
    if form.validate_on_submit() and current_user.role == 'employer':
        job = Job(
            title=form.title.data,
            description=form.description.data,
            salary=form.salary.data,
            location=form.location.data,
            company=form.company.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!')
        return redirect(url_for('main.dashboard'))

    return render_template('post_job.html', form=form, user=current_user)


@main.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('search', '').lower()

    if search_query:
        db_jobs = Job.query.filter(
            (Job.title.ilike(f'%{search_query}%')) |
            (Job.location.ilike(f'%{search_query}%')) |
            (Job.company.ilike(f'%{search_query}%'))
        ).all()
    else:
        db_jobs = Job.query.all()

    # Remotive API
    try:
        resp = requests.get('https://remotive.com/api/remote-jobs?limit=10')
        remotive_data = resp.json().get('jobs', [])
    except:
        remotive_data = []

    # Himalayas API
    try:
        resp2 = requests.get('https://himalayas.app/jobs/api?limit=10')
        himalayas_data = resp2.json().get('jobs', [])
    except:
        himalayas_data = []

    return render_template(
        'dashboard.html',
        user=current_user,
        db_jobs=db_jobs,
        remotive_jobs=remotive_data,
        himalayas_jobs=himalayas_data
    )
from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Job

@main.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.posted_by != current_user.id:
        flash("You are not authorized to delete this job.")
        return redirect(url_for('main.dashboard'))
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.")
    return redirect(url_for('main.dashboard'))


import os
from flask import render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from .forms import ApplicationForm
from .models import Application, Job
from . import db

@main.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplicationForm()
    if form.validate_on_submit():
        resume_file = form.resume.data
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join('D:\VS Code\InnovativeClode_Solutions\Final_Project (working code).zip', filename) # Adjust the path as needed
        os.makedirs(os.path.dirname(resume_path), exist_ok=True)
        print("Saving resume to:", resume_path)  
        resume_file.save(resume_path)

        application = Application(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            resume=filename,
            job_id=job.id,
            job_title=job.title
        )
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('main.login'))  # Or redirect to job list
    return render_template('apply.html', form=form, job=job)

@main.route('/applications')
def view_applications():
    applications = Application.query.all()
    return render_template('view_applications.html', applications=applications)

from flask import send_from_directory

@main.route('/resumes/<filename>')
def view_resume(filename):
    return send_from_directory('static/resumes', filename)
