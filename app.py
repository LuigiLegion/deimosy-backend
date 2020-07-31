# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from utils import coordinates, find_optimal_path


# Constants
DEFAULT_IMAGE = 'static/images/1.png'


# Initializations
# Create server
app = Flask(__name__)
# Enable CORS
CORS(app)


# Routes
@app.route('/api/path', methods=['POST'])
def path():
    if request.method == 'POST':
        # Extract start and end points coordinates from request
        coords = coordinates(request)
        # Create image from image file path
        img = Image.open(DEFAULT_IMAGE)
        # Find optimal path based on start and end points
        path = find_optimal_path(img, coords)

        return jsonify(path)


# Run server
if __name__ == '__main__':
    app.run()
