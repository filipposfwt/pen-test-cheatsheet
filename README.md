# pen-test-cheatsheet
## Scanning/Enumeration
### Tools
- nmap 
- nikto
- dirbuster

### Nmap
```
git status
git add
git commit
```
## Bypassing AV & EDRs
### Tools
- Shellter - Dynamic shellcode injection tool aka dynamic PE infector (https://www.shellterproject.com)
- SigThief - Stealing Signatures and Making One Invalid Signature (https://github.com/secretsquirrel/SigThief)
- MetaTwin - Cloning metadata and digital signature (https://github.com/threatexpress/metatwin)
- CMiner - Finding code caves in PEs (https://github.com/EgeBalci/Cminer)
- CFF explorer - Viewing a file's details

## MS Office Documents
### Generating malicious macro-enabled documents
- Boobsnail - BoobSnail allows generating XLM (Excel 4.0) macro. (https://github.com/STMCyber/boobsnail)
- Evilclippy - A cross-platform assistant for creating malicious MS Office documents. Can hide VBA macros, stomp VBA code (via P-Code) and confuse macro analysis tools. (https://github.com/outflanknl/EvilClippy)
- Ivy - payload creation framework for the execution of arbitrary VBA (macro) source code in memory. (https://github.com/optiv/Ivy)
- Hot-manchego - Macro-Enabled Excel File Generator (.xlsm) using the EPPlus Library. (https://github.com/FortyNorthSecurity/hot-manchego)

### Sandbox evasion with VBA referencing 
- Doctrack - Inserting tracking pixel and remote template for template injection. (https://github.com/wavvs/doctrack)
- intercepter.py - Custom python script to serve a tracking .png image, detect if code is running in a sandbox or user and serve a benign or malicious template.

