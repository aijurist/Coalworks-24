from flask import Flask
from task_alloc import task_allocation
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(task_allocation, url_prefix='/tasks')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
