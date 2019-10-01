# from app import app
import urllib.request,json
from .models import Quote
import requests

#Getting api key

# api_key=None

# Quote= quote.Quote

# Getting the movie base url
base_url=None

def configure_request(app):
  global base_url
  base_url = app.config["QUOTE_API_BASE_URL"]
  

def get_quotes(category):
  '''
  Function that gets the json response to our url request
  '''
  # get_quotes_url = base_url.format(QUOTE_API_BASE_URL)

  with urllib.request.urlopen(base_url) as url:
    get_quotes_data = url.read()
    get_quotes_response = json.loads(get_quotes_data)
    print(get_quotes_response)
    quote_results = None

    if get_quotes_response:
      id=get_quotes_response.get('id')
      author=get_quotes_response.get('author')
      quote=get_quotes_response.get('quote')
      quote_results = Quote(id,author,quote)
  return quote_results

# def process_results(quote_list):
#   '''
#   Function  that processes the quote result and transform them to a list of Objects

#   Args:
#     quote_list: A list of dictionaries that contain quote details

#   Returns :
#     quote_results: A list of quote objects
#   '''
#   quote_results = []
#   for quote_item in quote_list:
#     id = quote_item.get('id')
#     author = quote_item.get('author')
#     quote= quote_item.get('quote')

  

#   return quote_results  