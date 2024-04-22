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
    if request.authorization:
        encoded = request.authorization.password.encode #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return "<h1> We are allowed to be here </h1>"
    return make_response("COULD NOT VERIFY!", 501, {"WWW-Authenticate" : "Basic realm = Login Required"})

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
@app.route('/api/facility', methods=['GET'])
def get_fac():
    return jsonify(sql.execute_read_query(connection,'SELECT * from facility'))

# add new facility
@app.route('/api/facility', methods=['POST'])
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
@app.route('/api/facility', methods=['PUT'])
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
    if 'id' in request.args:
        facilities = sql.execute_read_query(connection, 'SELECT * FROM facility')
        sql.execute_query(connection, query=f"DELETE FROM facility WHERE id = {request.args['id']}")
    else:
        return 'ERROR: no Facility ID provided'
    
    return 'Facility successfully deleted!'

# CLASSROOM METHODS
# all classroom methds must have a menu 
# allowing the user to select the facility 
# of the classroom they are trying to access

def facility_exists(facility):
    facs = sql.execute_read_query(connection,'SELECT * from facility')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(facility['id'] == int(facility) for fac in facs):
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
    if 'facility' in request.args: #only if an id is provided, proceed
        facility = int(request.args.get('facility'))

        # execute sql query
        classrooms = sql.execute_read_query(connection=connection,query=f'SELECT * from classroom WHERE facility = {facility}')

        if len(classrooms) == 0:
            return 'No classrooms were returned'

        # find classroom(s) to return
        results = []
        for classroom in classrooms:
            if classroom['facility'] == facility:
                results.append(classroom)
        return results
    
    # no facility error
    elif 'facility' not in request.args:
        return 'ERROR: no facility provided'
    

# add new classroom to db
@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    #   check for missing keys
    if ('facility' or 'name' or 'capacity') not in request.args:
        return 'ERROR: missing key(s), please try again'
    
    facility = int(request.args['facility'])
    
    if not facility_exists(facility):
        return 'ERROR: provied facility does not exist in database'
    

    classrooms = sql.execute_read_query(connection,f'SELECT * from classroom WHERE facility = {facility}')
      
    classrooms = sql.execute_query(connection, query=f"INSERT INTO classroom (capacity,name,facility) VALUES ({request.args['capacity']},'{request.args['name']}',{request.args['facility']})")

    return 'Classroom successfully added!'

# update classroom
@app.route('/api/classroom', methods=['PUT'])
def update_classroom():
    if 'id' in request.args:
        class_id = int(request.args['id'])
        classroom = sql.execute_read_query(connection, f'SELECT * FROM classroom WHERE id = {class_id}')

        if not classroom:
            return 'ERROR: Classroom ID not found'

        if 'facility' in request.args:
            if not facility_exists(request.args['facility']):
                return 'ERROR: Provided facility does not exist in the database'
            sql.execute_query(connection, query = f"UPDATE classroom SET facility = '{request.args['facility']}' WHERE id = {class_id}")
        if 'capacity' in request.args:
            sql.execute_query(connection, query=f"UPDATE classroom SET capacity = {request.args['capacity']} WHERE id = {class_id}")
        if 'name' in request.args:
            sql.execute_query(connection, query=f"UPDATE classroom SET name = '{request.args['name']}' WHERE id = {class_id}")
        if 'room' in request.args:
            sql.execute_query(connection, query=f"UPDATE classroom SET room = '{request.args['room']}' WHERE id = {class_id}")

        return 'ERROR: no classroom ID provided'
    return 'Classroom successfully updated!'

# delete a classroom
@app.route('/api/classroom', methods=['DELETE'])
def del_classroom():
    if 'id' in request.args:
        classrooms = sql.execute_read_query(connection, 'SELECT * FROM classroom')
        if not class_exists(request.args['id']):
            return 'ERROR: provided id does not exist in the database'
        sql.execute_query(connection, query=f"DELETE FROM classroom WHERE id = {request.args['id']}")
    else:
        return 'ERROR: no classroom ID provided'
    
    return 'Classroom successfully deleted!'

# TEACHER METHODS
# no more than 10 children per teacher
# regardless of classroom capacity

def class_exists(room):
    classrooms = sql.execute_read_query(connection,'SELECT * from classroom')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(classroom['id'] == int(room) for classroom in classrooms):
        return False
    return True

def teacher_exists(teacher_id):
    teachers = sql.execute_read_query(connection,'SELECT * from teacher')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(teacher['id'] == int(teacher_id) for teacher in teachers):
        return False
    return True

# return all teachers
@app.route('/api/teacher/all', methods=['GET'])
def get_teachers():
    return jsonify(sql.execute_read_query(connection,'SELECT * from teacher'))

#return teachers from one room
@app.route('/api/teacher', methods=['GET'])
def get_teachers_from_room():
    if 'room' in request.args:
        room = request.args['room']
        return jsonify(sql.execute_read_query(connection, f"SELECT * FROM teacher WHERE room = '{room}'"))
    
# add new teacher
@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    if 'room' not in request.args:
        return 'ERROR: Please provide a room id'
    if not class_exists(request.args['room']):
        return 'ERROR: Invalid room'
    if 'firstname' not in request.args:
        return 'ERROR: Please provide a firstname'
    if 'lastname' not in request.args:
        return 'ERROR: Please provide a lastname'
    teachers = sql.execute_query(connection, query=f"INSERT INTO teacher (firstname,lastname,room) VALUES ('{request.args['firstname']}','{request.args['lastname']}',{request.args['room']})")
    
    return 'Teacher successfully added!'
    

