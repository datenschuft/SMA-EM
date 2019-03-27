SMA-EM-Daemon contributors
============================================

* **[Wenger Florian](https://github.com/datenschuft)**

  * Initiator
  * Author and maintainer

* **[jhagberg](https://github.com/jhagberg)**

  * Encoding-hints

* **[mzealey](https://github.com/mzealey)**

  * domoticz support

* **[Tommi2Day](https://github.com/Tommi2Day)**

  * many modifications to enhance this tool to meke more configurable to allow developing und running on windows and add a new mqtt feature and a remote debug feature
  * "pvdata" for getting PV data from SMA Inverters via Modbus along SMA-EM/HM
  * "mqtt" to send SMA EM and PV data to an MQTT broker
  * "remotedebug" to allow remote debug from PyCharm
  * "influxdb" and sample grafana dashboard based on this plugin
  * "symcon" to supply SMA EM/HOM and PV data to "IP-Symcon" 

* **[david-m-m](https://github.com/david-m-m)**

  * rewrite SMA HM2.0 datagram parser
  * parse SMA EMETER datagrams
  * enhance mqtt module to export topics for all metrics, works with [mqtt_exporter](https://github.com/bendikwa/mqtt_exporter)
