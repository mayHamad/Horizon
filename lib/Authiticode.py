import windows.wintrust
import windows.crypto
import re
import lief

def GetSigner(FullPath):
    try:
        Cert = windows.crypto.CryptObject(FullPath) 
        if Cert:
            marker1 = 'b'
            marker2 = '" serial'
            regexPattern = marker1 + '(.+?)' + marker2
            Cert_Str = str(Cert.crypt_msg.certs[0])
            Singer = re.search(regexPattern, Cert_Str).group(1)
            return Singer.replace("'", "")
    except Exception as e:
        return 'Notfound'

def IsSign(File):
    try:
        return windows.wintrust.is_signed(File)
    except Exception as e:
        return 'N/A'
    
