import xml.etree.ElementTree as ET

class Ipconn: 

    # Possible Values

    # NAME="ZCON9999" 
    # CSDGROUP="PORTTC21"
    # APPLID="ZCONT1"
    # NETWORKID="D001"
    # HOST=""
    # PORT="NO"
    # TCPIPSERVICE="ZCON"
    # RECEIVECOUNT="100"
    # SENDCOUNT="000"
    # QUEUELIMIT="NO"
    # MAXQTIME="NO"
    # MIRRORLIFE="Request"
    # AUTOCONNECT="NO"
    # INSERVICE="YES"
    # HA="NO"
    # SSL="NO"
    # CERTIFICATE=""
    # CIPHERS=""
    # LINKAUTH="SECUSER"
    # SECURITYNAME=""
    # USERAUTH="IDENTIFY"
    # IDPROP="NOTALLOWED"
    # XLNACTION="KEEP" 

    def __init__(self,*args, **kwargs):
        """
        @param name: Name of the IPCONN Definition
        """
        
        self.name = kwargs.get("name","")
        self.description = kwargs.get("description","")
        self.csdgroup = kwargs.get("csdgroup","") 
        self.applid = kwargs.get("applid","") 
        self.networkid = kwargs.get("networkid","") 
        self.host = kwargs.get("host","") 
        self.port = kwargs.get("port","") 
        self.tcpipservice = kwargs.get("tcpipservice","") 
        self.receivecount = kwargs.get("receivecount","100") 
        self.sendcount = kwargs.get("sendcount","000") 
        self.queuelimit = kwargs.get("queuelimit","NO") 
        self.maxqtime = kwargs.get("maxqtime","NO") 
        self.mirrorlife = kwargs.get("mirrorlife","") 
        self.autoconnect = kwargs.get("autoconnect","NO") 
        self.inservice = kwargs.get("inservice","YES") 
        self.ha = kwargs.get("ha","NO") 
        self.ssl = kwargs.get("ssl","NO") 
        self.certificate = kwargs.get("certificate","") 
        self.ciphers = kwargs.get("ciphers","") 
        self.linkauth = kwargs.get("linkauth","") 
        self.securityname = kwargs.get("securityname","") 
        self.userauth = kwargs.get("userauth","") 
        self.idprop = kwargs.get("idprop","") 
        self.xln = kwargs.get("xln","KEEP")
        
        

    def toXML(self):
        attributes = ET.Element('attributes')
        attributes.set('NAME',self.name)
        attributes.set('DESCRIPTION',self.description)
        attributes.set('CSDGROUP',self.csdgroup)
        attributes.set('APPLID',self.applid)
        attributes.set('NETWORKID',self.networkid)
        attributes.set('HOST',self.host)
        attributes.set('PORT',self.port)
        attributes.set('TCPIPSERVICE',self.tcpipservice)
        attributes.set('RECEIVECOUNT',self.receivecount)
        attributes.set('SENDCOUNT',self.sendcount)
        attributes.set('QUEUELIMIT',self.queuelimit)
        attributes.set('MAXQTIME',self.maxqtime)
        attributes.set('MIRRORLIFE',self.mirrorlife)
        attributes.set('AUTOCONNECT',self.autoconnect)
        attributes.set('INSERVICE',self.inservice)
        attributes.set('HA',self.ha)
        attributes.set('SSL',self.ssl)

        if self.ssl == "YES":
            attributes.set('CERTIFICATE',self.linkauth)
            attributes.set('CIPHERS',self.ciphers)
        
        attributes.set('LINKAUTH',self.linkauth)
        attributes.set('SECURITYNAME',self.linkauth)
        attributes.set('USERAUTH',self.userauth)
        attributes.set('IDPROP',self.idprop)
        attributes.set('XLNACTION',self.xln)

        return attributes