#update teacher
@app.route('/api/teacher', methods=['PUT'])
def update_teacher():
    if 'id' in request.args:  # Only proceed if a teacher ID is provided
        if 'room' in request.args and not class_exists(request.args['room']):
            return 'ERROR: Invalid room'
        
        teacher_id = int(request.args['id'])
        teacher = sql.execute_read_query(connection, f'SELECT * FROM teacher WHERE id = {teacher_id}')

        if not teacher:
            return 'ERROR: Teacher ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, f"UPDATE teacher SET firstname = '{request.args['firstname']}' WHERE id = {teacher_id}")
        if 'lastname' in request.args:
            sql.execute_query(connection, f"UPDATE teacher SET lastname = '{request.args['lastname']}' WHERE id = {teacher_id}")
        if 'room' in request.args:
            sql.execute_query(connection, f"UPDATE teacher SET room = '{request.args['room']}' WHERE id = {teacher_id}")  # Enclose room value in single quotes
    else:
        return 'ERROR: no teacher ID provided'
    
    return 'Teacher successfully updated!'

# delete teacher
@app.route('/api/teacher', methods=['DELETE'])
def del_teacher():
    if 'id' in request.args:
        teacher_id = request.args['id']
        query = f"DELETE FROM teacher WHERE id = {teacher_id}"
        sql.execute_query(connection, query=query)
        return 'Teacher successfully removed!'
    else:
        return 'ERROR: no Child ID provided'

# CHILDREN METHODS
# same rules a teacher methods

def too_many_children(room):
    classroom = sql.execute_read_query(f"SELECT * from classrooms WHERE id = {room}")

    children_in_classroom = sql.execute_read_query(connection, f"SELECT * from child WHERE room = {room}")

    teachers_in_classroom = sql.execute_read_query(connection, f"SELECT * from teacher WHERE room = {room}")

    # if too many classrooms have reached capacity
    if len(children_in_classroom) == classroom[0]["capacity"]:
        print(f"Classroom capacity is {classroom[0]['capacity']}")
        return '100'
    
    # if there are not enough teachers
    if len(children_in_classroom)/10 >= len(teachers_in_classroom):
        return '200'


    # if there is room for at least 1 more student in the classroom
    return '000'

# return all children 
@app.route('/api/children/all', methods=['GET'])
def get_children():
    return jsonify(sql.execute_read_query(connection,'SELECT * from child'))

# return all children in a provided room
@app.route('/api/children', methods=['GET'])
def get_children_from_room():
    if 'room' in request.args:
        room = request.args['room']
        return jsonify(sql.execute_read_query(connection, f"SELECT * FROM child WHERE room = '{room}'"))
    
    return 'ERROR: no room provided'
    

# add new children
@app.route('/api/children', methods=['POST'])
def add_children():
    if 'firstname' not in request.args:
        return 'ERROR: no firstname provided'
    if 'lastname' not in request.args:
        return 'ERROR: no lastname provided'
    if 'room' not in request.args:
        return 'ERROR: no room provided'
    if 'age' not in request.args:
        return 'ERROR: no age provided'

    room = int(request.args['room'])
    if not class_exists(room):
        return 'ERROR: there is no classroom with that id in the database'
    
    room_status_code = too_many_children(room)
    
    if room_status_code == '100':
        return "ERROR: The room with that id is at capacity"
    elif room_status_code == '200':
        return 'ERROR: The room with that id needs another teacher before this student can be added'
    else:
        sql.execute_query(connection, query=f"INSERT INTO child (firstname, lastname, age, room) VALUES ('{request.args['firstname']}','{request.args['lastname']}',{request.args['age']},{request.args['room']})") 
        return 'Child successfully added to classroom!'

# update children
@app.route('/api/children', methods=['PUT'])
def update_child():
    if 'id' in request.args:  # Only proceed if a teacher ID is provided
        if 'room_id' in request.args and not class_exists(request.args['room_id']):
            return 'ERROR: Invalid room_id'
        
        child_id = int(request.args['id'])
        child = sql.execute_read_query(connection, f'SELECT * FROM child WHERE id = {child_id}')

        if not child:
            return 'ERROR: Child ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, f"UPDATE child SET firstname = '{request.args['firstname']}' WHERE id = {child_id}")
        if 'lastname' in request.args:
            sql.execute_query(connection, f"UPDATE child SET lastname = '{request.args['lastname']}' WHERE id = {child_id}")
        if 'age' in request.args:
            sql.execute_query(connection, f"UPDATE child SET age = '{request.args['age']} WHERE id = {child_id}")
        if 'room_id' in request.args:
            sql.execute_query(connection, f"UPDATE child SET room_id = {request.args['room_id']} WHERE id = {child_id}")
    else:
        return 'ERROR: no child ID provided'
    
    return 'Child successfully updated!'

# delete child from db
@app.route('/api/children', methods=['DELETE'])
def del_child():
    if 'id' in request.args:
        child_id = request.args['id']
        query = f"DELETE FROM child WHERE id = {child_id}"
        sql.execute_query(connection, query=query)
        return 'Child successfully removed from classroom!'
    else:
        return 'ERROR: no Child ID provided'

app.run()
