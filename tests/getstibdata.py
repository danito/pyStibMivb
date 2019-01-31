from pystibmivb import Stibmivb


stib = Stibmivb()
lat = '50.81635'
lon = '4.3339'
line = 54
iti = 1
halt = 2955
#stib.format = 'xml'
#stib.lang = 'nl'

#http://m.stib.be/api/getlinesnew.php
l = stib.get_lines_new()
print(l)

#http://m.stib.be/api/getitinerary.php?line=54&iti=1
i = stib.get_itinerary(line,iti)
print(i)

#http://m.stib.be/api/getwaitingtimes.php?line=54&iti=2&halt=2955
g = stib.get_waiting_times(line,iti,halt)
print(g)

#http://m.stib.be/api/getclosestops.php?latitude=50.81635&longitude=4.3339
c = stib.get_close_stops(lat,lon)
print(c)


