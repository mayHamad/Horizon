import pathlib
import os

def replaceRoot(path, root):
    if root == 'programfiles':
        return path.replace('programfiles','C:\\programfiles')
    elif root == 'programfiles(x86)':
        return path.replace('programfiles(x86)','C:\\programfiles(x86)')
    elif root == 'systemroot':
        return path.replace('systemroot','C:\\windows')
    elif root == 'windir':
        return path.replace('windir','C:\\windows')
    elif root == 'windows':
        return path.replace('windows','C:\\windows')
    elif root == 'system32':
        return path.replace('system32','C:\\windows\\system32')
    else:
        return path

def cleanup(path):
    path = path.lower()
    if path.startswith('"'):
        path = path[1:]
    if path.startswith('\??\\'):
        path = path.replace('\??\\', '')
    if '" ' in path:
       path = path.split('" ', 1)[0]
    if ' /' in path:
        path = path.split(' /', 1)[0]
    filename = os.path.basename(path)
    path = ''.join(path.partition(filename)[0:2])
    if path.endswith('"'):
        path = path[:-1]
    return path

def findRoot(path):
    path = cleanup(path)
    p = pathlib.Path(path)
    if p.parts[0] != 'c:\\':
        if p.parts[0] == '\\':
            path = path[1:]
            return replaceRoot(path, p.parts[1])
        elif p.parts[0].startswith('%'):
            path = path.replace('%', '', 2)
            p = pathlib.Path(path)
            return replaceRoot(path, p.parts[0])
        else:
            return replaceRoot(path, p.parts[0])
    return path 
