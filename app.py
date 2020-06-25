# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import math
from PIL import Image
from pathfinding.finder.finder import Finder
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


# Constants
DEFAULT_IMAGE = 'static/1.png'


# Initializations
def calc_cost(self, node_a, node_b):
    """
    Get the cost (absolute value of difference in height) between current node and its neighbor node
    """
    if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
        # Direct neighbor => Difference is 1
        ng = 1
    else:
        # Not direct neighbor => Diagonal movement
        ng = math.sqrt(2)

    # Weight for weighted algorithms
    if self.weighted:
        # Calculate absolute value of difference in weight (height) between current node and its neighbor node
        ng *= abs(node_a.weight - node_b.weight)

    return node_a.g + ng


# Monkey patch my variant of calc_cost method to pathfinding Finder class
Finder.calc_cost = calc_cost

# Create server
app = Flask(__name__)

# Enable CORS
CORS(app)


# Routes
@app.route('/path', methods=['POST'])
def path():
    if request.method == 'POST':
        # Extract start and end points coordinates from request
        coords = coordinates(request)
        # Create image from image file path
        img = Image.open(DEFAULT_IMAGE)
        # Find optimal path based on start and end points
        path = find_optimal_path(img, coords)

        return jsonify(path)


# Utilities
def coordinates(req):
    # Extract body string from request JSON
    body_str = req.get_json().get('body')
    # Deserialize body string into dictionary
    body_dict = json.loads(body_str)
    # Extract start and end points key-value pairs from body dictrionary
    start_dict = body_dict['start']
    end_dict = body_dict['end']
    # Create start and end coordinate tuples from start and end point dictrionaries
    start = (start_dict['x'], start_dict['y'])
    end = (end_dict['x'], end_dict['y'])
    # Store start and end coordinates in list
    coords = [start, end]

    return coords


def matrix(img):
    # Create grayscale image from image
    grayscale_img = img.convert('L')
    # Create list from grayscale image
    data = list(grayscale_img.getdata())
    # Extract width and height from image
    width, height = grayscale_img.size
    # Create matrix from grayscale image using its data and size
    mtrx = [data[offset:offset + width]
            for offset in range(0, width * height, width)]

    return mtrx


def optimal_path(mtrx, coords):
    print('Start point: ', coords[0])
    print('End point: ', coords[1], '\n')

    # Create grid from matrix
    grid = Grid(matrix=mtrx)
    # Create start and end point nodes from coordinates
    start = grid.node(coords[0][0], coords[0][1])
    end = grid.node(coords[1][0], coords[1][1])
    # Initialize finder as instance of AStarFinder that allows for diagonal movement
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    # Find optimal path and number of runs between start and end points
    path, runs = finder.find_path(start, end, grid)

    print('Number of runs: ', runs)
    print('Path length: ', len(path), '\n')

    return path


def find_optimal_path(img, coords):
    # Create matrix from image
    mtrx = matrix(img)
    # Find optimal path in matrix
    path = optimal_path(mtrx, coords)

    return path


if __name__ == '__main__':
    app.run()
