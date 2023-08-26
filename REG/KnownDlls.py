import os
import winreg
import datetime
from lib.Authiticode import IsSign, GetSigner
from lib.timestamp import dt_from_win32_ts
from lib.winapi import GetFileInfo
from lib.Hash import GetFileSHA1


FileInfo = {'RegKey Last time modified': 'N/A', 'Launch String': 'N/A', 'File Creation time': 'N/A', 'File modefied time': 'N/A', 'KnownDll': 'N/A', 'FullPath': 'N/A', 'Signer': 'N/A',
            'IsSign': 'N/A', 'OriginalFilename': 'N/A', 'ProductName': 'N/A', 'CompanyName': 'N/A', 'FileDescription': 'N/A', 'Language': 'N/A', 'Version': 'N/A', 'SHA1': 'N/A', 'Score': 0, 'Classified': 'N/A'}

def KnownDlls():
    lst = []
    Paths = ['C:\\windows\\system32\\', 'C:\\Windows\\SysWOW64\\']
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    keyPath = 'SYSTEM\ControlSet001\Control\Session Manager\KnownDLLs'
    aKey = winreg.OpenKey(aReg, keyPath)
    
    ts = winreg.QueryInfoKey(aKey)[2]
    numSkey = winreg.QueryInfoKey(aKey)[1]
    dt = dt_from_win32_ts(ts)
    for i in range(numSkey):
        try:
            aValue_name = winreg.EnumValue(aKey, i)
            for p in Paths:
                if os.path.isfile(p+aValue_name[1]):
                    FileInfo['RegKey Last time modified'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['Launch String'] = keyPath
                    FileInfo['File Creation time'] = datetime.datetime.fromtimestamp(os.path.getctime(p+aValue_name[1])).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['File modefied time'] = datetime.datetime.fromtimestamp(os.path.getmtime(p+aValue_name[1])).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['KnownDll'] = aValue_name[1] 
                    FileInfo['FullPath'] = p+aValue_name[1]
                    FileInfo['Signer'] = GetSigner(p+aValue_name[1])
                    FileInfo['IsSign'] = IsSign(p+aValue_name[1])
                    FileInfo['SHA1'] = GetFileSHA1(p+aValue_name[1])
                    for key, value in GetFileInfo(p+aValue_name[1]).items():
                        FileInfo[key] = value
                    lst.append(FileInfo.copy())            
        except EnvironmentError:
            break
    return lst, FileInfo