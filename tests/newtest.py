

from pystibmivb import Stibmivb
import json


stib = Stibmivb()
lat = '50.81635'
lon = '4.3339'
line = '54'
iti = 1
halt = 2955

i = stib.get_waiting_times('5152')
print(i)

a = stib.get_waiting_times_line('5152','54')

print(a)
