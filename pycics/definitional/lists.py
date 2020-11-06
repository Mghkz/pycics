import requests
import xml.etree.ElementTree as ET

def getGroupsInList(host,port,authIn,context,scope,csdlist):
    
    uri = "/CICSSystemManagement/CICSCSDGroupInList/"+context+"/"+scope+"?CRITERIA=CSDLIST="+csdlist
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

    
    if (api_response1 != "1024"):
        raise Exception('View CSD Definition failed with response code {} ({}) and reason code {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
        
    groups = []

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicscsdgroupinlist'):
        groups.append(record.get('csdgroup'))

    return groups
