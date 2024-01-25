import sys, blessed, os, shutil, json
import subprocess

t = blessed.Terminal()

BL_DATA = os.path.join(os.environ.get("APPDATA"), "..", "LocalLow", "Stress Level Zero", "Bonelab")
BL_MODS = os.path.join(BL_DATA, "Mods")
BL_MODS_OLD = BL_MODS

BASEDIR = os.path.join(BL_DATA, ".blmm")
BACKUP = os.path.join(BASEDIR, "mods")
PROFILES = os.path.join(BASEDIR, "profiles")
NEWMODS = os.path.join(BL_DATA, "INSTALL_MODS_HERE")

def create_profile(name, barcodes = []):
    pfd = os.path.join(PROFILES, name)
    os.makedirs(pfd)

    with open(os.path.join(pfd, "mods.json"), "w+") as modsfile:
        modsfile.write(json.dumps({ "name": name, "barcodes": barcodes }, indent="\t"))

def execute(args):

    with open(os.path.join(BASEDIR, "current_profile"), "r") as cp:
        current_profile = cp.read()

    match args[0]:
        case "profile":
            if len(args) >= 2:
                match args[1]:
                    case "new":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            profile_name = input(f"Enter Profile Name: ")

                        pfd = os.path.join(PROFILES, profile_name)
                        if os.path.exists(pfd):
                            print("Profile Already Exists!")
                        else:
                            create_profile(profile_name)
                    case "del":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            profile_name = input(f"Enter Profile Name: ")
                        pfd = os.path.join(PROFILES, profile_name)
                        shutil.rmtree(pfd)
                        
                        shutil.rmtree(BL_MODS_OLD)
                        os.makedirs(BL_MODS_OLD)

                        if current_profile == profile_name:
                            with open(os.path.join(BASEDIR, "current_profile"), "w+") as cp:
                                current_profile = cp.write("")

                    case "activate":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            profile_name = input(f"Enter Profile Name: ")
                        
                        with open(os.path.join(PROFILES, profile_name, "mods.json"), "r") as modsjson:
                            mods = json.load(modsjson)

                            shutil.rmtree(BL_MODS_OLD)
                            os.makedirs(BL_MODS_OLD)

                            nms = len(mods['barcodes'])
                            
                            for i, barcode in enumerate(mods["barcodes"]):
                                print(f"{i + 1}/{nms} {barcode}" + " " * 20, end="\r" if i < nms - 1 else "\n")
                                os.symlink(os.path.join(BACKUP, barcode), os.path.join(BL_MODS_OLD, barcode))
                            
                            print(f"Activated {profile_name}.")
                        
                        with open(os.path.join(BASEDIR, "current_profile"), "w+") as cp:
                            cp.write(profile_name)
                    case "addmod":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            profile_name = input(f"Enter Profile Name: ")
                        
                        if len(args) >= 4:
                            bc_name = args[3]
                        else:
                            bc_name = input(f"Enter Barcode: ")

                        if not os.path.exists(os.path.join(BACKUP, bc_name)):
                            print("Mod doesn't exist")
                            return
                        
                        if profile_name == current_profile:
                            os.symlink(os.path.join(BACKUP, bc_name), os.path.join(BL_MODS_OLD, bc_name))
                        
                        mjspath = os.path.join(PROFILES, profile_name, "mods.json")

                        with open(mjspath, "r") as modsjson:
                            mods = json.load(modsjson)
                            
                            barcodes = mods["barcodes"]

                        with open(mjspath, "w+") as modsfile:
                            modsfile.write(json.dumps({ "name": profile_name, "barcodes": barcodes + [bc_name] }, indent="\t"))

                    case "removemod":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            profile_name = input(f"Enter Profile Name: ")
                        
                        if len(args) >= 4:
                            bc_name = args[3]
                        else:
                            bc_name = input(f"Enter Barcode: ")
                        
                        if profile_name == current_profile:
                            os.unlink(os.path.join(BL_MODS_OLD, bc_name))
                        
                        mjspath = os.path.join(PROFILES, profile_name, "mods.json")

                        with open(mjspath, "r") as modsjson:
                            mods = json.load(modsjson)
                            
                            barcodes: list = mods["barcodes"]
                            barcodes.remove(bc_name)

                        with open(mjspath, "w+") as modsfile:
                            modsfile.write(json.dumps({ "name": profile_name, "barcodes": barcodes }, indent="\t"))
                    
                    case "list":
                        if len(args) >= 3:
                            profile_name = args[2]
                        else:
                            print("\n".join([t.bold(p) if p == current_profile else p for p in os.listdir(PROFILES)]))
                            return
                        
                        mjspath = os.path.join(PROFILES, profile_name, "mods.json")

                        with open(mjspath, "r") as modsjson:
                            mods = json.load(modsjson)
                            print("\n".join(mods["barcodes"]))
                        
                    case _:
                        print("Invalid option")
        case "list":
            print("\n".join(os.listdir(BACKUP)))
        case "browse":
            paths = {
                "bl": BL_DATA,
                "blmm": BASEDIR,
                "mods": BACKUP,
                "profiles": PROFILES
            }

            path = paths[args[1]] if len(args) > 1 else paths["bl"]

            subprocess.Popen(f"explorer /e,\"{path}\"")
        case "help":
            print("""Bonelab Mod Manager CLI (v1.0) - By RedBigz
CLI Commands:

list - Lists all mods installed.

profile:
    list - Lists all profiles.

    new <name?> - Creates a profile.
    del <name?> - Deletes a profile.

    addmod <name?> <barcode?> - Adds a mod to a profile.
    removemod <name?> <barcode?> - Removes a mod from a profile.

    activate <name?> - Activates a profile.

browse:
    bl - Browses Bonelab's Data Folder.
    blmm - Browses ".blmm"
    mods - Browses All Mods.

quit/exit - Quits BLMM.

help - Prints this message.
""")
        case "quit" | "exit":
            sys.exit(0)
        case _:
            print("Invalid option")

