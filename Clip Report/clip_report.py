import json
from datetime import timedelta

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

def clip_info(file):
    from datetime import timedelta
    pm = resolve.GetProjectManager()
    p = pm.GetCurrentProject()
    t_count = p.GetTimelineCount()
    clip_data = {}
    for timeline in range(t_count):
        t = p.GetTimelineByIndex(timeline+1)
        t_name = t.GetName()
        print(t_name)
        fps = t.GetSetting("timelineFrameRate")
        tracks = t.GetTrackCount("video")
        for track in range(tracks):
            clips = t.GetItemListInTrack("video",track+1)
            for clip in clips:
                count = clip.GetStart() - t.GetStartFrame()
                td = timedelta(seconds=(count/fps))
                add_to_key(clip_data,clip.GetName(), {"timeline":t_name,"track": track+1,"time": td.seconds})

    with open(file,"w") as mf:
        mf.write(json.dumps(clip_data,indent=4))
        

def add_to_key(data_dict, key, value):
    # Ensure the key exists with a default value (empty list in this case)
    data_dict.setdefault(key, []).append(value)

    

if __name__ == "__main__":
    #windows example filepath (note the "r" when using single slash
    #   r"C:\Users\**replace with user**\Desktop\clip report.json"
    #   "C:\\Users\\**replace with user**\\Desktop\\clip report.json"

    clip_info("./clip report.json")
