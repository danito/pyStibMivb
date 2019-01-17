from stibmivb import iStibmivb
import xmltodict
import pprint
stib = iStibmivb()


mystops = stib.get_lines_new()
dd = xmltodict.parse(mystops)
print (dd['lines']['line'][0])

mystops = stib.get_close_stops('50.807736','4.313616')
print (mystops.decode())
co = xmltodict.parse(mystops)
pprint.pprint(co)
