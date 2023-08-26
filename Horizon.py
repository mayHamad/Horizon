from csv import DictWriter
import sys, os
import argparse
import yaml
from lib.WihteListValidate import ValidateSigner, ValidatePath, ValidateExt, ValidateFileName, ValidateVersion, ValidateHash, ValidateLang
import REG.KnownDlls, REG.Drivers

def ReadYaml(FullPath):
    try:
        with open(FullPath, 'r') as File :
            Wlst = {}
            Blst = {}
            lst = yaml.safe_load(File)
            if 'whiteList' in lst:
                for key, value in lst['whiteList'].items():
                    Wlst[key] = value
            if 'blackList' in lst:
                for key, value in lst['blackList'].items():
                    Blst[key] = value
            return Wlst, Blst
    except Exception as e:
        return e , e       

def Classfied (score):
    if score == 0:
        return 'Clean'
    elif score < 16:
        return 'Notice'
    elif score < 41:
        return 'Warning'
    else:
        return 'Alert'

def HuntFunc(Wlst, Blst, arti, VT, key):
    datalst = []
    i = 0
    for row in arti:
        Signer_score, FN_score, P_score, Ext_score, V_score, hash_score, l_score = 0, 0, 0, 0, 0, 0, 0
        signername = ''

        if Wlst['signer'] or Blst['signer']:
            Signer_score, signername = ValidateSigner(row['Signer'], row['SHA1'], Wlst['signer'], Blst['signer'], VT, key)
        if Wlst['filename'] or Blst['filename']:
            FN_score = ValidateFileName(row['FullPath'], Wlst['filename'], Blst['filename'])
        if Wlst['path'] or Blst['path']:
            P_score = ValidatePath(row['FullPath'], Wlst['path'], Blst['path'])
        if Wlst['ext'] or Blst['ext']:
            Ext_score = ValidateExt(row['FullPath'], Wlst['ext'], Blst['ext'])
        if Blst['version']:
            V_score = ValidateVersion(row['Version'], Blst['version'])
        if Blst['hash']:
            hash_score = ValidateHash(row['SHA1'], Blst['hash'])
        if Blst['lang']:
            l_score = ValidateLang(row['Language'], Blst['lang'])
        datalst.append(row)
        if hash_score > 0:
            datalst[i]['Score'] = ((Signer_score + hash_score)/2) + (((FN_score + P_score + Ext_score + V_score + hash_score + l_score)*20)/100)
        else:
            datalst[i]['Score'] = Signer_score + (((FN_score + P_score + Ext_score + V_score + hash_score + l_score)/700)*20)
        ###
        datalst[i]['Signer'] = signername
        datalst[i]['Classified'] = Classfied(datalst[i]['Score'])
        i += 1
    return datalst

def printOut(data, Fields, path, filename):
    with open(path+ '\\' + filename + '.csv', "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=Fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def artifactList():
    artilst = {
        'Drivers':{'parser': REG.Drivers.Drivers(), 'filters': 'Drivers.yml', 'Discription':'Lists  drivers that load at system bootup.'},
        'KnownDlls':{'parser': REG.KnownDlls.KnownDlls(), 'filters': 'KnownDlls.yml', 'Discription':'Lists Known DLLs that loaded by Session Manager during startup.'} }
    

    return artilst

def main(argv=None):
    argv = sys.argv
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', action='store', help='path to whitelist and blacklist yml files')
    parser.add_argument('-a', '--artilst', metavar='artifact', type=str, nargs='*', help='lists the artifacts name')
    parser.add_argument('-o', '--output', action='store', help='Path to output folder')
    parser.add_argument('-l',  '--list', action='store_true', help='List all parsers')
    parser.add_argument('-VT',  '--Virustotal', action='store_true', help='optional to use Virustotal feature')
    parser.add_argument('-k',  '--apikey', action='store', type=str, help='supply the API Key of your Virustotal account')
    
    args = parser.parse_args(argv[1:])
    parser = argparse.ArgumentParser(description='Hunter')

    if args.list:
        lst = []
        print ('List of avaiable parsers:\t')
        print ("{:<25} {:<10} ".format('Plugin', 'Discription'))
        for p in artifacts:
            print ("{:<25} {:<10} ".format(p, artifacts[p]['Discription']))
    if args.artilst:
        if os.path.exists(args.filter): 
            for arti in args.artilst:
                if args.Virustotal and args.apikey == None:
                    print('Enter the VT API key...')
                    break
                print('Parsing '+ arti+ '....')
                data, header = artifacts[arti]['parser']
                print('Evaluate the result of '+ arti+ '....')
                wlst, blst = ReadYaml(args.filter+'\\'+artifacts[arti]['filters'])
                lst = HuntFunc(wlst, blst, data, args.Virustotal, args.apikey)
                print('Print the results of '+ arti+ '....')
                printOut(lst, header, args.output, arti)
        else:
            print("The filter's folder is not exist")
            
if __name__ == '__main__':
    artifacts = artifactList()
    main(argv=sys.argv)
