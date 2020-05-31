# Imports
import math
from pathfinding.finder.finder import Finder
from flask import Flask, request
from flask_cors import CORS
import json


# Initializations
def calc_cost(self, node_a, node_b):
    """
    Get the cost (absolute value of difference in height) between current node and its neighbor node
    """
    if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
        # Direct neighbor => Difference is 1
        ng = 1
    else:
        # Not a direct neighbor => Diagonal movement
        ng = math.sqrt(2)

    # Weight for weighted algorithms
    if self.weighted:
        # Calculate absolute value of difference in weight (height) between current node and its neighbor node
        ng *= abs(node_a.weight - node_b.weight)

    return node_a.g + ng


Finder.calc_cost = calc_cost


app = Flask(__name__)
CORS(app)


# Routes
@app.route('/path', methods=['POST'])
def path():
    if request.method == 'POST':
        body_str = request.get_json().get('body')
        body_dict = json.loads(body_str)

        start_dict = body_dict['start']
        end_dict = body_dict['end']

        start = (start_dict['x'], start_dict['y'])
        end = (end_dict['x'], end_dict['y'])
        print('start: ', start, 'end: ', end)

        return 'PLACEHOLDER'


if __name__ == '__main__':
    app.debug = True
    app.run()
