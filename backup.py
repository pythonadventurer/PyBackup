from pathlib import Path
import configparser
import json
import zipfile
import datetime as dt

def zip_backup(source,dest):
    source = Path(source)
    timestamp = str(dt.datetime.now()).replace(" ","-").replace(":","")[:17]
    dest = Path(dest,timestamp + "-" + source.stem + ".zip")


    print(f"Backing up {source} to {dest}....")
    with zipfile.ZipFile(dest, mode="w") as archive:
        for file_path in source.rglob("*"):
            archive.write(file_path,
            arcname=file_path.relative_to(source))
    print("Backup completed.")

def save_backup(source,dest,name):
    with open("backups.json","r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    saved_backups[name] = {}
    saved_backups[name]["source"]=source    
    saved_backups[name]["dest"]=dest

    with open("backups.json","w",encoding="utf-8") as f:
        json.dump(saved_backups,f)

def load_backup(name):
    with open("backups.json","r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    return saved_backups[name]

def delete_backup(name):
    with open("backups.json","r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    n = saved_backups.pop(name)
    with open("backups.json","w",encoding="utf-8") as f:
        json.dump(saved_backups,f)

