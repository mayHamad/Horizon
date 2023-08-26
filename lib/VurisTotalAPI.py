import requests                     

def SHA1_Query(SHA1, apikey):
    response={}
    url = "https://www.virustotal.com/api/v3/files/" + SHA1

    headers = {
        "accept": "application/json",
        "x-apikey": apikey
    }
    try:
        response = requests.get(url, headers=headers).json()
    except Exception as e:
        print(e)
    if not 'error' in response:
        try:
            ## File Integrity Wight ##
            #
            #Singer = response['data']['attributes']['signature_info']['product']

            Integrity_WT = 0
            Signer = []

            if 'verified' in response['data']['attributes']['signature_info']:
                if response['data']['attributes']['signature_info']['verified'] != "Signed":
                    Integrity_WT = 50
            else:
                Integrity_WT = 100
            
            if 'x509' in response['data']['attributes']['signature_info']:
                for i in response['data']['attributes']['signature_info']['x509']:
                    Signer.append(i['name'])
            elif 'counter signers details' in response['data']['attributes']['signature_info']:
                for i in response['data']['attributes']['signature_info']['counter signers details']:
                    Signer.append(i['name'])
            #
            ## Hash Wight ## 
            #      
            Mal = response['data']['attributes']['last_analysis_stats']['malicious']
            Cln = response['data']['attributes']['last_analysis_stats']['undetected']
            Hash_WT = (Mal/(Mal+Cln))*100
            return ((Hash_WT*40)/100), ((Integrity_WT*10)/100), Signer
        except Exception as e:
            return 40, 10, ''        
    else:
        return 40, 10, ''