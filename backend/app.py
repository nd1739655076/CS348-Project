from flask import Flask
from models import db
from routes import sessions_bp, courses_bp, instructors_bp, rooms_bp
from report_routes import report_bp
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__, instance_relative_config=True)
CORS(app)


db_path = os.path.join(app.instance_path, 'course_tracker.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)
db.init_app(app)
#migrate = Migrate(app, db)

app.register_blueprint(sessions_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(instructors_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(report_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
