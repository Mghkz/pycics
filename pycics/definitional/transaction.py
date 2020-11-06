import requests
import xml.etree.ElementTree as ET

def viewTransactionDefinition(host,port,authIn,context,scope,tranId):
    
    uri = "/CICSSystemManagement/CICSDefinitionTransaction/"+context+"/"+scope+"?CRITERIA=NAME="+tranId+"&PARAMETER=CSDGROUP(*)"
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
        
    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitiontransaction'):
        name    = record.get('name')
        profile = record.get('profile')
        print(name," => ",profile)

def updateTransactionDefinition(host,port,authIn,context,scope,tranId,profile):
    
    # Build XML for with update statement
    request    = ET.Element('request')
    update     = ET.Element('update')
    attributes = ET.Element('attributes')
    attributes.set('PROFILE',profile)
    update.append(attributes)
    request.append(update)
    reqBody = ET.tostring(request)

    uri = "/CICSSystemManagement/CICSDefinitionTransaction/"+context+"/"+scope+"?CRITERIA=NAME="+tranId+"&PARAMETER=CSDGROUP(*)"
    url = "http://"+host+":"+port + uri

    # 'verify=False' to disable ssl certificate verification
    resp = requests.put(url,reqBody,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('PUT /tasks/ {}'.format(resp.status_code))

    content = resp.content
    root = ET.fromstring(content)

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}resultsummary'):
        api_response1 = record.get('api_response1')
        api_response2 = record.get('api_response2')
        api_response1_alt = record.get('api_response1_alt')
        api_response2_alt = record.get('api_response2_alt')

    if (api_response1 != "1024"):
        raise Exception('Update CSD Definition failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitiontransaction'):   
        name    = record.get('name')
        profile = record.get('profile')
        print(name," => ",profile)


def installTransactionDefinition(host,port,authIn,context,scope,tranId):

    # Build XML for with update statement
    request    = ET.Element('request')
    action     = ET.Element('action')
    action.set('name','CSDINSTALL')
    request.append(action)
    reqBody = ET.tostring(request)

    uri = "/CICSSystemManagement/CICSDefinitionTransaction/"+context+"/"+scope+"?CRITERIA=NAME="+tranId+"&PARAMETER=CSDGROUP(*)"
    url = "http://"+host+":"+port + uri

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

    if (api_response1 != "1024"):
        raise Exception('Install transaction failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    
    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitiontransaction'):   
        name    = record.get('name')
        profile = record.get('profile')
        print(name," => ",profile)


