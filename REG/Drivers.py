import os
import winreg
import datetime
from csv import DictWriter
from lib.GetPath import findRoot
from lib.Authiticode import IsSign, GetSigner
from lib.timestamp import dt_from_win32_ts
from lib.winapi import GetFileInfo
from lib.Hash import GetFileSHA1


FileInfo = {'RegKey Last time modified': 'N/A', 'Launch String': 'N/A', 'File Creation time': 'N/A', 'File modefied time': 'N/A', 'Name': 'N/A', 'Image Path': 'N/A', 'FullPath': 'N/A',  
            'Mode': 'N/A', 'Type': 'N/A', 'Signer': 'N/A', 'IsSign': 'N/A', 'OriginalFilename': 'N/A', 'ProductName': 'N/A', 'CompanyName': 'N/A', 
            'FileDescription': 'N/A', 'Language': 'N/A', 'Version': 'N/A', 'SHA1': 'N/A', 'Score': 0, 'Classified': 'N/A'}
ServiceStartMode = {0: "Boot", 1: "System", 2: "Automatic", 3: "Manual", 4: "Disabled"}
Type = {1: "KernelDriver", 2: "FileSystemDriver", 4: "Adapter", 8: "RecognizerDriver", 16: "Win32OwnProcess", 32: "Win32ShareProcess", 256: "InteractiveProcess"}
lst = []

def GetService(key):
    for i in range(1024):
        try:
            vname, value, vtype = winreg.EnumValue(key, i)
            if value:                
                if vname == 'ImagePath':
                    FileInfo['Image Path'] = value
                    FileInfo['FullPath'] = findRoot(value)
                elif vname == 'Start':
                    FileInfo['Mode'] = ServiceStartMode[value]
                elif vname == 'Type':
                    try:
                        FileInfo['Type'] = Type[value]
                    except:
                        continue 
        except:
            pass
 
def Drivers():
    
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    keyPath = 'SYSTEM\ControlSet001\Services'
    aKey = winreg.OpenKey(aReg, keyPath)
    numSkey = winreg.QueryInfoKey(aKey)[0]

    for i in range(numSkey):
        try:
            subkey = winreg.EnumKey(aKey, i)
            sKey = winreg.OpenKey(aReg, keyPath + '\\' + subkey)
            if winreg.QueryInfoKey(sKey)[1] > 0:
                FileInfo['Name'] = subkey
                type = winreg.QueryValueEx(sKey, 'Type')
                if type[0] == 1 or type[0] == 2 or type[0] == 4 or type[0] == 8:
                    GetService(sKey)
                    ts = winreg.QueryInfoKey(aKey)[2]
                    dt = dt_from_win32_ts(ts)
                    FileInfo['RegKey Last time modified'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['Launch String'] = keyPath + '\\' + subkey
                    FileInfo['File Creation time'] = datetime.datetime.fromtimestamp(os.path.getctime(FileInfo['FullPath'])).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['File modefied time'] = datetime.datetime.fromtimestamp(os.path.getmtime(FileInfo['FullPath'])).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    FileInfo['Signer'] = GetSigner(FileInfo['FullPath'])
                    FileInfo['IsSign'] = IsSign(FileInfo['FullPath'])
                    FileInfo['SHA1'] = GetFileSHA1(FileInfo['FullPath'])
                    for key, value in GetFileInfo(FileInfo['FullPath']).items():
                        FileInfo[key] = value
                    lst.append(FileInfo.copy())             
        except EnvironmentError:
            pass
    return lst, FileInfo
