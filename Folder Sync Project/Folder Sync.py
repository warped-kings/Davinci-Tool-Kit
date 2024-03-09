#!/usr/bin/env python
import sys
import os
import json

def GetResolve():
    try:
    # The PYTHONPATH needs to be set correctly for this import statement to work.
    # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath=os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath="/opt/resolve/libs/Fusion/Modules/"

        # check if the default path has it...
        print("Unable to find module DaVinciResolveScript from $PYTHONPATH - trying default locations")
        try:
            import imp
            bmd = imp.load_source('DaVinciResolveScript', expectedPath+"DaVinciResolveScript.py")
        except ImportError:
            # No fallbacks ... report error:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: "+expectedPath)
            sys.exit()

    return bmd.scriptapp("Resolve")

resolve = GetResolve()


class DavinciToolKit:
    def __init__(self):
        self.pm = resolve.GetProjectManager()

        return
    
    def folder_sync(self,bin_name,folder):
        mediastorage = resolve.GetMediaStorage()
        medpool = resolve.GetMediaPool()
        root = medpool.GetRootFolder()
        medpool.SetCurrentFolder(root)
        subs = root.GetSubFolderList()
        for sub in subs:
            if sub.GetName() == bin_name:
                medpool.SetCurrentFolder(sub)
        items = mediastorage.AddItemListToMediaPool(folder)

    
    def folder_list(self,file):
        mediastorage = resolve.GetMediaStorage()
        media_files = self.find_media_files(file)
        mediastorage.AddItemListToMediaPool(media_files)


    def find_media_files(self,config_file):
        # Load the JSON configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        media_files = []

        # Iterate over each folder entry in the configuration
        for folder in config["folders"]:
            folder_path = folder["path"]
            extensions = folder["media"]

            # Ensure the folder path exists
            if os.path.exists(folder_path):
                # Iterate over the files in the folder
                for filename in os.listdir(folder_path):
                    # Get the file extension
                    _, extension = os.path.splitext(filename)
                    extension = extension.lower()[1:]  # Remove the leading dot

                    # Check if the file extension is allowed
                    if extension in extensions:
                        media_files.append(os.path.join(folder_path, filename))
        return media_files


if __name__ == "__main__":
    import time
    if resolve:
        dtk = DavinciToolKit()
        dtk.folder_list("C:\\**Your**\\**Path**\\**to file**\\folder_sync.json")
    time.sleep(3)
