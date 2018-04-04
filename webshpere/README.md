# Install WebSphere via Command Line

> https://www.ibm.com/support/knowledgecenter/SSV2LR/com.ibm.wbpm.imuc.sbpm.doc/topics/inst_sil_cmd_win.html

> https://www.ibm.com/support/knowledgecenter/en/SSDV2W_1.8.5/com.ibm.silentinstall12.doc/topics/t_silent_installIM_IMinst.html

## Required Resources
Please copy resources to following folder and ensure it has the exactly the same folder structure and contents:
```
-- C:\middleware\WebSphere
 |-- 8.5.5.11 Body
 |-- 8.5.5.11 Supplements
 |-- body
 |-- CIL0DML
 |-- Patch
 |-- Supplements
 |-- Tools
```

> You can copy it to another folder other than _C:\middleware\WebSphere_. 
> Please replace _C:\middleware\WebSphere_ with your folder in following command lines.

## Steps

### Extract Install Resources
Extract the installation files into separated folder of their current directories:
* C:\middleware\WebSphere\CIL0DML\agent.installer.win32.x86_64_1.8.5.zip
* C:\middleware\WebSphere\body\WASND_v8.5.5_1of3.zip
* C:\middleware\WebSphere\body\WASND_v8.5.5_2of3.zip
* C:\middleware\WebSphere\body\WASND_v8.5.5_3of3.zip
* C:\middleware\WebSphere\Supplements\WAS_V8.5.5_SUPPL_1_OF_3.zip
* C:\middleware\WebSphere\Supplements\WAS_V8.5.5_SUPPL_2_OF_3.zip
* C:\middleware\WebSphere\Supplements\WAS_V8.5.5_SUPPL_3_OF_3.zip
* C:\middleware\WebSphere\Patch\8.5.0.0-WS-WASJavaSDK-WinX64-IFPI76779.zip
* C:\middleware\WebSphere\Patch\8.5.5.0-ws-was-ifpi70169.zip
* C:\middleware\WebSphere\Patch\8.5.5.0-ws-was-ifpi73367.zip
* C:\middleware\WebSphere\Patch\8.5.5.11-ws-was-ifpi70627.zip
* C:\middleware\WebSphere\Patch\8.5.5.11-ws-wasihs-ifpi73984.zip
* C:\middleware\WebSphere\Patch\8.5.5.3-ws-wasprod-ifpi74857.zip
* C:\middleware\WebSphere\Patch\8.5.5.4-ws-was-ifpi73519.zip

### Install Installation Manager
> Reference: https://www.ibm.com/support/knowledgecenter/en/SSDV2W_1.7.3/com.ibm.silentinstall12.doc/topics/t_silent_installIM_IMinst.html

```commandline
cd C:\middleware\WebSphere\CIL0DML\agent.installer.win32.x86_64_1.8.5
installc.exe -log install.log -acceptLicense
```
> Note: 
> * The default installation directory is _C:\Program Files\IBM\Installation Manager_. Change by add `-installationDirectory` option
> * The license can be found at _C:\middleware\WebSphere\CIL0DML\agent.installer.win32.x86_64_1.8.5\native\agent.license_1.8.5.20160504.zip\license.txt_

### Record the Reponse File
**If there is an existing response file, the step can be skipped.** 
```commandline
cd C:\Program Files\IBM\Installation Manager\eclipse
IBMIM.exe -record WASv85.install.Win64.xml -skipInstall agentData
```


### 3. Silently installing packages using Installation Manager
```commandline
cd C:\Program Files\IBM\Installation Manager\eclipse
```
> Reference: https://www.ibm.com/support/knowledgecenter/en/SS62YD_2.2.1/com.ibm.datatools.base.install.doc/topics/t_silent_install_IM.html



## Reference
* [Sample response file: Installing IBM WebSphere Application Server Network Deployment](https://www.ibm.com/support/knowledgecenter/en/SSAW57_8.5.5/com.ibm.websphere.installation.nd.doc/ae/cins_WASv85_nd_install_Win32.html)
* [Sample response files](https://www.ibm.com/support/knowledgecenter/SSAW57_8.5.5/com.ibm.websphere.installation.nd.doc/ae/tins_WASv85_sample_response.html)


