from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import math

app = Flask(__name__)
CORS(app)

class Fetcher:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="Quagmire",
            user="postgres",
            password="Yuri.0025",
            host="localhost",
            port="5432"
        )

    def fetch(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()  

class Routes:
    def __init__(self):
        self.cities = []
        self.connections = []
        self.measured_connections = []
    
    def way(self):
        for i in range(len(self.cities)):
            for j in range(i+1, len(self.cities)):
                self.connections.append([self.cities[i], self.cities[j]])
        return self.connections
    
    def measure(self):
        for connection in self.connections:
            A = connection[0][1]
            B = connection[1][1]
            length = math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

            if length < 105:
                self.measured_connections.append(connection)
                    
        return self.measured_connections

fetcher = Fetcher()
path = Routes()

for id, coordenada, nome, região in fetcher.fetch("SELECT id, coords, nomes, regiões FROM cities"):
    path.cities.append([id, coordenada, nome, região])

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(path.cities)

@app.route('/get_measured_connections', methods=['GET'])
def get_measured_connections():
    path.way()
    measured_connections = path.measure()
    return jsonify(measured_connections)

if __name__ == '__main__':
    app.run(debug=True)