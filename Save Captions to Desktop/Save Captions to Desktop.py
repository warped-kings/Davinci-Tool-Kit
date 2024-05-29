import DaVinciResolveScript as dvr
import os


def get_subtitles(track, t):
    subtitle = t.GetItemListInTrack("subtitle",1)
    text = []
    location = os.path.expanduser(f"~/Desktop/{p.GetName()} Subtitle Track {track+1}.txt")
    for sub in subtitle:
        text.append(sub.GetName())
    with open(location,"w") as mf:
        mf.write("\n".join(text))

if __name__ == "__main__":
    resolve = dvr.scriptapp("Resolve")
    fusion = resolve.Fusion()
    pm = resolve.GetProjectManager()
    p = pm.GetCurrentProject()
    t = p.GetCurrentTimeline()
    count = t.GetTrackCount("subtitle")
    for track in range(count):
        get_subtitles(track, t)