if not os.path.exists(BASEDIR):
    print("We're moving your mods to our custom structure, please wait...")

    if os.path.islink(BL_MODS_OLD):
        BL_MODS = os.readlink(BL_MODS).replace("\\\\?\\", "")

    os.makedirs(BASEDIR)
    os.makedirs(PROFILES)
    os.makedirs(NEWMODS, exist_ok=True)

    shutil.copytree(BL_MODS, BACKUP)

    if os.path.islink(BL_MODS_OLD):
        os.unlink(BL_MODS_OLD)
    else:
        shutil.rmtree(BL_MODS_OLD)
    
    os.mkdir(BL_MODS_OLD)

    create_profile("main", os.listdir(BACKUP))
    execute(["profile", "activate", "main"])

    print("All of your mods were transferred to a profile named \"main\". A folder called \"INSTALL_MODS_HERE\" was created. Install any new mods (unzipped) to that location, then add the mod barcodes via BLMM to your current profile.")

    print("-" * 15)

newmods = os.listdir(NEWMODS)
nms = len(newmods)

if nms != 0:
    print("It appears that you have downloaded new mods, copying...")

    for i, file in enumerate(newmods):
        nmf = os.path.join(NEWMODS, file)
        shutil.copytree(nmf, os.path.join(BACKUP, file))
        shutil.rmtree(nmf)
        print(f"{i + 1}/{nms} {file}" + " " * 20, end="\r" if i < nms - 1 else "\n")
        execute(["profile", "addmod", "main", file]) # Adds new mods to "main"
    
    print("-" * 15)

if not len(sys.argv) > 1:
    try:
        while True:
            prompt = input(f"{t.bold('blmm>')} ")
            if len(prompt) != 0:
                execute(prompt.split(" "))
    except KeyboardInterrupt:
        sys.exit(0)
else:
    execute(sys.argv[1:])