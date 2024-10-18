import os
import json
import xmltodict

for filename in os.listdir("."):
	if filename.endswith(".xml"):
		with open(filename, "r") as xml_file:
			data = xml_file.read()
		jdata = xmltodict.parse(data)["root"]
		with open("../files/" + filename[:-4] + ".json", 'w') as outfile:
			json.dump(jdata, outfile, indent=3)	
