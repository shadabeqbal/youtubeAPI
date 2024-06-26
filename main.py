from flask import Flask

from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from apscheduler.schedulers.background import BackgroundScheduler
from service.updater import *
import time
from utils.conn import db
from utils.configReader import ConfigReader
from api.routes import api

app = Flask(__name__)

app.register_blueprint(api)
Swagger(app)

config_obj = ConfigReader()
config = config_obj.get_database_config()

DB_USER = config['DB_USER']
DB_PASS = config['DB_PASS']
DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db.init_app(app)

from database.video_details import VideoDetails
from database.trends import Trends
from database.top_keywords import TopKeywords
from database.analyze_metrics import AnalyzeMetrics

with app.app_context():
    try:
        # Check if the connection is established
        db.session.execute(text('SELECT 1'))

        # Create tables if they don't exist
        db.create_all()
        print('Database tables created successfully.')
        print('Database connection established successfully.')

    except Exception as e:
        print('Error connecting to the database:', str(e))

# Set up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_update, 'interval', hours=1)
scheduler.start()
    
if __name__ == '__main__':
    try:   
        app.run(debug=True)
        
        # Keep the scheduler running in the background
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()