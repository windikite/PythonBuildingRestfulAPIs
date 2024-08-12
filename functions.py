from flask import jsonify, request
import mysql.connector
from mysql.connector import Error
from password import my_password
from marshmallow import ValidationError

def get_db_connection():
    db_name = 'fitness_center'
    user = 'root'
    password = my_password
    host = 'localhost'

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user=user,
            password=password,
            host=host
        )

        print('Connected to the MySQL database successfully')
        return conn
    except Error as e:
        print(f'Error: {e}')
        return None

def execute_fetch(schema, query):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query)

        results = cursor.fetchall()
        return schema.jsonify(results)
    except Error as e:
        print(f'Error: {e}')
        return jsonify({{'error': 'Internal Server Error'}}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def execute_change(query, variables):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
        cursor.execute(query, variables)
        conn.commit()
        return jsonify({'message': 'Database updated successfully'}), 201
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def validate_request(schema):
    try:
        data = schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    else:
        return data