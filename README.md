# CamMander (CVE-2013-1599)
### Exploit toolkit for (old) IP Cameras
**_Educational Purposes Only_**
<center>
<img src="logo.jpeg" width="320" height="320">
</center>
Inspired by Black Hat 2013 - Exploiting Network Surveillance Cameras Like a Hollywood Hacker talk by Craig Heffner. This is a rootshell toolkit for an Old day targeting D-LINK and TRENDnet cameras.
<hr>

In his talk he mentioned that these cameras would most likely be exploitable "3 years from now". Well here we are 10 years later and there are still thousands of these devices unpatched and connected to the internet.

I tried to include a feature from his demo that would allow one to 'freeze' the camera feed with a still image and provide a backdoor feed but it doesn't seem possible without firmware modification (they're using cramfs and I have limited time).

This is intended to be solely a proof of concept and demonstrate the longengivity of vulnerabilities in IoT devices. With some time and imagination one could only dream of all of the ways these devices can be manipulated and misused by attackers. 

**Affeced Devices:**
* D-Link DCS-1130
* D-Link DCS-2102
* D-Link DCS-2121
* D-Link DCS-3410
* D-Link DCS-5230
* D-Link DCS-5605
* Trendnet TV-IP512WN
* Trendnet TV-IP512P
* Trendnet TV-IP522P
* Trendnet TV-IP612WN

```
CamMander Exploit Toolkit (CVE_2013_1599)
        menu - prints this menu
        getpasswd - retrieve admin password from camera
        help - list available commands on camera
        killfeed - temporarily kills all active camera feeds until browser is refreshed
        exit - quit the program
(192.168.168.168)# 
```

**_Educational Purposes Only_**