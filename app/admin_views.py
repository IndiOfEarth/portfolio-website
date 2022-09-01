import os
from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from app.forms import AuthenticationForm, ImageForm, ProjectForm
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
# Configure application for Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
PATH = r"app/static"

class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), unique=True, nullable=False)
    project_type = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(750), unique=True, nullable=False)
    img_url_1 = db.Column(db.String(250), nullable=False)
    img_url_2 = db.Column(db.String(250), nullable=False)
    img_url_3 = db.Column(db.String(250), nullable=False)
    img_url_4 = db.Column(db.String(250), nullable=False)
    modal_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Portfolio {self.title}>'


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)


# ADMIN SIGN IN FORM HERE - allows access to other routes
@app.route("/admin", methods=["GET", "POST"])
def admin_home():
    # Create an instance of the authentication form for admin login
    authentication_form = AuthenticationForm()
    if authentication_form.validate_on_submit():
        # Get the correct admin username and password
        admin = Admin.query.filter_by(username="ledbetter").first()
        admin_password = admin.password
        if authentication_form.username.data == admin.username and authentication_form.password.data == admin_password:
            login_user(admin)
            flash("Login Successful")
            return redirect(url_for('admin_home'))

    return render_template("admin.html", form=authentication_form, current_user=current_user)


@app.route("/admin/upload-image", methods=["GET", "POST"])
@login_required
def upload_image():
    # Create an instance of the Image Upload form
    upload_form = ImageForm()
    # Handling File Uploads
    if upload_form.validate_on_submit():
        print(upload_form.path.data)
        if upload_form.path.data == "standard":
            uploaded_file = request.files['file']
            # Uploads the image to the UPLOAD_PATH set in config.py
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
            return redirect(url_for('admin_home'))
        elif upload_form.path.data == "other-imgs":
            uploaded_file = request.files['file']
            # Uploads the image to the UPLOAD_PATH set in config.py
            uploaded_file.save(os.path.join('app/static/img/other-imgs', uploaded_file.filename))
            return redirect(url_for('admin_home'))

    return render_template("upload-image.html", current_user=current_user, form=upload_form)



@app.route("/admin/portfolio", methods=["GET", "POST"])
@login_required
def portfolio():
    all_projects = db.session.query(Portfolio).all()
    column_names = Portfolio.__table__.columns.keys()
    project_form = ProjectForm()

    # Handling new portfolio entry
    if project_form.validate_on_submit():
        id = project_form.id.data
        project_name = project_form.project_name.data
        project_type = project_form.project_type.data
        short_desc = project_form.short_desc.data
        description = project_form.description.data
        img_url_1 = project_form.img_url_1.data
        img_url_2 = project_form.img_url_2.data
        img_url_3 = project_form.img_url_3.data
        img_url_4 = project_form.img_url_4.data
        modal_id = project_form.modal_id.data
        # Create a new Portfolio entry in the database
        new_project = Portfolio(id=id,
                                project_name=project_name,
                                project_type=project_type,
                                short_desc=short_desc,
                                description=description,
                                img_url_1=img_url_1,
                                img_url_2=img_url_2,
                                img_url_3=img_url_3,
                                img_url_4=img_url_4,
                                modal_id=modal_id
                                )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('portfolio'))

    return render_template("portfolio.html", portfolio_projects=all_projects, column_names=column_names, project_form=project_form)


@app.route("/delete")
@login_required
def delete():
    project_id = request.args.get('id')
    project_selected = Portfolio.query.get(project_id)
    db.session.delete(project_selected)
    db.session.commit()
    return redirect(url_for('portfolio'))

@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    project_id = request.args.get('id')
    project_selected = Portfolio.query.get(project_id)
    all_projects = db.session.query(Portfolio).all()
    column_names = Portfolio.__table__.columns.keys()
    project_form = ProjectForm()

    if request.method == 'GET':
        project_form.id.data = project_selected.id
        project_form.project_name.data = project_selected.project_name
        project_form.project_type.data = project_selected.project_type
        project_form.short_desc.data = project_selected.short_desc
        project_form.description.data = project_selected.description
        project_form.img_url_1.data = project_selected.img_url_1
        project_form.img_url_2.data = project_selected.img_url_2
        project_form.img_url_3.data = project_selected.img_url_3
        project_form.img_url_4.data = project_selected.img_url_4
        project_form.modal_id.data = project_selected.modal_id
    if project_form.validate_on_submit():
        project_selected.id = project_form.id.data
        project_selected.project_name = project_form.project_name.data
        project_selected.project_type = project_form.project_type.data
        project_selected.short_desc = project_form.short_desc.data
        project_selected.description = project_form.description.data
        project_selected.img_url_1 = project_form.img_url_1.data
        project_selected.img_url_2 = project_form.img_url_2.data
        project_selected.img_url_3 = project_form.img_url_3.data
        project_selected.img_url_4 = project_form.img_url_4.data
        project_selected.modal_id = project_form.modal_id.data
        db.session.commit()
        return redirect(url_for('portfolio'))

    return render_template("portfolio.html", portfolio_projects=all_projects, column_names=column_names,
                           project_form=project_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_home'))