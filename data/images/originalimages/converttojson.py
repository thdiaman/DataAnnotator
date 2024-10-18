import os
import json
import base64
from PIL import Image
from io import BytesIO

for filename in os.listdir("."):
	if filename.endswith(".png"):
		with open(filename, "rb") as image_file:
			data = base64.b64encode(image_file.read())
		im = Image.open(BytesIO(base64.b64decode(data)))
		imjson = {"filename": "./data/images/" + filename, "width": im.size[0], "height": im.size[1], "image": data.decode()}
		with open("../files/" + filename[:-4] + ".json", 'w') as outfile:
			json.dump(imjson, outfile, indent=3)	
