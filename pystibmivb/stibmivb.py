import requests
import xmltodict
import json

#version 0.2.4.2
session = requests.Session()

base_url = { 
        'fr':"http://m.stib.be/api/{}.php",
        'nl':"http://m.mivb.be/api/{}.php"
        }


methods = {
    'getitinerary' : ['line', 'iti'],
    'getlinesnew' : [],
    'getwaitingtimes' : ['halt'],
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
          '''Get data from api endpoint'''

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

      def get_waiting_times(self, halt=None):
          '''Retrieve waiting times for a line at a stop id'''
          if halt is not None:
              extra_params = {'halt': halt}
              response_data = self.do_request('getwaitingtimes', extra_params)
              return response_data

      def get_itinerary(self, line=None, iti=1):
          '''Retrieve all stops for a line for a given direction (1 or 2)'''
          if line and iti in [1,2]:
              extra_params = {'line':line, 'iti':iti}
              response_data = self.do_request('getitinerary', extra_params)
              return response_data

      def get_json(self, json_data):
          '''transform xml to dict to json'''
          try:
              json_data = xmltodict.parse(json_data)
          except xmltodict.expat.ExpatError:
              return -1
          json_data = json.dumps(json_data, ensure_ascii=False)
          return json_data

      def get_waiting_times_line(self, halt=None,line=None):
          '''Get waiting times for particular line for a halt id'''
          if None not in [halt,line]:
              waiting_times = []
              halt_data = self.get_waiting_times(halt)
              halt_data = json.loads(halt_data)
              if 'waitingtime' in halt_data['waitingtimes']:
                  wts = halt_data['waitingtimes']['waitingtime']
                  if type(wts) is dict:
                      wts = [wts]
                  for w in wts:
                      if w['line'] == line:
                          waiting_times.append(w)
              else:
                  waiting_times = None
          return waiting_times        

      def get_line_name(self,line):
          '''Get destinations for a line'''
          if line:
              line_name = []
              lines = self.get_lines_new()
              lines = json.loads(lines)
              for l in lines['lines']['line']:
                  if l['id'] == line:
                      line_name.append(l)
              return line_name
                          
      def get_halt_ids_latlon(self, lat=None, lon=None):
          if None not in [lat,lon]:
              halt_ids = []
              halts = self.get_close_stops(lat,lon)
              halts =json.loads(halts)
              if 'halt' in halts['halts']:
                for halt in halts['halts']['halt']:
                    halt_ids.append(halt['id'])
              return halt_ids


      