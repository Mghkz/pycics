import requests
import xml.etree.ElementTree as ET


def inquireConnections(host,port,authIn,context,scope):
    uri = "/CICSSystemManagement/CICSISCMROConnection/"+context+"/"+scope
    url = "http://"+host+":"+port + uri
    
    connections = []

    # 'verify=False' to disable ssl certificate verification
    resp = requests.get(url,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('Get /tasks/ {}'.format(resp.status_code))

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
        raise Exception('Inquire connections failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("No connections found for {}... ".format(scope))

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsiscmroconnection'):   
        name = record.get('name') # C002
        serverstatus = record.get('servstatus') # INSERVICE 
        netname = record.get('netname') # netname="CICSSC20" 
        
        connection = {
            "name": name,
            "serverstatus": serverstatus,
            "netname": netname
        }
        
        connections.append(connection) 

        # print("termid for",netname,"=>",termId)
    
    return connections

