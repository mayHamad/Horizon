import hashlib

def GetFileMD5(FullPath):
    try:
        return hashlib.md5(open(FullPath,'rb').read()).hexdigest()
    except:
        return 'n/a'

def GetFileSHA1(FullPath):
    try:
        return hashlib.sha1(open(FullPath,'rb').read()).hexdigest()
    except:
        return 'n/a'
