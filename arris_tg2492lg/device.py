class Device:
    def __init__(self, ip):
        self.ip = ip
        self.hostname = None
        self.mac = None
        self.adapter_type = None
        self.type = None
        self.lease_end = None
        self.row_status = None
        self.online = None
        self.comment = None
        self.device_name = None
    
    def __str__(self):
        return "ip: %s, hostname: %s" % (self.ip, self.hostname)
