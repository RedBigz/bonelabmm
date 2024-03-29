<p align="center">
<img src="res/icon.png">
</p>
<h1 align="center">Bonelab Mod Manager</h1>
<p align="center">
BLMM is a CLI app which allows you to create custom mod profiles in Bonelab for Traditional Map/Weapon Mods.
<b>This is not for code mods.</b>
</p>

## Running
### Binaries
Download the .exe from the [releases](https://github.com/RedBigz/bonelabmm/releases) and run it.
### From source
See [the compiling section](#compiling) if you want to contribute or build it yourself.

## Basics
### Profiles
By default all your mods before running for the first time will be put into a profile named **main**.

To create a profile, run either:
```
blmm> profile new <name>
```
or...
```ps1
./blmm.exe profile new <name>
```

### Adding Mods
Run `browse bl` and go to INSTALL_MODS_HERE. Add new mods there, and then add the mod barcodes to your profile with `profile addmod`, for example:
```ps1
./blmm.exe profile addmod RedBigz.ExampleMod
```

### Launching a Profile
Run this command:
```ps1
./blmm.exe profile activate <profile name>
```
After you ran the command, launch Bonelab.

**For other commands run `./blmm.exe help`.**

## Compiling
First, clone the repo.

```sh
git clone https://github.com/RedBigz/bonelabmm
```

Then, create a venv and install the requirements.

```sh
python -m venv .venv
pip install -r requirements.txt
```

### Make (Recommended)

Run `make`.
```sh
make
```

A `blmm.exe` should appear in the root directory of the repo.

Then you can run `make clean` to clean the `dist` and `build` directories, along with removing the spec files.

### PyInstaller

Run `pyinstaller` to create the executable.

```sh
pyinstaller --icon=res/icon.ico --onefile main.py
```
