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
t = stib.get_waiting_times(halt)
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
ids = []
for halt in c['halts']['halt']:
    halt_name = halt['name']
    halt_id = halt['id']
    ids.append(halt_id)
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

    hd = [halt_id,halt_line, halt_mode, halt_iti, halt_dest]
    h[halt_name].append(hd)

print(h)
print(ids)
wts=[]
for i in ids:
    wts.append(stib.get_waiting_times(i))

print("_______")


class STIBgetIDs():
    '''Get halt ids from lat/lon'''

    def __init__(self, latitude, longitude, api_client):
        self.api_client = api_client
        self.latitude = latitude
        self.longitude = longitude

    def update(self):
        response = self.api_client.get_close_stops(self.latitude,self.longitude)
        response = json.loads(response)
        ids = []
        for halt in response['halts']['halt']:
            ids.append(halt['id'])

        return ids

class STIBgetData():

    def __init__(self, halts, api_client):
        self.api_client = api_client
        self.halts = halts

    def get_halt_data(self):
        wts = []
        w = {}
        ht = {}
        for halt in self.halts:
            wt = self.api_client.get_waiting_times(halt)
            wt = json.loads(wt)
            if 'waitingtimes' in wt:
                wt = wt['waitingtimes']
                w['id']=halt
                w['stopname'] = wt['stopname']
                if 'waitingtime' in wt:
                    lines = wt['waitingtime']
                    if type(lines) is dict:
                        lines = [lines]
                    l = {}
                    for line in lines:
                        line_id = line['line']
                        line_mode = line['mode']
                        line_minutes = line['minutes']
                        line_dest = line['destination']
                        line_t_name = "{}{}".format(line_mode,line_id)
                        t = {'line_id': line_id,
                                'line_mode' : line_mode,
                                'line_minutes' : line_minutes,
                                'line_dest' : line_dest }
                        if line_t_name not in w:
                            w[line_t_name]=[]
                        w[line_t_name].append(t)
                        if halt not in ht:
                            ht[halt]=[]
                            ht[halt].append(w)
        return wts

class STIBgetLine():
    
    def __init__(self, line, api_client):
        self.api_client = api_client
        self.line = line

    def get_line_name(self):
        lines = self.api_client.get_lines_new()
        lines = json.loads(lines)
        ln = []
        for l in lines['lines']['line']:
            if l['id'] == self.line:
                d1 = "{}{} - {}".format(l['mode'],line,l['destination1'])
                d2 = "{}{} - {}".format(l['mode'],line,l['destination2'])
                ln = [d1,d2]

        return ln

t = STIBgetIDs(lat,lon,stib)
r = (t.update())

s = STIBgetData(r, stib)
p = s.get_halt_data()
l = STIBgetLine('54',stib)
ln = l.get_line_name()
print(ln)
