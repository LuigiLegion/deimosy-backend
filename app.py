# Imports
from flask import Flask

# Initializations
app = Flask(__name__)


# Routes
@app.route('/path')
def index():
    return 'PLACEHOLDER'


if __name__ == '__main__':
    app.debug = True
    app.run()
