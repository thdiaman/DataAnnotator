import os
import json
from flask import Flask, render_template, request
from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter
from properties import datapath, nextpage
formatter = HtmlFormatter()
lex = lexers.get_lexer_by_name("java")

# Run this server with the following command:
# python -m flask --debug --app run run

def parse_value(value, valuetype):
	if valuetype == "CODE":
		return highlight(value, lex, formatter)
	elif valuetype == "URL":
		return "<a href=\"" + value + "\" target=\"_blank\">" + value + "</a>"
	elif valuetype == "PNG":
		return "<img src=\"data:image/jpeg;base64," + value + "\">"
	else:
		return value

def parse_filedata_to_schema(filedata, schema, newfiledata, key=""):
	for field in schema:
		if type(schema[field]) is dict:
			parse_filedata_to_schema(filedata[field], schema[field], newfiledata, key + field + ".")
		elif type(schema[field]) is list:
			if type(schema[field][0]) is dict:
				for v, value in enumerate(filedata[field]):
					parse_filedata_to_schema(value, schema[field][0], newfiledata, key + field + "." + str(v) + ".")
			else:
				for v, value in enumerate(filedata[field]):
					newfiledata[key + field + "." + str(v)] = parse_value(value, schema[field][0])
		else:
			newfiledata[key + field] = parse_value(filedata[field], schema[field])
	return newfiledata

def read_data():
	# Read schema
	with open(os.path.join(datapath, "schema.json")) as infile:
		schema = json.load(infile)

	# Read files	
	files = []
	filespath = os.path.join(datapath, "files")
	for afile in sorted(os.listdir(filespath)):
		with open(os.path.join(filespath, afile)) as infile:
			filedata = json.load(infile)
			newfiledata = {}
			parse_filedata_to_schema(filedata, schema, newfiledata)
			files.append(newfiledata)

	# Read classes
	with open(os.path.join(datapath, "classes.json")) as infile:
		classes = json.load(infile)["classes"]

	# Read annotations
	annotationspath = os.path.join(datapath, "annotations.json")
	if not os.path.exists(annotationspath):
		with open(annotationspath, 'w') as outfile:
			json.dump({"classes": {}, "annotations": {}}, outfile)
	with open(annotationspath) as infile:
		annotations = json.load(infile)
	annotations["classes"] = classes

	# Get id key and create list of ids
	idkey = [k for k, v in schema.items() if v == "ID"][0]
	ids = sorted([afile[idkey] for afile in files])

	# Add default annotation (0) to all files that are not annotated
	annotations["classes"]["0"] = "Non-annotated"
	for afile in files:
		if afile[idkey] not in annotations["annotations"]:
			annotations["annotations"][afile[idkey]] = "0"

	# Return all data
	return ids, files, annotations, classes, schema, idkey

def write_annotations(annotations):
	newannotations = {"classes": annotations["classes"], "annotations": {}}
	for annkey, annvalue in annotations["annotations"].items():
		if annvalue != "0":
			newannotations["annotations"][annkey] = annvalue
	with open(os.path.join(datapath, "annotations.json"), 'w') as outfile:
		json.dump(newannotations, outfile, indent = 3)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	ids, files, annotations, classes, schema, idkey = read_data()
	currentid = request.form.get('comp_select')
	if currentid is None: currentid = ids[0]
	if 'action' in request.form and request.form['action'] == '>':
		currentid = ids[ids.index(currentid) + 1] if ids.index(currentid) + 1 < len(ids) else ids[0]
	if 'action' in request.form and request.form['action'] == '<':
		currentid = ids[ids.index(currentid) - 1] if ids.index(currentid) - 1 >= 0 else ids[len(ids) - 1]

	if currentid is None:
		currentid = files[0][idkey]
	else:
		ann_select = request.form.get('ann_select')
		if ann_select is not None:
			# Add annotation
			annotations["annotations"][currentid] = ann_select
			write_annotations(annotations)
			ids, files, annotations, classes, schema, idkey = read_data()
			if nextpage:
				currentid = ids[ids.index(currentid) + 1] if ids.index(currentid) + 1 < len(ids) else ids[0]

	return render_template('index.html', files={afile[idkey]: afile for afile in files}, currentid=currentid, annotations=annotations, classes=classes, schema=schema)
