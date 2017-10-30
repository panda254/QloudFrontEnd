from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, request
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
import os
import requests
import json

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess string'


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():    
    return render_template('index.html')

@app.route('/sendQuestion', methods=['GET', 'POST'])
def sendQuestion():
    question = request.args.get('question', '0', type=str)
    
    print question
    
    return question

@app.route('/askQuestion', methods=['GET', 'POST'])
def askQuestion():
	return render_template('QuestionPage.html')


@app.route('/viewAnswer/<question>')
def viewAnswer(question):
	answers=[]
	answers.append('This is answer 1')
	answers.append('This is answer 2')
	answers.append('This is answer 3')
	answers.append('This is answer 4')

	print "hello"

	return render_template('QuestionPage.html',answers=answers)

if __name__ == '__main__':
       # app.run(debug=True)
        manager.run()
