import sql
import flask
from flask import jsonify
from flask import request

# to-do list
'''
    create tables in db

    needs login api before this is a true boiler plate for this project (idk how to do it)

    finish all of these methods (obviously)
'''

#connect to db
connection = sql.create_connection()

# set app name
app = flask.Flask(__name__) # set up app
app.config['DEBUG'] = True # allow to show errors in browser

# CLASSROOM METHODS
# all classroom methds must have a menu 
# allowing the user to select the facility 
# of the classroom they are trying to access

# return all classrooms
@app.route('/api/classroom', methods=['GET'])
def get_classrooms():
    return

# add new classroom to db
@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    return

# update classroom
@app.route('/api/classroom', methods=['PUT'])
def update_classroom():
    return

# delete a classroom
@app.route('/api/classroom', methods=['DELETE'])
def del_classroom():
    return

# TEACHER METHODS
# no more than 10 children per teacher
# regardless of classroom capacity

# return all teachers
@app.route('/api/teacher', methods=['GET'])
def get_teachers():
    return

# add new teacher
@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    return

#update teacher
@app.route('/api/teacher', methods=['PUT'])
def update_teacher():
    return

# delete teacher
@app.route('/api/teacher', methods=['DELETE'])
def del_teacher():
    return


# CHILDREN METHODS
# same rules a teacher methods

# return all children 
@app.route('/api/children', methods=['GET'])
def get_children():
    return

# add new children
@app.route('/api/children', methods=['POST'])
def add_children():
    return

# update children
@app.route('/api/children', methods=['PUT'])
def update_child():
    return

# delete child from db
@app.route('/api/children', methods=['DELETE'])
def del_child():
    return

app.run()