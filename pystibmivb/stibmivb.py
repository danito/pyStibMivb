import requests
import xmltodict
import json


session = requests.Session()

base_url = { 
        'fr':"http://m.stib.be/api/{}.php",
        'nl':"http://m.mivb.be/api/{}.php"
        }


methods = {
    'getitinerary' : ['line', 'iti'],
    'getlinesnew' : [],
    'getwaitingtimes' : ['line','iti','halt'],
    'getclosestops' : ['latitude','longitude']
    }

headers = {'user-agent': 'pyStibmivb (daniel.nix@gmail.com)'}

    
class Stibmivb:
      
      def __init__(self, lang=None, format=None):
          if format is None:
              format = 'json'
          self.format = format               
          if lang is None:
              lang = 'fr'
          self.lang = lang

      @property
      def format(self):
          return self.__format

      @format.setter
      def format(self, value):
          if value in ['json', 'xml']:
              self.__format = value
          else:
              self.__format = 'json'

      @property
      def lang(self):
          return self.__lang

      @lang.setter
      def lang(self, value):
          if value in ['fr', 'nl']:
              self.__lang = value
          else:
              self.__lang = 'fr'  


      def do_request(self, method, args=None):

          if method in methods:
              url = base_url[self.lang].format(method)
              params = {}
              if args:
                  params = args
              try:
                  response = session.get(url, params = params, headers = headers)
                  try:
                      response_data = response.content
                      if self.format is 'json':
                          print('format : json')
                          response_data = self.get_json(response_data)
                      return response_data
                  except ValueError:
                      return -1
              except requests.exceptions.RequestException as e:
                  print(e)
                  try:
                          session.get('https://1.1.1.1/', timeout=1)
                  except requests.exceptions.ConnectionError:    
                          print("Your internet doesn't seem to be working.")
                          return -1
                  else:
                          print("The Stib API doesn't seem to be working.")
                          return -1

      def get_close_stops (self, latitude=None, longitude=None):
          """Retrieve a list of stops near a waypoint"""
          if latitude is not None and longitude is not None:
              extra_params = {'latitude': latitude, 'longitude':longitude}
              response_data = self.do_request('getclosestops', extra_params)
              return response_data

      def get_lines_new(self):
          """Retrieve all lines."""
          response_data = self.do_request('getlinesnew')
          return response_data

      def get_waiting_times(self, line=None, iti=1, halt=None):
          '''Retrieve waiting times for a line at a stop id'''
          if None not in (line, halt) and iti in [1,2]:
              extra_params = {'line': line, 'iti': iti, 'halt': halt}
              response_data = self.do_request('getwaitingtimes', extra_params)
              return response_data

      def get_itinerary(self, line=None, iti=1):
          '''Retrieve all stops for a line for a given direction (1 or 2)'''
          if line and iti in [1,2]:
              extra_params = {'line':line, 'iti':iti}
              response_data = self.do_request('getitinerary', extra_params)
              return xml_data

      def get_json(self, json_data):
          '''transform xml to dict to json'''
          try:
              json_data = xmltodict.parse(json_data)
          except xmltodict.expat.ExpatError:
              print("ERROR")
              print(json_data)
              return -1
          json_data = json.dumps(json_data, ensure_ascii=False)
          print(json_data)
          return json_data
