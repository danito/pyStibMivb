from pystibmivb import Stibmivb
import json


stib = Stibmivb()
lat = '50.81635'
lon = '4.3339'
line = '54'
iti = 1
halt = 2955
#stib.format = 'xml'
#stib.lang = 'nl'

#http://m.stib.be/api/getlinesnew.php
l = stib.get_lines_new()
l = json.loads(l)

#http://m.stib.be/api/getitinerary.php?line=54&iti=1
i = stib.get_itinerary(line,iti)
i = json.loads(i)

#http://m.stib.be/api/getwaitingtimes.php?line=54&iti=2&halt=2955
t = stib.get_waiting_times(line,iti,halt)
t = json.loads(t)

#http://m.stib.be/api/getclosestops.php?latitude=50.81635&longitude=4.3339
c = stib.get_close_stops(lat,lon)
c = json.loads(c)

'''get destination halt name for line'''
for ld in l['lines']['line']:
    if ld['id'] == line:
        line_name = [ld['destination1'], ld['destination2']]
        mode = ld['mode']

'''get waitingtimes for line'''
wtd = []
stopname = t['waitingtimes']['stopname']
for wt in t['waitingtimes']['waitingtime']:
    if wt['line'] == line:
        wtd.append(wt)

t = iti - 1
print ("{}".format(stopname))
print ("  {}{} - {}".format(mode,line,line_name[t]))
for d in wtd:
    print("    {} - {}".format(d['destination'],d['minutes']))


lat = '50.82166'
lon = '4.34163'
c = stib.get_close_stops(lat,lon)
c = json.loads(c)
h = {}
for halt in c['halts']['halt']:
    halt_name = halt['name']
    halt_id = halt['id']
    if halt_name not in h:
        h[halt_name] = []
    if type(halt['destinations']['destination']) is not dict:
        halt_iti= halt['destinations']['destination'][0]['destcode']
        halt_line= halt['destinations']['destination'][0]['line']
        halt_mode= halt['destinations']['destination'][0]['mode']
        halt_dest= halt['destinations']['destination'][0]['name']
    else:
        halt_iti= halt['destinations']['destination']['destcode']
        halt_line= halt['destinations']['destination']['line']
        halt_mode= halt['destinations']['destination']['mode']
        halt_dest= halt['destinations']['destination']['name']

    hd = [halt_line, halt_mode, halt_iti, halt_dest]
    h[halt_name].append(hd)

print(h)
