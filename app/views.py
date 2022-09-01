# importing the 'app' from the __init__.py
from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

directory = r'app/static/img/other-imgs'
other_imgs = []
for filename in os.listdir(directory):
    other_imgs.append(filename)

db = SQLAlchemy(app)


# Creating a 'Portfolio' Table
class Portfolio(db.Model):
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


# db.create_all()


@app.route("/")
def home():
    all_projects = db.session.query(Portfolio).all()
    print(app.config['ENV'])
    return render_template('index.html', portfolio_projects=all_projects, imgs=other_imgs)


@app.route("/download")
def download_cv():
    pass