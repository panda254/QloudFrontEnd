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
from py4j.java_gateway import JavaGateway
from xml.dom import minidom

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
    qid = db.createQuestion(question)
    
    ret_json = {}
    ret_json['qid']= qid
    ret_json['question'] = question
    
    return json.dumps(ret_json)

@app.route('/_createAnswer', methods=['GET', 'POST'])
def _createAnswer():
   	qid = request.args.get('qid', '0', type=str)
    	answer = request.args.get('answer', '1' , type=str)
    	db.createAnswer(qid,answer)

    	question_xml= db.readQuestion(qid)
	ret_json = {}
	question_dict = {}
	xmldoc = minidom.parseString(question_xml)
	itemlist = xmldoc.getElementsByTagName('question')
	ret_json['question'] = question_dict
	ret_json['question']['id'] = itemlist[0].attributes['id'].value

	answer_list = xmldoc.getElementsByTagName('answer')
	for answer in answer_list:
		ret_json['question']['answer'+answer.attributes['id'].value] = answer.firstChild.nodeValue			
	    
	return json.dumps(ret_json)
    
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

@app.route('/searchQue')
def searchQue():
	return render_template('searchQue.html')

@app.route('/searchQuestion/<question>')
def searchQuestion(question):
	
	print "here " + question
	try:	
		question_str = db.searchQuestion(question)
	except:
		return render_template('searchQue.html') 
	question_list = question_str.split(';')
	questions = []
	for index,question in enumerate(question_list):
		if (index%2!=0):
			questions.append(question)

	return render_template('searchQue.html',questions=questions)

@app.route('/_searchQuestion', methods=['GET', 'POST'])
def _searchQuestion():
    question = request.args.get('question', '0', type=str)
    try:
    	question_str= db.searchQuestion(question)
    except Exception as e :
	return "No question present"
    question_list = question_str.split(';')
    ret_json = {}
    ret_json['questions'] = []
    for index,question in enumerate(question_list):
		if (index%2!=0):
			x = index/2
			ret_json['questions'][x]['question']=question
		else:
			question_dict = {}
			question_dict['id'] = question
			ret_json['questions'].append(question_dict)
			
    
    return json.dumps(ret_json)

@app.route('/_viewAnswers', methods=['GET', 'POST'])
def _viewAnswers():
    qid = request.args.get('qid', '0', type=str)
    question_xml= db.readQuestion(qid)
    ret_json = {}
    question_dict = {}
    xmldoc = minidom.parseString(question_xml)
    itemlist = xmldoc.getElementsByTagName('question')
    ret_json['question'] = question_dict
    ret_json['question']['id'] = itemlist[0].attributes['id'].value

    answer_list = xmldoc.getElementsByTagName('answer')
    for answer in answer_list:
	ret_json['question']['answer'+answer.attributes['id'].value] = answer.firstChild.nodeValue			
    
    return json.dumps(ret_json)

@app.route('/createAnswer/<answer>/<question>')
def createAnswer(answer,question):
	
	print "in createAnswer " + question	
	question_str = db.searchQuestion(question)
	question_list = question_str.split(';')
	questions = []
	
	db.createAnswer(question_list[0],answer)
	
	print "qid = " + question_list[0]
	print "answer= " + answer
	
	return render_template('editAnswer.html',question=question)
	


@app.route('/writeAnswer/<question>')
def writeAnswer(question):
	
	return render_template('editAnswer.html',question=question)

if __name__ == '__main__':
       # app.run(debug=True)
	gateway = JavaGateway()
	db = gateway.entry_point.getDatabase()
        manager.run()
