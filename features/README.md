# SMA-EM daemon features

this page should give an overview of available features.
I could not test all features, because I do not have the appropriate hardware / software.

All the desired features must be activated in the configuration file
```
[SMA-EM]
# list of features to load/run
features=simplefswriter nextfeature
```
Each feature has it own configuration section  in the configuration-file.

[FEATURE-featurename]

please have a look at the config.sample file or have a look at the features file (description) for supported configuration options.

```
[FEATURE-simplefswriter]
# list serials simplefswriter notice
serials=1900204522
# measurement vars simplefswriter should write to filesystem (only from smas with serial in serials)
values=pconsume psupply qsupply ssupply
```

Feature fist

## domoticz.py
send SMA-measurement-values to domoticz.

## influxdb.py
send SMA-measurement-values to an influxdb.

## mqtt.py
send SMA-measurement-values to an mqtt broker.

## pvdata.py
read sma inverter values via modbus.

## pvdata_kostal_json.py
read kostal piko inverter values via http/json.

## remotedebug.py
allow remote debug with PyCharm.

## sample.py
a sample file; how to start writing a feature

## simplefswriter.py
writes configureable measurement-values to the filesystem

## sma_grafana.json
example grafana configuration to display SAM-measurement-values stored in influxdb

## smamodbus.py
sma modbus library (required for pvdata.py)

## symcon.py
send SMA-measurement-values to symcon

## symcon_smaem_webhook.php
symcon webhook (required for symcon.py)

## symcon_smawr_webhook.php
symcon webhook (required for symcon.py)

## influxdb2.py
send SMA-measurement-values to an influxdb2.

## ediplugs.py
get power consumption values of Edimax smartplugs
