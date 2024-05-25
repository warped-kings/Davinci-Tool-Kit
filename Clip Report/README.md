For Windows users: Save the "clip_report.py" file in the following folder: C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility

Upon next Davinci reload, you should see the script in Workspace > Scripts

You'd need to edit the file path line at the end and direct it to your path of choosing "clip report.json" file. 
You need to add a 2nd "\\" to the file path for windows directories. "C:\Users\**replace with user**\Desktop\clip report.json"" becomes ""C:\\\\Users\\\\**replace with user**\\\\Desktop\\\\clip report.json"

This will return a json file with all clips that are in a timeline, what timelines they are in, and the time in seconds
