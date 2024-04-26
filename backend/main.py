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

#create second_id
def generate_second_id(idSTR):
    result = ''

    for char in idSTR[::1]:
        if char == '0':
            result += 'Z'
        if char == "1":
            result += 'A'
        if char =='2':
            result += 'B'
        if char =='3':
            result += 'C'
        if char =='4':
            result += 'D'
        if char =='5':
            result += 'E'
        if char =='6':
            result += 'F'
        if char =='7':
            result += 'G'
        if char =='8':
            result += 'H'
        if char =='9':
            result += 'I'

    return result


def insert_second_id_all(table):

    ents = sql.execute_read_query(connection,f'SELECT * from {table}')
    for entry in ents:
        second_id = generate_second_id(str(entry.get('id')))
        sql.execute_query(connection, f"UPDATE {table} SET second_id='{second_id}' WHERE id = {entry.get('id')};")

        connection.commit()

# updates second_id for latest entry
def insert_second_id_post(table, entryID):

    second_id = generate_second_id(str(entryID))
    sql.execute_query(connection, f"UPDATE {table} SET second_id='{second_id}' WHERE id = {entryID};")

    

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
@app.route('/api/facility', methods=['GET'])
def get_fac():
    return jsonify(sql.execute_read_query(connection,'SELECT * from facility'))

# add new facility
@app.route('/api/facility', methods=['POST'])
def add_fac():
    facs = None
    facs = sql.execute_read_query(connection,'SELECT * from facility')

    if 'id' not in request.args:
        return 'ERROR: no id provided, please try again'


    new_fac_id = request.args['id']

    for fac in facs:
        if fac['id'] == new_fac_id:
            return "This facility ID already exists, please try again"
    
    # add new facility to db
    cursor = connection.cursor(dictionary=True)
    cursor.execute('INSERT INTO facility VALUES (%s,%s,%s)', (request.args['id'],request.args['name']))

    insert_second_id_post('facility',request.args['id'])
    connection.commit()

    return 'Facility successfully added'

# update facility
@app.route('/api/facility', methods=['PUT'])
def update_fac():

    if 'id' not in request.args:
        return 'ERROR: No id provided. Please try again'

    # facility to be updated
    update_fac_id = request.args['id']

    # update facility in db
    cursor = connection.cursor(dictionary=True)
    cursor.execute('UPDATE facility SET name = %s WHERE id = %s', (request.args['name'],request.args['id']))
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
    
    connection.commit()
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

    insert_second_id_post('classroom',request.args['id'])

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
    
    connection.commit()
    return 'Classroom successfully deleted!'

# TEACHER METHODS
# no more than 10 children per teacher
# regardless of classroom capacity

def class_exists(room):
    classrooms = sql.execute_read_query(connection,'SELECT * from classroom')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(classroom['second_id'] == room for classroom in classrooms):
        return False
    return True

def teacher_exists(teacher_id):
    teachers = sql.execute_read_query(connection,'SELECT * from teacher')
    # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries-in-python
    if not any(teacher['second_id'] == teacher_id for teacher in teachers):
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
    teachers = sql.execute_query(connection, query=f"INSERT INTO teacher (firstname,lastname,room) VALUES ('{request.args['firstname']}','{request.args['lastname']}','{request.args['room']}')")

    all_teachers = sql.execute_read_query(connection, query=f"SELECT * FROM teacher")
    new_teacher_id = all_teachers[-1]['id']
    
    insert_second_id_post('teacher', new_teacher_id)
    connection.commit()
    return 'Teacher successfully added!'
    

#update teacher
@app.route('/api/teacher', methods=['PUT'])
def update_teacher():
    if 'id' in request.args:  # Only proceed if a teacher ID is provided
        if 'room' in request.args and not class_exists(request.args['room']):
            return 'ERROR: Invalid room'
        
        teacher_id = request.args['id']
        teacher = sql.execute_read_query(connection, f"SELECT * FROM teacher WHERE second_id = '{teacher_id}'")

        if not teacher:
            return 'ERROR: Teacher ID not found'

        if 'firstname' in request.args:
            
            sql.execute_query(connection, query=f"UPDATE teacher SET firstname = '{request.args['firstname']}' WHERE second_id = '{teacher_id}'")
            
        if 'lastname' in request.args:
            sql.execute_query(connection, query=f"UPDATE teacher SET lastname = '{request.args['lastname']}' WHERE second_id = '{teacher_id}'")
        if 'room' in request.args:
            sql.execute_query(connection, query=f"UPDATE teacher SET room = '{request.args['room']}' WHERE second_id = '{teacher_id}'")  # Enclose room value in single quotes
    else:
        return 'ERROR: no teacher ID provided'
    
    return 'Teacher successfully updated!'

