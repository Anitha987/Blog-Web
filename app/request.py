from app import app
import urllib.request,json
from models import quote

#Getting api key
api_key=app.config['QUOTE_API_KEY']

Quote= quote.Quote