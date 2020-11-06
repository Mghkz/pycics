import requests
import xml.etree.ElementTree as ET

# Get a terminal for the given netname
def inquireTerminalWithNetname(host,port,authIn,context,scope,netname):

    uri = "/CICSSystemManagement/CICSTerminal/"+context+"/"+scope+"?CRITERIA=NETNAME="+netname
    url = "http://"+host+":"+port + uri
    
    termIds = []

    # 'verify=False' to disable ssl certificate verification
    resp = requests.get(url,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('Delete /tasks/ {}'.format(resp.status_code))

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
        raise Exception('Discard transaction failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("No terminal found for {}... ".format(netname))

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsterminal'):   
        termId = record.get('termid')
        termIds.append(termId)

        print("termid for",netname,"=>",termId)
    
    return termIds
