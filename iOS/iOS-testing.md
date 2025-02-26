# iOS practical

## Jailbreak
There are multiple jailbreaks available, depending on the firmware and device model, different jailbreak will apply. 

- [AppleDB](https://appledb.dev) - Finding the device model and firmware to check which JB are available.
- [ios.cfw.guid](https://ios.cfw.guide/get-started/) -  Provides precautions and instructions on what to mind in every jailbreak.

The most famous jailbreaks are [checkra1n](https://checkra.in/), [palera1n](https://palera.in/) and [uncover](https://unc0ver.dev/).

After booting into the device, through the pre-installed package manager (Cydia, Sileo etc) install OpenSSH and Frida packages. 

Now you should be able to ssh into the device with:
```
ssh root@<IP_Address>
```
and the default password for root is <kbd>alpine</kbd>

## Reconnaissance

iOS apps are bundled in **IPA** zip archive. 

```
unzip -d <output_name> <zip_name>
```

Binaries are all signed by Apple, otherwise iOS refuses to execute them if they are not signed. 

Located in <kbd>Code signatures</kbd> → <kbd>CodeResources.xml</kbd>

To view architecture of the binary: 

```
xcrun -sdk iphoneos lipo -info <binary_name>
```

To locate certain strings inside the app : 

```
strings <binary_name>
```

Open the binary in **IDA** or **Frida** dissassembler. 

The same functionality with strings can be found in symbols search in IDA.

If an app really needs to have hardcoded secrets but not secrets, the developers can encode the string. Obfuscate it using anything like XOR. Another option is to encrypt the binary section which contains the strings. Binaries have some constructors that run before main, so the decryption algorithm can be called inside such a constructor, if an attacker have access to the binary at rest they will not be able to see the strings so easily.

Any application has a directory in which is installed and stores its data in:

```
 /private/var/mobile/Containers/Data/Application
```

In order to find where our app is we can use the command:

```
find / -name “*<binary_name>*”
```

If there is a **plist** file we can copy it to our computer. To convert the plist to xml we can use:

```
plistutil -i <filename>
```
## Static Analysis

For static analysis of iOS binaries the tools to use are [Ghidra](https://github.com/NationalSecurityAgency/ghidra) and [Hopper](https://www.hopperapp.com/).

[MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) can be used to see binary information, general app info, list of strings, the permissions of the app, and a list of issues.

For a quick setup simply run:

```
docker pull opensecurity/mobile-security-framework-mobsf:latest
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```

## Dynamic Instrumentation
### Frida

Dynamic Instrumentation with [Frida](https://github.com/frida), to intercept function calls, check function arguments and function return values and be able to change the apps control flow. Works well for mobile native applications (ObjC/Swift, native libraries, binaries compiled from C, C++, rust etc).

After connecting to the device with ssh, to get frida running on all interfaces simply run:

```
frida-server -l 0.0.0.0 &
```
The recommended way of running frida on our machine is inside a virtual environment. So after having installed python venv with
```
sudo apt install python3.10-venv
```
we can initiate a frida venv by running
```
python3 -m venv frida
source ~/path/to/fridas_venv/bin/activate
pip install frida frida-tools
```
To ensure frida is running on the device and we can interact with it we can list all running processes with the following command:
```
frida-ps -H <iPhone_IP> 
```
or to list all running processes along with their package names:
```
frida-ps -Uai
```

One can attach to a binary/process by running:
```
frida -U <binary_name> 
```

Then in the frida CLI in order to see all loaded modules (frameworks, libraries etc.) or filter out loaded modules according to a certain search term simply run:
```
mods = Process.enumerateModules()
or listmods = mods.filter(function(m){ return m.name.toLowerCase().includes("<keyword>")});
```
In order to search for specific functions inside an app we can use frida-trace. There is different syntax for when the function we are looking for is written in objective C or non-objectice C.

Objective C:
```
frida-trace -U <binary_name> -m "*[* *<keyword>]"
```
Non-objective C:
```
frida-trace -U <binary_name> -i "*<keyword"
```

### Objection
Another dynamic analysic tool which is basically based on Frida is [Objection](https://github.com/sensepost/objection). Objection has ready scripts for dumping application keychain, cookies,reading plist files or check for ssl pinning bypass etc.:

```
Objection -g <binary_pid> explore

Options:
 - ios keychain dump
 - ios cookies get
 - ios pasteboard monitor
 - ios sslpinning disable --quiet
 - ios nsuserdefaults get
 - ios nsurlcredentialstorage dump
 - ios plist cat <filename>.plist
```

A rooted device is needed for all the above, unless values are stored in the secure enclave. 

## Set up a proxy / Bypass certificate pinning
1. Set up a listening proxy for all interfaces on a specified port (eg. 8081)
2. List all running processes with frida to find out the process name of the application which certificate you want to bypass
   ```
   frida-ps -H <iPhone_IP> -ai
   ```
3. Run a SSL pinning bypass script from frida's codebase:
   ```
   frida --codeshare <path_to_file> -f <app_package_name> -H <iPhone_IP> (on a specific app)
    
   frida --codeshare <path_to_file> -F -H <iPhone_IP> (on the forefront app)
   ```

## Bypassing the jailbreak check

In frida check the symbols for the word jailbreak to find the function in which the check is implemented. Next we need to hook the application, essentially patching the function with our own code. To patch the app with frida we use:

```
frida -U -f -com.example.<app_name> -l <custom_function_name.js> --no-pause
```

If the method was in a c method and its symbol was stripped from the binary we would not be able to do this. In this case, we have to replace the method by chance. We should find the offset of the method but we don’t know where the binary is loaded in memory because of ASLR. We should find the address of the binary in the memory, we will look for a function or method for which we have the symbol (there is always gonna be a method with known symbols).
