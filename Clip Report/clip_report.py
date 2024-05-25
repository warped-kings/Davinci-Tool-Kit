import json
from datetime import timedelta
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")

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
                add_to_key(clip_data,clip.GetName(), {"track":t_name,"time": td.seconds})

    with open(file,"w") as mf:
        mf.write(json.dumps(clip_data,indent=4))
        

def add_to_key(data_dict, key, value):
    # Ensure the key exists with a default value (empty list in this case)
    data_dict.setdefault(key, []).append(value)

    

if __name__ == "__main__":
    clip_info("./clip report.json")