# delete teacher
@app.route('/api/teacher', methods=['DELETE'])
def del_teacher():
    if 'id' in request.args:
        teacher_id = request.args['id']
        query = f"DELETE FROM teacher WHERE second_id = '{teacher_id}'"
        sql.execute_query(connection, query=query)
        connection.commit()
        return 'Teacher successfully removed!'
    else:
        return 'ERROR: no Teacher ID provided'

# CHILDREN METHODS
# same rules a teacher methods

def too_many_children(room):
    classroom = sql.execute_read_query(connection, f"SELECT * from classroom WHERE id = {room}")

    if not classroom:
        return '400'

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
@app.route('/api/child', methods=['GET'])
def get_children_from_room():
    if 'room' in request.args:
        room = request.args['room']
        return jsonify(sql.execute_read_query(connection, f"SELECT * FROM child WHERE room = '{room}'"))
    
    return 'ERROR: no room provided'

# add new children
@app.route('/api/child', methods=['POST'])
def add_children():
    if 'firstname' not in request.args:
        return 'ERROR: no firstname provided'
    if 'lastname' not in request.args:
        return 'ERROR: no lastname provided'
    if 'room' not in request.args:
        return 'ERROR: no room provided'
    if 'age' not in request.args:
        return 'ERROR: no age provided'

    room = request.args['room']
    if not class_exists(room):
        return 'ERROR: there is no classroom with that id in the database'
    
    room_status_code = too_many_children(room)
    
    if room_status_code == '100':
        return "ERROR: The room with that id is at capacity"
    elif room_status_code == '200':
        return 'ERROR: The room with that id needs another teacher before this student can be added'
    else:
        sql.execute_query(connection, query=f"INSERT INTO child (firstname, lastname, age, room) VALUES ('{request.args['firstname']}','{request.args['lastname']}','{request.args['age']}','{request.args['room']}')")

        all_children = sql.execute_read_query(connection, query=f"SELECT * FROM teacher")
        new_child_id = all_children[-1]['id']
    
        insert_second_id_post('child', new_child_id)

        connection.commit()

        return 'Child successfully added to classroom!'

# update children
@app.route('/api/child', methods=['PUT'])
def update_child():
    if 'id' in request.args:  # Only proceed if a child ID is provided
        if 'room' in request.args and not class_exists(request.args['room']):
            return 'ERROR: Invalid room'
        
        child_id = request.args['id']
        child = sql.execute_read_query(connection, f"SELECT * FROM child WHERE second_id = '{child_id}'")

        if not child:
            return 'ERROR: Child ID not found'

        if 'firstname' in request.args:
            sql.execute_query(connection, query=f"UPDATE child SET firstname = '{request.args['firstname']}' WHERE second_id = '{child_id}'")
        if 'lastname' in request.args:
            sql.execute_query(connection, query=f"UPDATE child SET lastname = '{request.args['lastname']}' WHERE second_id = '{child_id}'")
        if 'age' in request.args:
            sql.execute_query(connection, query=f"UPDATE child SET age = '{request.args['age']}' WHERE second_id = '{child_id}'")       
        if 'room' in request.args:
            sql.execute_query(connection, query=f"UPDATE child SET room = '{request.args['room']}' WHERE second_id = '{child_id}'")  
    else:
        return 'ERROR: no child ID provided'
    
    return 'Child successfully updated!'


# delete child from db
@app.route('/api/child', methods=['DELETE'])
def del_child():
    if 'id' in request.args:
        child_id = request.args['id']
        query = f"DELETE FROM child WHERE second_id = '{child_id}'"
        sql.execute_query(connection, query=query)
        connection.commit()
        return 'Child successfully removed from classroom!'
    else:
        return 'ERROR: no Child ID provided'

app.run()