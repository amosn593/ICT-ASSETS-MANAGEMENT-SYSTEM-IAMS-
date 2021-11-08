import socket

if socket.gethostname() == "AMOC":
    from .local import *
else:
    from .production import *
