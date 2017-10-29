Student Portal For Addition And Substitution
============================================

Assignment:- Student Portal, that has functionality of adding and substituting courses

Folders
--------

a) static:- contains all the static files like icon, images etc
b) templates:- contains all the HTML files
c) venv:- The virtual enviroment that has all the dependencies installed.


Important Files 
----------------

a) courses_info.json:- The database for the courses, Contains all the information about the courses like instructor name, course code etc
b) users.json:- Contains the database of the students, the courses they are registered in.
c) portal.py:- The main application


How to run the application -

a) Open the terminal. Go to the directory of the application. 
b) Activate the virtual environement by  "source venv/bin/activate"
c) To run the application as a localhost run the command "python portal.py runserver"
   To make your system as server and host the application run the command "python portal.py runserver --host=' < your_ip >'"


RESTAPIs.txt contains information about the REST APIs provided for addition substitution and viewing or courses.