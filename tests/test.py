from pystibmivb import Stibmivb

stib = Stibmivb()
#stib.format = 'xml'
print ("OK")
g = stib.get_waiting_times(54,1,2955)
'''gwt = xmltodict.parse(gwt)
g = json.dumps(gwt, ensure_ascii=False)
'''
print(g)
g = stib.get_waiting_times(54,2,2955)
