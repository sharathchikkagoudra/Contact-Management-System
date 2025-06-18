from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='cmsdb',  # Changed database name here
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO contacts (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['first_name'], data['last_name'], data['email'], data['phone']))
        connection.commit()
    connection.close()
    return jsonify({'message': 'Contact added successfully'}), 201

@app.route('/contacts', methods=['GET'])
def get_contacts():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
    connection.close()
    return jsonify(contacts)

@app.route('/contact/<int:id>', methods=['GET'])
def get_contact(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
        contact = cursor.fetchone()
    connection.close()
    if contact:
        return jsonify(contact)
    else:
        return jsonify({'message': 'Contact not found'}), 404

@app.route('/contact/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE contacts SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE id = %s"
        cursor.execute(sql, (data['first_name'], data['last_name'], data['email'], data['phone'], id))
        connection.commit()
    connection.close()
    return jsonify({'message': 'Contact updated successfully'})

@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        connection.commit()
    connection.close()
    return jsonify({'message': 'Contact deleted successfully'})

@app.route('/search', methods=['GET'])
def search_contacts():
    query = request.args.get('q')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM contacts WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s"
        cursor.execute(sql, ('%' + query + '%', '%' + query + '%', '%' + query + '%' ))
        results = cursor.fetchall()
    connection.close()
    return jsonify(results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':  
    app.run(debug=True)
