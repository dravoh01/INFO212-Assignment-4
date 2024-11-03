from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Configure Neo4j connection
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "carrental"

driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def close_connection():
    driver.close()

# Home route
@app.route('/')
def home():
    return "Welcome to the Car Rental API!"

# CRUD for Cars
@app.route('/cars', methods=['GET'])
def get_cars():
    query = "MATCH (c:Car) RETURN id(c) AS id, c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status"
    with driver.session() as session:
        result = session.run(query)
        cars = [dict(record) for record in result]
        return jsonify(cars)

@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    query = "MATCH (c:Car) WHERE id(c) = $id RETURN id(c) AS id, c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status"
    with driver.session() as session:
        result = session.run(query, id=id)
        car = result.single()
        return jsonify(dict(car)) if car else ("Not Found", 404)

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    query = """
    CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: "available"})
    RETURN id(c) AS id, c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status
    """
    with driver.session() as session:
        result = session.run(query, make=data['make'], model=data['model'], year=data['year'], location=data['location'])
        car = result.single()
        return jsonify(dict(car)), 201

@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    updates = request.get_json()
    set_clause = ", ".join([f"c.{key} = ${key}" for key in updates.keys()])
    query = f"MATCH (c:Car) WHERE id(c) = $id SET {set_clause} RETURN id(c) AS id, c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status"
    with driver.session() as session:
        result = session.run(query, id=id, **updates)
        car = result.single()
        return jsonify(dict(car)) if car else ("Not Found", 404)

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    query = "MATCH (c:Car) WHERE id(c) = $id DELETE c"
    with driver.session() as session:
        session.run(query, id=id)
        return ("", 204)

# CRUD for Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    query = "MATCH (cust:Customer) RETURN id(cust) AS id, cust.name AS name, cust.age AS age, cust.address AS address"
    with driver.session() as session:
        result = session.run(query)
        customers = [dict(record) for record in result]
        return jsonify(customers)

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    query = "MATCH (cust:Customer) WHERE id(cust) = $id RETURN id(cust) AS id, cust.name AS name, cust.age AS age, cust.address AS address"
    with driver.session() as session:
        result = session.run(query, id=id)
        customer = result.single()
        return jsonify(dict(customer)) if customer else ("Not Found", 404)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    query = """
    CREATE (cust:Customer {name: $name, age: $age, address: $address})
    RETURN id(cust) AS id, cust.name AS name, cust.age AS age, cust.address AS address
    """
    with driver.session() as session:
        result = session.run(query, name=data['name'], age=data['age'], address=data['address'])
        customer = result.single()
        return jsonify(dict(customer)), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    updates = request.get_json()
    set_clause = ", ".join([f"cust.{key} = ${key}" for key in updates.keys()])
    query = f"MATCH (cust:Customer) WHERE id(cust) = $id SET {set_clause} RETURN id(cust) AS id, cust.name AS name, cust.age AS age, cust.address AS address"
    with driver.session() as session:
        result = session.run(query, id=id, **updates)
        customer = result.single()
        return jsonify(dict(customer)) if customer else ("Not Found", 404)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    query = "MATCH (cust:Customer) WHERE id(cust) = $id DELETE cust"
    with driver.session() as session:
        session.run(query, id=id)
        return ("", 204)

# CRUD for Employees
@app.route('/employees', methods=['GET'])
def get_employees():
    query = "MATCH (e:Employee) RETURN id(e) AS id, e.name AS name, e.address AS address, e.branch AS branch"
    with driver.session() as session:
        result = session.run(query)
        employees = [dict(record) for record in result]
        return jsonify(employees)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    query = "MATCH (e:Employee) WHERE id(e) = $id RETURN id(e) AS id, e.name AS name, e.address AS address, e.branch AS branch"
    with driver.session() as session:
        result = session.run(query, id=id)
        employee = result.single()
        return jsonify(dict(employee)) if employee else ("Not Found", 404)

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    query = """
    CREATE (e:Employee {name: $name, address: $address, branch: $branch})
    RETURN id(e) AS id, e.name AS name, e.address AS address, e.branch AS branch
    """
    with driver.session() as session:
        result = session.run(query, name=data['name'], address=data['address'], branch=data['branch'])
        employee = result.single()
        return jsonify(dict(employee)), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    updates = request.get_json()
    set_clause = ", ".join([f"e.{key} = ${key}" for key in updates.keys()])
    query = f"MATCH (e:Employee) WHERE id(e) = $id SET {set_clause} RETURN id(e) AS id, e.name AS name, e.address AS address, e.branch AS branch"
    with driver.session() as session:
        result = session.run(query, id=id, **updates)
        employee = result.single()
        return jsonify(dict(employee)) if employee else ("Not Found", 404)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    query = "MATCH (e:Employee) WHERE id(e) = $id DELETE e"
    with driver.session() as session:
        session.run(query, id=id)
        return ("", 204)

# Close Neo4j connection
@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection()

# Start Flask app
if __name__ == "__main__":
    app.run(debug=True)
