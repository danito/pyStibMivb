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


