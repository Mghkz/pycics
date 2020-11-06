import requests
import xml.etree.ElementTree as ET

#http://{{url-cmci}}:{{port-cmci}}/CICSSystemManagement/CICSLocalTransaction/CICSAI99/CICSTI99?CRITERIA=TRANID=4FT8

def viewInstalledTransaction(host,port,authIn,context,scope,tranId):
    print("viewLocalTransaction")


def discardInstalledTransaction(host,port,authIn,context,scope,tranId):

    uri = "/CICSSystemManagement/CICSLocalTransaction/"+context+"/"+scope+"?CRITERIA=TRANID="+tranId
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
    # 1027 => Nothing records return => Nothing to discard
    if (api_response1 != "1024" and api_response1 != "1027" ):
        raise Exception('Discard transaction failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    elif api_response1 == "1027":
        print("Could not discard the transaction because it was not installed... ")

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitiontransaction'):   
        name    = record.get('name')
        profile = record.get('profile')
        print(name," => ",profile)
