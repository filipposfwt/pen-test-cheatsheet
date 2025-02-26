Adb is the debugger used to interact with any android app. To list devices and get a shell run:
```
adb devices
adb shell
```
The package manager is called pm , $pm list packages will list all available packages on the device.
```
pm path <package_name> 
```

will retrieve the path where an apk resides.

```
adb pull <full_path> 
```

Static analysis with mobSF. Hashes, permissions, identified issues. Static analysis with qark.
```
qark –apk <apk_file> 
```

To get the contents of the apk we can use:

```
unzip <apk_file>
```

AndroidManifest.xml if opened will not list readable contents. So in order to properly view the manifest file we should use apktool:

```
java jar ~/tools/apktool/apktool_x_x_x.kjar d I <apk_file>
```

Inside the created folder there is a readable AndroidManifest.xml file.

Inside the application folder there is a directory containing all activities code in smali code. One can actually edit these files, add smali code, recompile the code and repackage the application and install it on the device. 

First we should install the original application by running adb install <apk_name>.  

We can now edit the smali code of any activity and edit the onCreate method and add our code. Save the file and recompile with :

```
java jar ~/tools/apktool/apktool_x_x_x.kjar b I <apk_file>
```

If we try to install the app like that, the device will not let us since it is not sgned. We can use zipalign to align the app.

```
zipalign -f 4 <apk_name> <apk_output_name>
```

and to generate a key 

```
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```
sign the apk
```
apksigner sign –ks keystore.jks <apk_output_name>
```
and install the apk with 
```
adb install <apk_output_name>
```
From here we can use another tool called jadx is actually a decompiler, it does what apktool does but furthermore it will try to decompile the java code. Using this if the decompilation is successful we can have a look at the code and can be used to bypass certain security measures. 

For functional testing we should use Burp. We should configure the device to use a proxy through the wifi settings. We should download the CA .der certificate of Burp and install on the device, Android does not accept .der certificate so we have to transform it into .cer. 
```
frida-ps -U 
```
shows all the running applications on the device
```
frida -U -f com.android.<app_name> -l <bypass_script.js>
```
To hook the certain application and bypass the function of interest.

A very useful frida tool epsecially in the first stages of an application assessment is frida-trace, which searches for strings and automatically hooks found methods.

```
frida-trace -U -f com.android.<app_name> -i fopen* 
```

Another tool is called drozer. After downloading and installing the drozer agent apk on the device, we need to port forward to establish the communication between the Drozer Client and Agent, here is the command to do so:

```
adb forward tcp:31415 tcp:31415
```

Then we can connect to the device and open the drozer console with the following command:

```
drozer console connect 
```

From here valuable information can be obtained using the various modules available for drozer.The following command will output broadcast receivers and list their actions and permissions. We can open dz console and by running the following command see if the intent is actually unprotected.

```
run app.broadcast.info -a com.android.<app_name> -i
run app.broadcast.send –action <action_name> --extra string <parameter_name> <parameter_value> --extra string <parameter_name> <parameter_value>
```
