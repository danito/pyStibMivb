

from pystibmivb import Stibmivb
import json


stib = Stibmivb()
lat = '50.81635'
lon = '4.3339'
line = '54'
iti = 1
halt = 2955

i = stib.get_waiting_times('2952')
print(i)

a = stib.get_waiting_times_line('2952','54')
print("_______________________")
print(a[0])

print("_______________________")
c = stib.get_line_name('54')

print(c)

h = stib.get_halt_ids_latlon(lat, lon)

print(h)
