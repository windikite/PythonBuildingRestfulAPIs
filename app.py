from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields
from functions import get_db_connection, execute_fetch, execute_change, validate_request


app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ('id', 'name', 'age')

member_schema = MemberSchema()
members_schema  = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    session_id = fields.Integer(dump_only=True)
    member_id = fields.String(required=True)
    session_date = fields.String(required=True)
    session_time = fields.Integer(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'session_time', 'activity')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema  = WorkoutSessionSchema(many=True)

@app.route('/')
def home():
    return 'Welcome to my flask site!'

# members
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    return execute_fetch(members_schema, f"SELECT * FROM Members WHERE id = {id}")

@app.route('/members', methods=['GET'])
def get_members():
    return execute_fetch(members_schema, "SELECT * FROM Members")

@app.route('/members', methods=['POST'])
def add_member():
    member_data = validate_request(member_schema)
    if member_data:
        query = "INSERT INTO Members (name, age) VALUES (%s, %s)"
        variables = (member_data['name'], member_data['age'])
        return execute_change(query, variables)
    else:
        return jsonify({'error': 'Session data unable to be validated'}), 500

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member_data = validate_request(member_schema)
    if member_data:
        query = "UPDATE Members SET name = %s, age = %s WHERE id = %s"
        variables = (member_data['name'], member_data['age'], id)
        return execute_change(query, variables)
    else:
        return jsonify({'error': 'Session data unable to be validated'}), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = get_db_connection()
    if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    member_to_remove = (id, )
    cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_remove)
    member = cursor.fetchone()
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return execute_change("DELETE FROM Members WHERE id = %s", member_to_remove)

# workout sessions
@app.route('/sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    return execute_fetch(workout_sessions_schema, f"SELECT * FROM WorkoutSessions WHERE session_id = {id}")

@app.route('/sessions', methods=['GET'])
def get_workout_sessions():
    return execute_fetch(workout_sessions_schema, "SELECT * FROM WorkoutSessions")

@app.route('/sessions_by_member/<int:id>', methods=['GET'])
def get_workout_sessions_by_member(id):
    if request.method != 'GET':
        return jsonify({'error': 'Method Not Allowed'}), 405
    return execute_fetch(workout_sessions_schema, f"SELECT * FROM WorkoutSessions WHERE member_id = {id}")

@app.route('/sessions', methods=['POST'])
def add_workout_session():
    workout_session_data = validate_request(workout_session_schema)
    if workout_session_data:
        query = "INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s)"
        variables = (workout_session_data['member_id'], 
            workout_session_data['session_date'], 
            workout_session_data['session_time'], 
            workout_session_data['activity'])
        return execute_change(query, variables)
    else:
        return jsonify({'error': 'Session data unable to be validated'}), 500

@app.route('/sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    workout_session_data = validate_request(workout_session_schema)
    if workout_session_data:
        query = "UPDATE WorkoutSessions SET member_id = %s, session_date = %s, session_time = %s, activity = %s WHERE session_id = %s"
        variables = (workout_session_data['member_id'], 
            workout_session_data['session_date'], 
            workout_session_data['session_time'], 
            workout_session_data['activity'],
            id)
        return execute_change(query, variables)
    else:
        return jsonify({'error': 'Session data unable to be validated'}), 500

@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    conn = get_db_connection()
    if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    workout_session_to_remove = (id, )
    cursor.execute("SELECT * FROM WorkoutSessions WHERE session_id = %s", workout_session_to_remove)
    workout_session = cursor.fetchone()
    if not workout_session:
        return jsonify({"error": "Workout Session not found"}), 404
    return execute_change("DELETE FROM WorkoutSessions WHERE session_id = %s", workout_session_to_remove)


if __name__ == '__main__':
    app.run(debug=True)