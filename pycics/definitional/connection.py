import requests
import xml.etree.ElementTree as ET


def defineMroConnectionSession(host,port,authIn,context,scope,connName,csdgroup,netname):
    
    # Build XML body for create action

    # Example
    # <request>
    #     <create>
    #        <parameter name="CSD"/>
    #        <attributes 
    #            name="C002" 
    #            csdgroup="CICSTI99"
    #            ACCESSMETHOD='Xm' 
    #            protocol='NOTAPPLIC'
    #            COnntype='NOTAPPLIC'
    #            PSRECOVERY="N_A"
    #            XLNACTION="KEEP"
    #            SInglesess='NO'
    #            DAtastream='USER'
    #            RECordformat="U"
    #            USEDFLTUSER="NO" 
    #            ATTACHSEC="IDENTIFY" 
    #            AUTOCONNECT="YES"
    #            netname="CICSTI02"
    #            INSERVICE="YES" />
    #    </create>
    # </request>

    request    = ET.Element('request')
    create     = ET.Element('create')
    
    parameter  = ET.Element('parameter')
    parameter.set("name","CSD")
    
    attributes = ET.Element('attributes')
    attributes.set('name',connName)
    attributes.set('csdgroup',csdgroup)
    attributes.set('ACCESSMETHOD','Xm')
    attributes.set('protocol','NOTAPPLIC')
    attributes.set('COnntype','NOTAPPLIC')
    attributes.set('PSRECOVERY','N_A')
    attributes.set('XLNACTION','KEEP')
    attributes.set('SInglesess','NO')
    attributes.set('DAtastream','USER')
    attributes.set('RECordformat','U')
    attributes.set('USEDFLTUSER','NO')
    attributes.set('ATTACHSEC','IDENTIFY')
    attributes.set('AUTOCONNECT','YES')
    attributes.set('netname',netname)
    attributes.set('INSERVICE','YES')

    create.append(parameter)
    create.append(attributes)
    request.append(create)
    reqBody = ET.tostring(request)

    uri = "/CICSSystemManagement/CICSDefinitionISCMROConnection/"+context+"/"+scope
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

        raise Exception('Create connection in CSD failed with code {} ({}) - {} ({})'.format(api_response1,api_response1_alt,api_response2,api_response2_alt))
    

    for record in root.iter('{http://www.ibm.com/xmlns/prod/CICS/smw2int}cicsdefinitioniscmroconnection'):   
        print("Created {} in group {} with netname {}".format(connName,csdgroup,netname))
        return record
        # name    = record.get('name')
        # profile = record.get('profile')
        # print(name," => ",profile)


def discardConnectionDefinition(host,port,authIn,context,scope,connName,csdgroup):

    uri = "/CICSSystemManagement/CICSDefinitionISCMROConnection/"+context+"/"+scope+"?CRITERIA=NAME="+connName+"&PARAMETER=CSDGROUP("+csdgroup+")"
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
        print("No session found for {} in group {}...".format(connName,csdgroup))
    elif api_response1 == "1024":
        print("Connection",connName," definition discarded")
