"""
PyBackup - A simple personal backup utility
Copyright (C) 2023  Robert T. Fowler IV

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from pathlib import Path
from config import *
import json
import zipfile
import datetime as dt

def zip_backup(source,dest):
    source = Path(source)
    timestamp = str(dt.datetime.now()).replace(" ","-").replace(":","")[:17]
    dest = Path(dest,source.stem  + "-" + timestamp + ".zip")


    print(f"Backing up {source} to {dest}....")
    with zipfile.ZipFile(dest, mode="w") as archive:
        for file_path in source.rglob("*"):
            archive.write(file_path,
            arcname=file_path.relative_to(source))
            print(file_path)
            
    print("Backup completed.")

# TODO Warn if overwriting existing backup name

def save_backup(source,dest,name, backupsDropDown):
    with open(varSavedBackups,"r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    saved_backups[name] = {}
    saved_backups[name]["source"]=source    
    saved_backups[name]["dest"]=dest

    with open(varSavedBackups,"w",encoding="utf-8") as f:
        json.dump(saved_backups,f)

    backupsDropDown.delete(0,"end")
    backups_list = list(saved_backups.keys())
    backupsDropDown['values'] = backups_list

def load_backup(name):
    with open(varSavedBackups,"r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    return saved_backups[name]

def delete_backup(name):
    with open(varSavedBackups,"r",encoding="utf-8") as f:
        saved_backups = json.load(f)
    n = saved_backups.pop(name)
    with open(varSavedBackups,"w",encoding="utf-8") as f:
        json.dump(saved_backups,f)

