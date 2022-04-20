import csv,datetime,json,pytz,xml.etree.ElementTree as ET

def update_csv(x,y):
	tree = ET.parse('test_payload1.xml')
	root = tree.getroot()
	root[0][2][0].text=(datetime.datetime.now() + datetime.timedelta(days=x)).strftime('%Y%m%d')
	root[0][2][1].text=(datetime.datetime.now() + datetime.timedelta(days=y)).strftime('%Y%m%d')
	out_xml = ET.tostring(root)
	with open("test_payload2.xml", "wb") as f:
    		f.write(out_xml)

def remove_attribute(x): 
	f = open('test_payload.json')
	data = json.load(f)
	if x in data:
		del data[x]
	if(x in data['inParams']):
		del data['inParams'][x]
	with open("test_payload2.json", "w") as outfile:
    		json.dump(data, outfile)
	f.close()

def read_jmeter_log(file_name):
	file = open(file_name)
	csvreader = csv.reader(file)
	header = next(csvreader)
	for row in csvreader:
		if(not row[3]=='200'):
			if(row[8]==''): 
				row[8]='N/A'

			utc_datetime = datetime.datetime.utcfromtimestamp(float(row[0]) / 1000.)
			row[0] = utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
			print(row[0],row[2],row[3],row[4],row[8],sep=', ')
	file.close()

update_csv(21,23)
remove_attribute('appdate')
read_jmeter_log("Jmeter_log1.jtl")
read_jmeter_log("Jmeter_log2.jtl")