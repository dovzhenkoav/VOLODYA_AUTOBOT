"""
Settings file needs to keep project constants.
"""
import os


BOT_TOKEN = os.getenv('VOLODYA_AUTOBOT_TOKEN')
BOT_ID = '6369095971'
DB_NAME = os.path.join('data', 'volodya.db')
