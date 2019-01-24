from pystibmivb import Stibmivb
import xmltodict
import json

stib = Stibmivb()


gwt = stib.get_waiting_times(54,1,2955)
gwt = xmltodict.parse(gwt)
g = json.dumps(gwt, ensure_ascii=False)
print(g)
