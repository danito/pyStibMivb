from pystibmivb import Stibmivb
import json


stib = Stibmivb()
lat = '50.81635'
lon = '4.3339'
line = '54'
iti = 1
halt = ['2955','5720', '5152']


latlon = []

def get_lat_lon(halt):
    wts = stib.get_waiting_times(halt)
    lat=wts[['waitingtimes']['position']['latitude']]
    lon=wts[['waitingtimes']['position']['longitude']]
    return [lat, lon]
        
def get_halt_ids(lat,lon):
    stops = stib.get_close_stops(lat,lon)
    halt_ids = []
    for halt in stops['halts']:
        halt_id.append(halt['id'])
    return halt_ids

def get_zone_lines(lat,lon):
    halts = stib.get_close_stops(lat,lon)
    lines = []
    for halt in halts['halts']:
        destinations = halt['destinations']
        for destination in destinations['destination']:
            line = {line:d['line'],
                    name:d['name'],
                    mode:d['mode']}
        lines.append(line)
    return lines

def get_waiting_times(halt):
    times = stib.get_waiting_times(halt)
    stopname = times['waitingtimes']['stopname']
    time = []
    w = {}
    for t in times['waitingtimes']['waitingtime']:
        if type(t) is dict:
            t = [t]
        line_t_name = "{}{}".format(t['mode'],t['line'])
        if line_t_name is not in w:
            w[line_t_name]=[]
        l = {'line':t['line'],
                'mode':t['mode']
                '
                
                



