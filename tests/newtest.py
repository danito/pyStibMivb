

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
if a:
    print(a)
else:
    print("N/A")


print("_______________________")
c = stib.get_line_name('54')

print(c)
print("_______________________")

h = stib.get_halt_ids_latlon(lat, lon)

print(h)

print("_______________________")

for halt in h:
     halt = list(halt.keys())
     for k in halt:
         print (k)