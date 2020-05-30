# Imports
import math
from pathfinding.finder.finder import Finder
from flask import Flask


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


# Routes
@app.route('/path')
def index():
    return 'PLACEHOLDER'


if __name__ == '__main__':
    app.debug = True
    app.run()
