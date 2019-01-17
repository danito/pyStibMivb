import requests

session = requests.Session()

base_url = "http://m.stib.be/api/{}.php"

methods = {
    'getitinerary' : ['line', 'iti'],
    'getlinesnew' : [],
    'getwaitingtimes' : ['line','iti','halt'],
    'getclosestops' : ['latitude','longitude']
    }

headers = {'user-agent': 'pyStibmivb (daniel.nix@gmail.com)'}

    
class iStibmivb:

      def __init__(self, format=None):
          if format is None:
              format = "xml"
          self.format = format
          
      @property
      def format(self):
          return self.__format

      @format.setter
      def format(self, value):
          if value in ['xml', 'json']:
              self.__format = value
          else:
              self.__format = 'json'

      def do_request(self, method, args=None):
          if method in methods:
              url = base_url.format(method)
              params = {}
              if args:
                  params = args
              try:
                  response = session.get(url, params = params, headers = headers)
                  try:
                      xml_data = response.content
                      return xml_data
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
          print("latitude", latitude)
          if latitude is not None and  longitude is not None:
              extra_params = {'latitude': latitude, 'longitude':longitude}
              xml_data = self.do_request('getclosestops', extra_params)
              return xml_data

      def get_lines_new(self):
          """Retrieve all lines."""
          xml_data = self.do_request('getlinesnew')
          return xml_data

      def get_waiting_times(self, line=None, iti=None, halt=None):
          if bool(line) ^ bool(halt):
              extra_params = {'line': line, 'iti': iti, 'halt': halt}
              xml_data = self.do_request('getwaitingtimes', extra_params)
              return xml_data

      def get_itinerary(self, line=None, iti=1):
          if line:
              extra_params = {'line':line, 'iti':iti}
              xml_data = self.do_request('getitinerary', extra_params)
              return xml_data
