![](docs/vmt_vr.png)
## [Official page and Manual](https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/)
### [API Reference](https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/api/)
### [Sample Code](https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/sample/)
### [Download Binaly](https://github.com/MeemeeLab/VirtualMotionTracker-for-linux/releases)

> [!INFO]  
> This is NOT a original version of Virtual Motion Tracker by `gpsnmeajp`.  
> If you don't need Linux support or just want to read readme, Go to official repository! [gpsnmeajp/VirtualMotionTracker](https://github.com/gpsnmeajp/VirtualMotionTracker)

> [!WARNING]  
> This linux port is still a experimental and it is prototype level. Do not use for production!

# VMT - Virtual Motion Tracker for Linux
This is fork of Virtual Motion Tracker, patched to work with GNU/Linux.
Tested on Arch Linux rolling x86_64, ALVR, Oculus Quest 2.

## Installation
Grab my builds from [release page](https://github.com/MeemeeLab/VirtualMotionTracker-for-linux/releases).

After downloading precompiled driver, extract somewhere that is _permanant_.

Next, you need to tell SteamVR to use this driver. Run this command:
```sh
~/.steam/steam/steamapps/common/SteamVR/bin/vrpathreg.sh adddriver /path/to/driver
```

Root of driver directory includes driver.vrdrivermanifest, settings.json and some directories.

After registration, SteamVR should load drivers for you. Start SteamVR and check driver is loaded:
```
Option (top-left corner button of SteamVR window) -> Settings -> Controllers -> Manage Trackers
```
If you see multiple trackers like `VMT_0`, hooray! it's installed. Follow setup guide section [Initial Setup of original VirtualMotionTracker](https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/setup/#initial-setup) but with vmt_manager_gtk as a manager. You can skip Download and Installation section of official document. it is only for Windows.

\> For installing vmt_manager_gtk on Linux, go to [vmt_manager_gtk/README.md](https://github.com/MeemeeLab/VirtualMotionTracker-for-linux/blob/master/vmt_manager_gtk/README.md)

# Licence
MIT Licence

Logo text font: M+ Fonts https://mplus-fonts.osdn.jp/about2.html

![](docs/VMTlogo.png)
