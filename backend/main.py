import hashlib
import sql
import flask
from flask import jsonify
from flask import request, make_response

# to-do list
'''
    needs login api before this is a true boiler plate for this project (idk how to do it)
'''

#connect to db
connection = sql.create_connection()

# set app name
app = flask.Flask(__name__) # set up app
app.config['DEBUG'] = True # allow to show errors in browser

#Pre-configured username and password
USERNAME = "admin"
PASSWORD = "password"

#waiting for further clarification on log in API 
# Simple authentication function
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

# Login API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username or password missing'}), 400
    
    if authenticate(username, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# FACILTY METHODS

# return all facilities
@app.route('/api/facility/', methods=['GET'])
def get_fac():
    return jsonify(sql.execute_read_query(connection,'SELECT * from facility'))

# add new facility
@app.route('/api/facility/', methods=['POST'])
def add_fac():
    facs = None
    facs = sql.execute_read_query(connection,'SELECT * from facility')

    # new facility id
    request_data =  request.get_json()

    if 'id' not in request_data.keys():
        return 'ERROR: no id provided, please try again'


    new_fac_id = request_data['id']

    for fac in facs:
        if fac['id'] == new_fac_id:
            return "This facility ID already exists, please try again"
    
    # add new facility to db
    cursor = connection.cursor(dictionary=True)
    cursor.execute('INSERT INTO facility VALUES (%s,%s)', (request_data['id'],request_data['name']))
    connection.commit()
    
    return 'Facility successfully added'

# update facility
@app.route('/api/facility/', methods=['PUT'])
def update_fac():
    
    request_data =  request.get_json()

    if 'id' not in request_data.keys():
        return 'ERROR: No id provided. Please try again'

    # facility to be updated
    update_fac_id = request_data['id']

    # update facility in db
    cursor = connection.cursor(dictionary=True)
    cursor.execute('UPDATE facility SET name = %s WHERE id = %s', (request_data['name'],request_data['id']))
    connection.commit()

    return 'Facility successfully updated'

# delete facility
@app.route('/api/facility/', methods=['DELETE'])
def del_fac():
    # facility to be deleted
    request_data = request.get_json()

    if 'id' not in request_data.keys():
        return 'ERROR: No id provided. Please try again'
    
    # update facility in db
    cursor = connection.cursor()
    cursor.execute(f'DELETE from facility WHERE id = {request_data['id']}')
    connection.commit()
    print("Query executed successfully")

    return 'Facility successfully deleted'

# CLASSROOM METHODS
# all classroom methds must have a menu 
# allowing the user to select the facility 
# of the classroom they are trying to access

# return all classrooms
@app.route('/api/classroom/all', methods=['GET'])
def get_classrooms():
    return jsonify(sql.execute_read_query(connection,'SELECT * from classroom'))

# return all classrooms from a specific facility
@app.route('/api/classroom/', methods=['GET'])
def get_classrooms_id():
    classrooms = None
    if 'facility' in request.args: #only if an id is provided, proceed
        facility = int(request.args['facility'])
        classrooms = sql.execute_read_query(connection, 'SELECT * from classroom WHERE facility = %s', facility)
    else:
        return 'ERROR: no facility provided'
    results = [] #resulting classroom(s) to return
    
    for classroom in classrooms:
        if classroom['id'] == id:
            results.append(classroom)
    return jsonify(results)

# add new classroom to db
@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    classrooms = sql.execute_read_query(connection, query=('INSERT INTO classrooms (%s,%s,%s,%s)', (request.args['id'],request.args['capacity'],request.args['name'],request.args['facility']))) # this sql may be wrong / incomplete
    return 'Classroom successfully added!'

# update classroom
@app.route('/api/classroom', methods=['PUT'])
def update_classroom():
    if 'id' in request.args: #only if a facility is provided, proceed
        id = int(request.args['id'])
        classroom = sql.execute_read_query(connection, 'SELECT * FROM classroom WHERE id = %s', (id)) # this sql may be wrong / incomplete

        if 'capacity' in request.args:
            sql.execute_query(connection, query=('UPDATE classroom SET capacity = %s WHERE id = %s', (request.args['capacity'],id)))
        if 'name' in request.args:
            sql.execute_query(connection, query=('UPDATE classroom SET name = %s WHERE id = %s', (request.args['name'],id)))
        if 'room'in request.args:
            sql.execute_query(connection, query=('UPDATE classroom SET room = %s WHERE id = %s', (request.args['room'],id)))
    else:
        return 'ERROR: no classroom ID provided'
    return 'Classroom successfully updated!'

# delete a classroom
@app.route('/api/classroom', methods=['DELETE'])
def del_classroom():
    if 'id' in request.args:
        sql.execute_query(connection,query=('DELETE from classroom WHERE id = %s', request.args['id']))
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Classroom successfully deleted!'

# TEACHER METHODS
# no more than 10 children per teacher
# regardless of classroom capacity

# return all teachers
@app.route('/api/teacher', methods=['GET'])
def get_teachers():
    return jsonify(sql.execute_read_query(connection,'SELECT * from teacher'))
    

# add new teacher
@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    teachers = sql.execute_read_query(connection, query=('INSERT INTO teacher (%s,%s,%s)', (request.args['firstname'],request.args['lastname'],request.args['room_id']))) # this sql may be wrong / incomplete
    return 'Teacher successfully added!'
    

#update teacher
@app.route('/api/teacher', methods=['PUT'])
def update_teacher():
    if 'id' in request.args:  # Only proceed if a teacher ID is provided
        id = int(request.args['id'])
        teacher = sql.execute_read_query(connection, 'SELECT * FROM teacher WHERE id = %s', (id,))

        if not teacher:
            return 'ERROR: Teacher ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, 'UPDATE teacher SET firstname = %s WHERE id = %s', (request.args['firstname'], id))
        if 'lastname' in request.args:
            sql.execute_query(connection, 'UPDATE teacher SET lastname = %s WHERE id = %s', (request.args['lastname'], id))
        if 'room_id' in request.args:
            sql.execute_query(connection, 'UPDATE teacher SET room_id = %s WHERE id = %s', (request.args['room_id'], id))
    else:
        return 'ERROR: no teacher ID provided'
    
    return 'Teacher successfully updated!'

# delete teacher
@app.route('/api/classroom', methods=['DELETE'])
def del_teacher():
    if 'id' in request.args:
        sql.execute_query(connection,query=('DELETE from teacher WHERE id = %s', request.args['id']))
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Classroom successfully deleted!'

# CHILDREN METHODS
# same rules a teacher methods

# return all children 
@app.route('/api/children/all', methods=['GET'])
def get_children():
    return jsonify(sql.execute_read_query(connection,'SELECT * from child'))
    

# add new children
@app.route('/api/children', methods=['POST'])
def add_children():
    Children = sql.execute_read_query(connection, query=('INSERT INTO child (%s,%s,%s)', (request.args['firstname'],request.args['lastname'],request.args['age'],request.args['room_id']))) # this sql may be wrong / incomplete
    return 'Child successfully added to classroom!'

# update children
@app.route('/api/children', methods=['PUT'])
def update_child():
    if 'id' in request.args:  # Only proceed if a child ID is provided
        id = int(request.args['id'])
        child = sql.execute_read_query(connection, 'SELECT * FROM child WHERE id = %s', (id,))

        if not child:
            return 'ERROR: Child ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, 'UPDATE child SET firstname = %s WHERE id = %s', (request.args['firstname'], id))
        if 'lastname' in request.args:
            sql.execute_query(connection, 'UPDATE child SET lastname = %s WHERE id = %s', (request.args['lastname'], id))
        if 'age' in request.args:
            sql.execute_query(connection, 'UPDATE child SET age = %s WHERE id = %s', (request.args['age'], id))
        if 'room_id' in request.args:
            sql.execute_query(connection, 'UPDATE child SET room_id = %s WHERE id = %s', (request.args['room_id'], id))
        
        return 'Child successfully updated!'
    else:
        return 'ERROR: no child ID provided'

# delete child from db
@app.route('/api/children', methods=['DELETE'])
def del_child():
    if 'id' in request.args:
        sql.execute_query(connection,query=('DELETE from child WHERE id = %s', request.args['id']))
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Child successfully removed from classroom!'

app.run()