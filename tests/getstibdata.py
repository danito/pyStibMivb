from collections import OrderedDict 
from pystibmivb import Stibmivb
import xmltodict

latitude = '50.82141'
longitude = '4.34187'
lang = 'fr'

stib = Stibmivb(lang)
stibdata = {}


def get_waiting_times(line,iti,halt):
    waiting_times_xml = stib.get_waiting_times(line,iti,halt)
    waiting_times = xmltodict.parse(waiting_times_xml)
    w = waiting_times['waitingtimes']
    wt_data = {
            "wt_stope_name": w['stopname'],
            'wt_position_lat':w['position']['latitude'],
            'wt_position_long':w['position']['latitude']
            }
    if 'message' in w:
        wt_data['message']=(w['message'])
    '''Let's check that there are results for this schedule'''
    if 'waitingtime' in waiting_times['waitingtimes']:
        wt =(waiting_times['waitingtimes']['waitingtime'])
        wtd = []
        for w in wt:
            if w['line'] == line:
                waitingtime = {
                        'wt_waitingtime_line' : w['line'],
                        'wt_waitingtime_mode' : w['mode'],
                        'wt_waitingtime_minutes' : w['minutes'],
                        'wt_waitingtime_destination' : w['destination'],
                        }
                wtd.append(waitingtime)
        wt_data['wt_waitingtimes'] = wtd
    return wt_data


'''http://m.stib.be/api/getclosestops.php?latitude=50.82141&longitude=4.34187'''
def get_waiting_times_by_location(latitude, longitude):
    location_data = {}
    stib_data = stib.get_close_stops(latitude,longitude)
    halts = xmltodict.parse(stib_data)
    location_data['halts'] = []
    for halt in halts['halts']['halt']:
        stop_id = halt['id']
        halt_data = {
            'halt_name': halt['name'],
            'halt_id': halt['id'],
            'halt_lat':halt['latitude'],
            'halt_lon': halt['longitude'],
            'halt_destinations':[]
            }
        destinations = halt['destinations']['destination']
        d = []
        if type(destinations) is OrderedDict:
            '''if only one stop, result is OD'''
            d.append(destinations)
            destinations = d 
        for destination in destinations:
            dest_line = destination['line']
            dest_code = destination['destcode']
            halt_destination = {
                'dest_mode' : destination['mode'],
                'dest_line' : destination['line'],
                'dest_code' : destination['destcode'],
                'dest_name' : destination['name']
                }
            waiting_times_data = get_waiting_times(dest_line, dest_code, stop_id)
            halt_destination['dest_waiting_times'] = waiting_times_data
            halt_data['halt_destinations'].append(halt_destination)
        location_data['halts'].append(halt_data)
    return location_data
                      
'''
mystops = stib.get_close_stops(latitude,longitude)
stops = xmltodict.parse(mystops)

print("Waiting times for stops near lat:{}, long:{}".format(latitude, longitude))
for halt in stops['halts']['halt']:
    print(halt['name'], halt['id'])
    lines = halt['destinations']['destination']
    stop_id = halt['id']
    stop_name = halt['name']
    if type(lines) is OrderedDict:
        print(lines['mode'],lines['line'],lines['name'],lines['destcode'])
        waiting_times = stib.get_waiting_times(lines['line'],lines['destcode'],stop_id)
        waiting_times = xmltodict.parse(waiting_times)
        if 'waitingtime' in waiting_times['waitingtimes']:
            wt =(waiting_times['waitingtimes']['waitingtime'])
            for w in wt:
                if w['line'] == lines['line']:
                   print("    ",w['minutes'], w['destination'])
    else:
       for l in lines:
          print (l['mode'],l['line'],l['name'],l['destcode'])
          waiting_times = stib.get_waiting_times(l['line'],l['destcode'],stop_id)
          waiting_times = xmltodict.parse(waiting_times)
          if 'waitingtime' in waiting_times['waitingtimes']:
              wt =(waiting_times['waitingtimes']['waitingtime'])
              for w in wt:
                  if w['line'] == l['line']:
                      print("    ",w['minutes'], w['destination'])
          
    print ("================================")
'''    
def get_default_line(line,iti):
    newlines = stib.get_lines_new()
    newlines = xmltodict.parse(newlines)
    d = ("destination{}".format(iti))
    print(d)
    destination = ''
    lines = newlines['lines']['line']
    for l in lines:
        if l['id'] == line:
            destination = l[d] 
    return destination
        
'''
stop_id = 2957
iti = 1 
line = 54
waiting_times = stib.get_waiting_times(line,iti,stop_id)
waiting_times = xmltodict.parse(waiting_times)
if 'waitingtime' in waiting_times['waitingtimes']:
    wt =(waiting_times['waitingtimes']['waitingtime'])
    stop_name =(waiting_times['waitingtimes']['stopname'])
    print("Waitingtimes for transportation stopping at {}".format(stop_name))
    for w in wt:
        line_dest = get_default_line(w['line'], iti)
        print(w['mode'],w['line'], line_dest)
        print("    ",w['minutes'], w['destination'])


'''
get_data = get_waiting_times_by_location(latitude, longitude)
print(get_data)
