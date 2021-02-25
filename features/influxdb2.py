"""
	Send SMA values influxdb 2.0

	2021-02-25 dervomsee

	Configuration:
	pip3 install influxdb-client

	[SMA-EM]
	# serials of sma-ems the daemon should take notice
	# seperated by space
	serials=30028xxx
	# features could filter serials to, but wouldn't see serials if these serials was not defines in SMA-EM serials
	# list of features to load/run
	features=influxdb2

	[FEATURE-influxdb2]
	debug=0
	url=hostname.tld
	token=long_token
	org=org_name
	bucket=bucket_name
	measurement=SMAEM
	fields=pconsume,psupply,p1consume,p2consume,p3consume,p1supply,p2supply,p3supply

	# How frequently to send updates over (defaults to 20 sec)
	min_update=30

	#pv fields
	pvmeasurement=SMAWR
	pvfields=AC Power,AC_Current,Grid_Frequency
	# How frequently to send updates over (defaults to 20 sec)

"""

import time
import datetime
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteType

influx2_client = InfluxDBClient(url="dummy", token="test", org="", debug=False)
influx2_write_api = influx2_client.write_api(write_options=SYNCHRONOUS)
influx2_last_update = 0
influx2_debug = 0


def run(emparts, config):
	global influx2_debug
	global influx2_last_update
	global influx2_client
	global influx2_write_api

	# Only update every X seconds
	if time.time() < influx2_last_update + int(config.get('min_update', 20)):
		if (influx2_debug > 1):
			print("InfluxDB: data skipping")
		return
	influx2_last_update = time.time()

	mesurement = config.get('measurement', 'SMAEM')
	fields = config.get('fields', 'pconsume,psupply')
	now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	serial = emparts['serial']

	# data fields
	data = {}
	for f in fields.split(','):
		data[f] = emparts.get(f)
		if data[f] is None:
			data[f] = 0.0

	# inverter data
	pvpower = 0
	pdirectusage = 0
	try:
		from features.pvdata import pv_data
		for inv in pv_data:
			# handle missing data during night hours
			if inv.get("AC Power") is None:
				pass
			elif inv.get("DeviceClass") == "Solar Inverter":
				pvpower += inv.get("AC Power", 0)
		pconsume = emparts.get('pconsume', 0)
		psupply = emparts.get('psupply', 0)
		pusage = pvpower + pconsume - psupply

		if pdirectusage is None:
			pdirectusage = 0
		if pvpower > pusage:
			pdirectusage = pusage
		else:
			pdirectusage = pvpower
		data['pdirectusage'] = float(pdirectusage)
		data['pvpower'] = float(pvpower)
		data['pusage'] = float(pusage)
	except:
		# Kostal inverter? (pvdata_kostal_json)
		if influx2_debug > 0:
			print("InfluxDB2: " + "except - no sma - inverter")
		try:
			from features.pvdata_kostal_json import pv_data
			pvpower = pv_data.get("AC Power")
			if pvpower is None:
				pvpower = 0
			pconsume = emparts.get('pconsume', 0)
			psupply = emparts.get('psupply', 0)
			pusage = pvpower + pconsume - psupply
			if pdirectusage is None:
				pdirectusage = 0
			if pvpower > pusage:
				pdirectusage = pusage
			else:
				pdirectusage = pvpower
			data['pdirectusage'] = float(pdirectusage)
			data['pvpower'] = float(pvpower)
			data['pusage'] = float(pusage)
		except:
			pv_data = None
			if influx2_debug > 0:
				print("InfluxDB2: " + "no kostal inverter")
		pass

	# data point
	influx_data = {}
	influx_data['measurement'] = mesurement
	influx_data['time'] = now
	influx_data['tags'] = {}
	influx_data['tags']["serial"] = serial
	influx_data['fields'] = data
	points = [influx_data]

	# write em data
	org = config.get('org', "my-org")
	bucket = config.get('bucket', "my-bucket")
	influx2_write_api.write(bucket, org, points,
							write_precision=WritePrecision.S)

	# prepare pv data
	pvfields = config.get('pvfields')
	pvmeasurement = config.get('pvmeasurement')
	if None in [pvfields, pv_data, pvmeasurement]:
		return
	points = []
	influx_data = []
	datapoint = {
		'measurement': pvmeasurement,
		'time': now,
		'tags': {},
		'fields': {}
	}
	taglist = ['serial', 'DeviceID']
	tags = {}
	fields = {}
	for inv in pv_data:
		# add tag columns and remove from data list
		for t in taglist:
			if inv.get(t) is None:
				pass
			else:
				tags[t] = inv.get(t)
				inv.pop(t)

		# only if we have values
		if pv_data is not None:
			for f in pvfields.split(','):
				if inv.get(f) is None:
					pass
				else:
					fields[f] = inv.get(f, 0)

		datapoint['tags'] = tags.copy()
		datapoint['fields'] = fields.copy()
		influx_data.append(datapoint.copy())

	# write pv data
	points = influx_data
	influx2_write_api.write(bucket, org, points,
							write_precision=WritePrecision.S)


def stopping(emparts, config):
	global influx2_client
	influx2_client.close()
	global influx2_write_api
	influx2_write_api.close()
	pass


def config(config):
	global influx2_debug
	global influx2_client
	global influx2_write_api
	influx2_debug = int(config.get('debug', 0))
	org = config.get('org', "my-org")
	url = config.get('url', "http://localhost:8086")
	token = config.get('token', "my-token")

	# create connection
	influx2_client.close()
	if influx2_debug > 0:
		influx2_client = InfluxDBClient(
			url=url, token=token, org=org, debug=True)
	else:
		influx2_client = InfluxDBClient(
			url=url, token=token, org=org, debug=False)
	influx2_write_api.close()
	influx2_write_api = influx2_client.write_api(write_options=WriteOptions(batch_size=200,
																			flush_interval=120_000,
																			jitter_interval=2_000,
																			retry_interval=5_000,
																			max_retries=5,
																			max_retry_delay=30_000,
																			exponential_base=2))
	print('influxdb2: feature enabled')
