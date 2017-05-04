## Known Problems
Systemd starts daemon to early

systemd[1]: Started SMA Energymeter measurement daemon.
sma-daemon.py[574]: Traceback (most recent call last):
sma-daemon.py[574]: File "/opt/smaem/sma-daemon.py", line 24, in <module>
sma-daemon.py[574]: import smaem
sma-daemon.py[574]: File "/opt/smaem/smaem.py", line 49, in <module>
sma-daemon.py[574]: sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sma-daemon.py[574]: OSError: [Errno 19] No such device
systemd[1]: smaemd.service: main process exited, code=exited, status=1/FAILURE

should create a .socket file with ListenNetlink= MCastGroup
need to import more systemd - stuff to brain.
