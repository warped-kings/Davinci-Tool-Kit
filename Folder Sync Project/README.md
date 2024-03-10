For Windows users:
Save the "Folder Sync.py" file in the following folder:
C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility

Upon next Davinci reload, you should see the script in Workspace > Scripts

You'd need to edit the file path line at the end and direct it to your "folder_sync.json" file.
You need to add a 2nd "\\" to the file path for windows directories. "C:\" becomes "C:\\"

The folder_list function will import all specified media types from the directories the json file includes
and import them into your current project.
