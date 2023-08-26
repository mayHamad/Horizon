from win32api import *


PropertyNames = ( 'OriginalFilename', 'ProductName', 'CompanyName', 'FileDescription')

def GetFileInfo(windows_exe):
    FileInfo = {}
    try:
        language, codepage = GetFileVersionInfo(windows_exe, '\\VarFileInfo\\Translation')[0]
        for Name in PropertyNames:
            strFileInfo = u'\\StringFileInfo\\%04X%04X\\%s' % (language, codepage, Name)
            FileInfo[Name] = GetFileVersionInfo(windows_exe, strFileInfo)
        FileInfo['Language'] = language
        FileInfo['Version'] = ".".join(get_version_number(windows_exe))
    except Exception as e:
        print("The error is: ",e)
        
    return FileInfo
    
def get_version_number(file_path):
  
    File_information = GetFileVersionInfo(file_path, "\\")
  
    ms_file_version = File_information['FileVersionMS']
    ls_file_version = File_information['FileVersionLS']
  
    return [str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)),
            str(HIWORD(ls_file_version)), str(LOWORD(ls_file_version))]
