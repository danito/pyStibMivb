from pystibmivb import iStibmivb
import xmltodict
from collections import OrderedDict 

latitude = '50.809655'
longitude = '4.320166'
lang = 'fr'

stib = iStibmivb(lang)
stibdata = {}

mystops = stib.get_close_stops(latitude,longitude)
stops = xmltodict.parse(mystops)

for halt in stops['halts']['halt']:
    print(halt['name'], halt['id'])
    lines = halt['destinations']['destination']
    stop_id = halt['id']
    stop_name = halt['name']
    if type(lines) is OrderedDict:
        print(lines['mode'],lines['line'],lines['name'],lines['destcode'])
        waiting_times = stib.get_waiting_times(lines['line'],lines['destcode'],stop_id)
        waiting_times = xmltodict.parse(waiting_times)
        wt =(waiting_times['waitingtimes']['waitingtime'])
        for w in wt:
            if w['line'] == lines['line']:
                print("    ",w['minutes'], w['destination'])
    else:
       for l in lines:
          print (l['mode'],l['line'],l['name'],l['destcode'])
          waiting_times = stib.get_waiting_times(l['line'],l['destcode'],stop_id)
          waiting_times = xmltodict.parse(waiting_times)
          wt =(waiting_times['waitingtimes']['waitingtime'])
          for w in wt:
            if w['line'] == l['line']:
                print("    ",w['minutes'], w['destination'])
          
    print ("================================")
    
