import requests
import xml.etree.ElementTree as ET

def setTerminalOutService(host,port,authIn,context,scope,termid):

    uri = "/CICSSystemManagement/CICSTerminal/"+context+"/"+scope+"?CRITERIA=TERMID="+termid
    url = "http://"+host+":"+port + uri
    
  
    termIds = []

    # Build XML for with update statement
    request    = ET.Element('request')
    action     = ET.Element('action')

    action.set('name',"OUTSERVICE")
    request.append(action)

    reqBody = ET.tostring(request)

    # 'verify=False' to disable ssl certificate verification
    resp = requests.put(url,reqBody,auth=authIn,verify=False)
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
        print("No terminal found for {}... ".format(termid))

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsterminal'):   
        termId = record.get('termid')
        termIds.append(termId)

        print("termid",termId,"outserviced")
    
    return termIds


def discardTerminal(host,port,authIn,context,scope,termid):

    uri = "/CICSSystemManagement/CICSTerminal/"+context+"/"+scope+"?CRITERIA=TERMID="+termid
    url = "http://"+host+":"+port + uri


    # 'verify=False' to disable ssl certificate verification
    resp = requests.delete(url,auth=authIn,verify=False)
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
        print("No terminal found for {}... ".format(termid))
    elif api_response1 == "1024":
        print("Termid",termid,"discarded")


    # No Records returned after discard

    #for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsterminal'):   
    #    termId = record.get('termid')
    #    termIds.append(termId)
    #    print("termid",termId,"discarded")
    

def discardTerminalDefinition(host,port,authIn,context,scope,termid,csdgroup):

    uri = "/CICSSystemManagement/CICSDefinitionTerminal/"+context+"/"+scope+"?CRITERIA=NAME="+termid+"&PARAMETER=CSDGROUP("+csdgroup+")"
    url = "http://"+host+":"+port + uri


    # 'verify=False' to disable ssl certificate verification
    resp = requests.delete(url,auth=authIn,verify=False)
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
        raise Exception('Delete terminal definition failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("No terminal definition found for {} in group {}...".format(termid,csdgroup))
    elif api_response1 == "1024":
        print("Termid",termid," definition discarded")


    # No Records returned after discard

    #for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsterminal'):   
    #    termId = record.get('termid')
    #    termIds.append(termId)
    #    print("termid",termId,"discarded")
    
