import hashlib
import sql
import flask
from flask import jsonify
from flask import request, make_response

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

# password 'password' hashed
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
masterUsername = 'username'
validTokens = {"100", "200", "300", "400"}

authorizedusers = [
    {
        #default user
        'username': 'username',
        'password': 'password',
        'role': 'default',
        'token': '0',
        'admininfo': None
    },
    {
        #admin user
        'username': 'admin',
        'password': '123450',
        'role': 'admin',
        'token': '1234567890',
        'admininfo': 'michael & daniyal'
    }
]

#basic http authentication, prompts username and password:
@app.route('/authenticatedroute', methods=['GET'])
def auth():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> We are allowed to be here </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

#route to authenticate with username and password against a dataset
@app.route('/api/login', methods = ['GET'])
def usernamepw_example():
    username = request.headers['username'] # get header parameter
    pw = request.headers['password']
    for au in authorizedusers: #loop over users and find authorized on
        if au['username'] == username and au['password'] == pw:
            sessiontoken = au['token']
            adminInfo = au['admininfo']
            returnInfo = []
            returnInfo.append(au['role'])
            returnInfo.append(sessiontoken)
            returnInfo.append(adminInfo)

            return jsonify(returnInfo)
    return 'Security error'

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