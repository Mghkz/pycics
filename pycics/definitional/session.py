import requests
import xml.etree.ElementTree as ET


def defineLU61Session(host,port,authIn,context,scope,sessionName,csdgroup,connection):
    
   # Build XML body for create action

    # Example
    # <request>
    #     <create>
    #        <parameter name="CSD"/>
    #        <attributes 
    #             NAME="C099C002" 
    #             CSDGROUP="CICSTI99"
    #             AUTOCONNECT="YES"
    #             BUILDCHAIN="YES"
    #             DISCREQ="NO"
    #             IOAREALEN="1024"
    #             IOAREALEN2="1024"
    #             RELREQ="NO"
    #             CONNECTION="C002"
    #             PROTOCOL="LU61"
    #             RECEIVECOUNT="40"
    #             RECEIVEPFX="V0"
    #             RECEIVESIZE="4096"
    #             SENDCOUNT="40"
    #             SENDPFX="N0"
    #             SENDSIZE="4096"
    #             SESSPRIORITY="50"
    #     </create>
    # </request>

    request    = ET.Element('request')
    create     = ET.Element('create')
    
    parameter  = ET.Element('parameter')
    parameter.set("name","CSD")
    
    attributes = ET.Element('attributes')
    attributes.set('NAME',sessionName)
    attributes.set('CSDGROUP',csdgroup)
    attributes.set('AUTOCONNECT','YES')
    attributes.set('BUILDCHAIN','YES')
    attributes.set('DISCREQ','NO')
    attributes.set('IOAREALEN','1024')
    attributes.set('IOAREALEN2','1024')
    attributes.set('RELREQ','NO')
    attributes.set('CONNECTION',connection)
    attributes.set('PROTOCOL','LU61')
    attributes.set('RECEIVECOUNT','40')
    attributes.set('RECEIVEPFX','<')
    attributes.set('RECEIVESIZE','4096')
    attributes.set('SENDCOUNT','40')
    attributes.set('SENDPFX','>')
    attributes.set('SENDSIZE','4096')
    attributes.set('SESSPRIORITY','50')

    create.append(parameter)
    create.append(attributes)
    request.append(create)
    reqBody = ET.tostring(request)

    uri = "/CICSSystemManagement/CICSDefinitionSession/"+context+"/"+scope
    url = "http://"+host+":"+port + uri

    # 'verify=False' to disable ssl certificate verification
    resp = requests.post(url,reqBody,auth=authIn,verify=False)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('POST /tasks/ {}'.format(resp.status_code))

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

        raise Exception('Create session in CSD failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitionsession'):   
        print("Created {} in group {} with connection {}".format(sessionName,csdgroup,connection))
        return record
        # name    = record.get('name')
        # profile = record.get('profile')
        # print(name," => ",profile)


def discardSessionDefinition(host,port,authIn,context,scope,sessionName,csdgroup):

    uri = "/CICSSystemManagement/CICSDefinitionSession/"+context+"/"+scope+"?CRITERIA=NAME="+sessionName+"&PARAMETER=CSDGROUP("+csdgroup+")"
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
        print("Session",sessionName,"definition discarded")