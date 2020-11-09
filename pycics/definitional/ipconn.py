import requests
import xml.etree.ElementTree as ET

# from ..classes import ipconn as i
# x = i.Ipconn(name="a")

def viewIPConnDefinition(host,port,authIn,context,scope,ipconnId):
    
    uri = "/CICSSystemManagement/CICSDefinitionIPICConnection/"+context+"/"+scope+"?CRITERIA=NAME="+ipconnId+"&PARAMETER=CSDGROUP(*)"
    url = "http://"+host+":"+port + uri

    # 'verify=False' to disable ssl certificate verification
    resp = requests.get(url,auth=authIn,verify=False)
    
    # Throw Exception when bad request
    if resp.status_code != 200:
        raise Exception('GET /tasks/ {}'.format(resp.status_code))

    content = resp.content
    root = ET.fromstring(content)

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}resultsummary'):
        api_response1 = record.get('api_response1')
        api_response2 = record.get('api_response2')
        api_response1_alt = record.get('api_response1_alt')
        api_response2_alt = record.get('api_response2_alt')

    
    if (api_response1 != "1024" and api_response1 != "1027"):
        raise Exception('View CSD Definition failed with response code {} ({}) and reason code {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("No IPCONN Definition found")
        
    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitionipicconnection'):
        name    = record.get('name')
        description = record.get('description')
        print(name," => ",description)

def defineIPConnDefinition(host,port,authIn,context,scope,ipconnObject):
    
   # Build XML body for create action

    # Example
    # <request>
    #     <create>
    #        <parameter name="CSD"/>
    #        <attributes 
    #             NAME="ZCON9999" 
    #             CSDGROUP="PORTTC21"
    #             APPLID="ZCONT1"
    #             NETWORKID="D001"
    #             HOST=""
    #             PORT="NO"
    #             TCPIPSERVICE="ZCON"
    #             RECEIVECOUNT="100"
    #             SENDCOUNT="000"
    #             QUEUELIMIT="NO"
    #             MAXQTIME="NO"
    #             MIRRORLIFE="Request"
    #             AUTOCONNECT="NO"
    #             INSERVICE="YES"
    #             HA="NO"
    #             SSL="NO"
    #             LINKAUTH="SECUSER"
    #             USERAUTH="IDENTIFY"
    #             IDPROP="NOTALLOWED"
    #             XLNACTION="KEEP" />
    #     </create>
    # </request>

    request    = ET.Element('request')
    create     = ET.Element('create')
    
    parameter  = ET.Element('parameter')
    parameter.set("name","CSD")
    
    
    # attributes = ET.Element('attributes')
    # attributes.set('NAME',ipconnName)
    # attributes.set('CSDGROUP',csdgroup)
    # attributes.set('APPLID',"")
    # attributes.set('NETWORKID',"")
    # attributes.set('HOST',"")
    # attributes.set('PORT',"")
    # attributes.set('TCPIPSERVICE',"")
    # attributes.set('RECEIVECOUNT',"")
    # attributes.set('SENDCOUNT',"")
    # attributes.set('QUEUELIMIT',"")
    # attributes.set('MAXQTIME',"")
    # attributes.set('MIRRORLIFE',"")
    # attributes.set('AUTOCONNECT',"")
    # attributes.set('INSERVICE',"")
    # attributes.set('HA',"NO")
    # attributes.set('SSL',"")
    # attributes.set('LINKAUTH',"")
    # attributes.set('USERAUTH',"")
    # attributes.set('XLNACTION',"KEEP")

    create.append(parameter)
    create.append(ipconnObject.toXML())
    request.append(create)
    reqBody = ET.tostring(request)

    uri = "/CICSSystemManagement/CICSDefinitionIPICConnection/"+context+"/"+scope
    url = "http://"+host+":"+port + uri

    # 'verify=False' to disable ssl certificate verification
    resp = requests.post(url,reqBody,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('POST /tasks/ {}\n{}'.format(resp.status_code,resp.content))

    content = resp.content
    root = ET.fromstring(content)
    
    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}resultsummary'):
        api_response1 = record.get('api_response1')
        api_response2 = record.get('api_response2')
        api_response1_alt = record.get('api_response1_alt')
        api_response2_alt = record.get('api_response2_alt')

    if (api_response1 != "1024"):
        for error in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}errors'):
            for feedback in error.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}feedback'):
                #print(feedback)
                print(feedback.tag,feedback.attrib)

        raise Exception('Create in CSD failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitionsession'):   
        print("Created {} in group {}".format(ipconnName,csdgroup))
        return record
        # name    = record.get('name')
        # profile = record.get('profile')
        # print(name," => ",profile)

def discardIpconnDefinition(host,port,authIn,context,scope,ipconnName,csdgroup):

    uri = "/CICSSystemManagement/CICSDefinitionIPICConnection/"+context+"/"+scope+"?CRITERIA=NAME="+ipconnName+"&PARAMETER=CSDGROUP("+csdgroup+")"
    url = "http://"+host+":"+port + uri


    # 'verify=False' to disable ssl certificate verification
    resp = requests.delete(url,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('Delete {} {}'.format(uri,resp.status_code))

    content = resp.content
    root = ET.fromstring(content)
    

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}resultsummary'):
        api_response1 = record.get('api_response1')
        api_response2 = record.get('api_response2')
        api_response1_alt = record.get('api_response1_alt')
        api_response2_alt = record.get('api_response2_alt')
        #recordcount = record.get('recordcount')
        #displayed_recordcount = record.get('displayed_recordcount')

    # 1024 => Succesfully Discarded
    # 1027 => No Records found so nothing to discard
    if (api_response1 != "1024" and api_response1 != "1027" ):
        raise Exception('Delete session definition failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("No Session definition found for {} in group {}...".format(sessionName,csdgroup))
    elif api_response1 == "1024":
        print("ipconn",ipconnName,"definition discarded")