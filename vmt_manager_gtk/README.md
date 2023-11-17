# vmt_manager_gtk

vmt_manager_gtk is the manager of Virtual Motion Tracker using GTK4.
Unlike vmt_manager_dotnet, GTK is designed to work with GNU/Linux.

> [!CAUTION]  
> EN: This program is NOT designed or developed by `gpsnmeajp`, a original author of Virtual Motion Tracker. This is fork of VMT with patches for GNU/Linux support. Do NOT contact original author with issues on this repository.  
> JA: このプログラムはVirtual Motion Trackerのオリジナル作者である`gpsnmeajp`さんによって設計、開発されたものではありません。これはVMTのフォークで、GNU/Linuxをサポートするためのパッチが含まれています。このリポジトリに関する問題を元の作者に問い合わせないでください。

This program is currently in development and some features are missing:
 - Install tab
    - Install tab is missing. This is in TODO list and will be implemented in future.
 - Input tab
    - Same as above, will be implmented in future.

While some futures are missing from dotnet version, you can set room matrix, which is a requirement for VMT to work.

To install vmt_manager_gtk as a flatpak package, follow these steps:
```sh
cd vmt_manager_gtk

# Build and install flatpak image
flatpak-builder --user --install --force-clean .build org.gpsnmeajp.vmt.vmt_manager.json
```

> [!NOTE]
> Building vmt_manager_gtk requires internet connection as it has to install python library dependencies on the container.

This should make a program menu entry for vmt_manager_gtk.

If you prefer to launch the program using a command line, use the following flatpak command:
```sh
flatpak run org.gpsnmeajp.vmt.vmt_manager
```

> [!WARNING]  
> Although vmt_manager_gtk itself does not contain code to read or write to the file system, please note that the OpenVR API may write certain files (e.g., log files) to your file system.  
> Therefore, ensure to include `--filesystem=~/.config/openvr` and `--filesystem=host` on flatpak arguments (By default, these arguments will be added automatically).  
> Even with `--filesystem=host` is present, `--filesystem=~/.config/openvr` must be specified, as flatpak hides all contents of `~/.config` directory except those specified in arguments.

## Tools used
I used GNOME Builder for building and testing, Cambalache for making UI, VSCode for editing.

Tools other than I mentioned is not supported.
