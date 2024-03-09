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
masterUsername = 'username'
masterPassword = "TeacherPassword"

#waiting for further clarification on log in API 
# Simple authentication function
def authenticate(username, password):
    return username == masterUsername and password == masterPassword

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
@app.route('/api/facility', methods=['DELETE'])
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

def facility_exists(facility_id):
    classrooms = sql.execute_read_query(connection,'SELECT * from classroom')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(classroom['id'] == int(facility_id) for classroom in classrooms):
        return False
    return True

# return all classrooms
@app.route('/api/classroom/all', methods=['GET'])
def get_classrooms():
    return jsonify(sql.execute_read_query(connection,'SELECT * from classroom'))

# return all classrooms from a specific facility
@app.route('/api/classroom', methods=['GET'])
def get_classrooms_id():
    classrooms = None
    if 'facility_id' in request.args: #only if an id is provided, proceed
        facility = int(request.args.get('facility_id'))

        # execute sql query
        classrooms = sql.execute_read_query(connection=connection,query=f'SELECT * from classroom WHERE facility_id = {facility}')

        if len(classrooms) == 0:
            return 'No classrooms were returned'

        # find classroom(s) to return
        results = []
        for classroom in classrooms:
            if classroom['facility_id'] == facility:
                results.append(classroom)
        return results
    
    # no facility error
    elif 'facility_id' not in request.args:
        return 'ERROR: no facility provided'
    

# add new classroom to db
@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    #   check for missing keys
    if ('id' or 'facility_id' or 'name' or 'capacity') not in request.args:
        return 'ERROR: missing key(s), please try again'
    
    facility = int(request.args['facility_id'])
    
    if not facility_exists(facility):
        return 'ERROR: provied facility_id does not exist in database'
    

    classrooms = sql.execute_read_query(connection,f'SELECT * from classroom WHERE facility_id = {facility}')
    for classroom in classrooms:
        if request.args['id'] == classroom['id']:
            return 'ERROR: id provided is already in classroom'
      
    classrooms = sql.execute_query(connection, query=f"INSERT INTO classroom (id,capacity,name,facility_id) VALUES ({request.args['id']},{request.args['capacity']},'{request.args['name']}',{request.args['facility_id']})")

    return 'Classroom successfully added!'

# update classroom
@app.route('/api/classroom', methods=['PUT'])
def update_classroom():
    if 'id' in request.args: #only if a 
        class_id = int(request.args['id'])
        classroom = sql.execute_read_query(connection, f'SELECT * FROM classroom WHERE id = {class_id}') # this sql may be wrong / incomplete

        
        if 'facility_id' in request.args:
            if not facility_exists(request.args['facility_id']):
                return 'ERROR: provied facility_id does not exist in database'
            sql.execute_query(connection, query = f'UPDATE classroom SET facility_id = {request.args['facility_id']}')
        if 'capacity' in request.args:
            sql.execute_query(connection, query=f'UPDATE classroom SET capacity = {request.args['capacity']} WHERE id = {class_id}')
        if 'name' in request.args:
            sql.execute_query(connection, query=f"UPDATE classroom SET name = '{request.args['name']}' WHERE id = {class_id}")
        if 'room' in request.args:
            sql.execute_query(connection, query=f'UPDATE classroom SET room = {request.args['room']} WHERE id = {class_id}')
    else:
        return 'ERROR: no classroom ID provided'
    return 'Classroom successfully updated!'

# delete a classroom
@app.route('/api/classroom', methods=['DELETE'])
def del_classroom():
    if 'id' in request.args:
        classrooms = sql.execute_read_query(connection, 'SELECT * from classroom')
        for classroom in classrooms:
            if classroom['id'] != request.args['id']:
                return 'ERROR: provided id does not exist in database'
        sql.execute_query(connection,query=f'DELETE from classroom WHERE id = {request.args['id']}')
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Classroom successfully deleted!'

# TEACHER METHODS
# no more than 10 children per teacher
# regardless of classroom capacity

def class_exists(room_id):
    teachers = sql.execute_read_query(connection,'SELECT * from teacher')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(teacher['room_id'] == int(room_id) for teacher in teachers):
        return False
    return True

def teacher_exists(teacher_id):
    teachers = sql.execute_read_query(connection,'SELECT * from teacher')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(teacher['id'] == int(teacher_id) for teacher in teachers):
        return False
    return True

# return all teachers
@app.route('/api/teacher', methods=['GET'])
def get_teachers():
    return jsonify(sql.execute_read_query(connection,'SELECT * from teacher'))
    
# add new teacher
@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    if 'room_id' not in request.args:
        return 'ERROR: Please provide a room id'
    if not class_exists(request.args['room_id']):
        return 'ERROR: Invalid room_id'
    if 'firstname' not in request.args:
        return 'ERROR: Please provide a firstname'
    if 'lastname' not in request.args:
        return 'ERROR: Please provide a lastname'
    teachers = sql.execute_query(connection, query=f"INSERT INTO teacher (firstname,lastname,room_id) VALUES ('{request.args['firstname']}','{request.args['lastname']}',{request.args['room_id']})")
    
    return 'Teacher successfully added!'
    

#update teacher
@app.route('/api/teacher', methods=['PUT'])
def update_teacher():
    if 'id' in request.args:  # Only proceed if a teacher ID is provided
        if 'room_id' in request.args and not class_exists(request.args['room_id']):
            return 'ERROR: Invalid room_id'
        
        teacher_id = int(request.args['id'])
        teacher = sql.execute_read_query(connection, f'SELECT * FROM teacher WHERE id = {teacher_id}')

        if not teacher:
            return 'ERROR: Teacher ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, f"UPDATE teacher SET firstname = '{request.args['firstname']}' WHERE id = {teacher_id}")
        if 'lastname' in request.args:
            sql.execute_query(connection, f"UPDATE teacher SET lastname = '{request.args['lastname']}' WHERE id = {teacher_id}")
        if 'room_id' in request.args:
            sql.execute_query(connection, f'UPDATE teacher SET room_id = {request.args['room_id']} WHERE id = {teacher_id}')
    else:
        return 'ERROR: no teacher ID provided'
    
    return 'Teacher successfully updated!'

# delete teacher
@app.route('/api/teacher', methods=['DELETE'])
def del_teacher():
    if 'id' in request.args:
        if not teacher_exists():
            return 'ERROR: Invalid id'
        sql.execute_query(connection,query=f'DELETE from teacher WHERE id = {request.args['id']}')
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Teacher successfully deleted!'

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
        return 'ERROR: no Child ID provided'
    
    return 'Child successfully removed from classroom!'

app.run()