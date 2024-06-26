import configparser

class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.properties')

    def get_database_config(self):
        db_config = {
            'DB_USER': self.config['database']['DB_USERNAME'],
            'DB_PASS': self.config['database']['DB_PASSWORD'],
            'DB_HOST': self.config['database']['DB_HOST'],
            'DB_PORT': self.config['database']['DB_PORT'],
            'DB_NAME': self.config['database']['DB_NAME']
        }
        
        return db_config

    def get_youtube_config(self):
        yt_config = {
            'YOUTUBE_API_SERVICE_NAME': self.config['youtube']['YOUTUBE_API_SERVICE_NAME'],
            'YOUTUBE_API_VERSION': self.config['youtube']['YOUTUBE_API_VERSION'],
            'API_KEY': self.config['youtube']['API_KEY']
        }
        
        return yt_config