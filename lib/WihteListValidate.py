import os
from lib.VurisTotalAPI import SHA1_Query

def findEntry(item, lst):
    if lst:
        for entry in lst:
            if item.lower() == entry.lower():
                return 'found'
    return 'Notfound'

## Validate The Signer ##
#
def ValidateSigner(signer, SHA1, WL_signer, BL_signer, VT, key):
    if VT:
        Hash, Integrity, SignerLst = SHA1_Query(SHA1, key)    
        if findEntry(signer, WL_signer) == 'found':
            return 0 + Hash + Integrity, signer   
        elif findEntry(signer, BL_signer) == 'found':
            return 30 + Hash + Integrity, signer
        for s in SignerLst:
            if findEntry(s, WL_signer) == 'found':
                return 0 + Hash + Integrity, s
            elif findEntry(s, BL_signer) == 'found':
                return 30 + Hash + Integrity, s
        return 15 + Hash + Integrity, 'Notfound'
    else:
        if findEntry(signer, WL_signer) == 'found':
            return 0, signer
        elif findEntry(signer, BL_signer) == 'found':
            return 80, 'Notfound'
        else:
            return 40, 'Notfound'     

## Path Validation ##
#s
def ValidatePath(path, WL_path, BL_path):
    if findEntry(os.path.dirname(path), WL_path) == 'found':
        return 0
    elif findEntry(os.path.dirname(path), BL_path) == 'found':
        return 100
    else:
        return 50

## Extension Validation ##
#
def ValidateExt(path, WL_Ext, BL_Ext):
    filename, file_extension = os.path.splitext(path)
    if findEntry(file_extension, WL_Ext) == 'found':
        return 0
    elif findEntry(file_extension, BL_Ext) == 'found':
        return 100
    else:
        return 50

## File Name Validation ##
#
def ValidateFileName(path, WL_FileName, BL_FileName):
    if findEntry(os.path.basename(path), WL_FileName) == 'found':
        return 0
    elif findEntry(os.path.basename(path), BL_FileName) == 'found':
        return 100
    else:
        return 50
## Version Validation ##
#
def ValidateVersion(version, BL_version):
    if findEntry(version, BL_version) == 'found':
        return 100
    else:
        return 0

def ValidateHash(Hash, BL_Hash):
    if findEntry(Hash, BL_Hash) == 'found':
        return 80
    else:
        return 0

def ValidateLang(Lang, BL_Lang):
    if findEntry(Lang, BL_Lang) == 'found':
        return 100
    else:
        return 0
