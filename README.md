# Horizon
Horizon is a live forensic tool that aims to evaluate the entries of system artifacts on Windows OS based on file metadata. The core idea of Horizon is the whitelisting and blacklisting concept where each piece of info from file metadata can have a whitelist, blacklist, or both. The file evaluation will be based on whitelist and blacklist in an automated manner using the weighted formula. The weighted formula used in the Horizon depends on Authenticode and file hash which represents 80% of the score. The 20% will be divided among the remains file metadata.
We can summarize the functionality of the tool into four functions:
- Parsing the artifact.
- Extract specific info from file metadata: file creation timestamp, file modified timestamp, Signer, whether the file is signed or not, the original filename, file location, product name, company name, file description, language, version, and file hash (SHA1).
- Evaluate the entries based on the whitelist and blacklist.
- Score each entry and classify it into one of three levels:
  - Clean: 0
  - Notice: from 1 to 15.
  - Warning: from 16 to 40
  - Alert: from 41 to 100

For the whitelist and blacklist, they define using YAML files. The project repository has examples in the "filter folder". 

**In below figure shows the tool's workflow at a high level.**
<p align="center">
<img src="https://github.com/mayHamad/Horizon/assets/46843593/5f7ebeaf-a559-496a-95c9-4c9fb4d83774" >
<p />

# Feature
- Provide file metadata for system artifacts that are provided by default, such as KnonwDlls.
- Evaluate the entries of system artifacts in an automated manner to facilitate the artifact analysis mission.
- Connect to Virustotal API to evaluate file hash. 
- Export the results in CSV format.
# How to use
```
Horizon.exe -a [lists the artifacts name] -f [path to whitelist and blacklist YAML files] -VT [optional to use Virustotal feature] -k [supply the API Key of your Virustotal account] -o [path to results folder]
```


