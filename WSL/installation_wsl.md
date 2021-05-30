# Windows Subsystem for Linux

### Enable WSL

Run powershell as administrator and paste this:
```POWERSHELL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
```

### Ubuntu

<a href = "https://www.windowscentral.com/e?link=https%3A%2F%2Fclick.linksynergy.com%2Fdeeplink%3Fid%3DkXQk6%252AivFEQ%26mid%3D24542%26u1%3DUUwpUdUnU72700YYwYg%26murl%3Dhttps%253A%252F%252Fwww.microsoft.com%252Fen-us%252Fp%252Fubuntu%252F9nblggh4msv6%26ourl%3Dhttps%253A%252F%252Fwww.microsoft.com%252Fstore%252FproductId%252F9NBLGGH4MSV6&token=ti9ZlPH4">Download Ubuntu</a>

### Download Windows Terminal
<a href = "https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab">Download Windows Terminal</a>

#### Convert WSL 1 to WSL 2
```POWERSHELL
wsl --set-version Ubuntu-20.04 2
```
