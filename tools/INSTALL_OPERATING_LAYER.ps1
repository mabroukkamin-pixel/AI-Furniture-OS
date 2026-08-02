
$ErrorActionPreference="Stop"


Write-Host ""
Write-Host "================================="
Write-Host " INSTALL AIFOS OPERATING LAYER "
Write-Host "================================="


New-Item brain\operating_system -ItemType Directory -Force | Out-Null



@"

import json
import os
import datetime



class TaskQueue:


    def __init__(self):

        self.queue=[]


    def add(self,task):

        self.queue.append(task)


    def get_all(self):

        return self.queue



"@ | Out-File brain\operating_system\task_queue.py -Encoding utf8





@"

import os



class WorkerManager:


    def __init__(self):

        self.workers=[]


    def register(self,name):

        self.workers.append(name)


    def status(self):

        return {

        "workers":self.workers,

        "count":len(self.workers)

        }



"@ | Out-File brain\operating_system\worker_manager.py -Encoding utf8





@"

import os


class PluginManager:


    def __init__(self):

        self.plugins=[]



    def scan(self):


        root="brain"


        for item in os.listdir(root):

            if item not in [

            "legacy",

            "__pycache__"

            ]:

                self.plugins.append(item)



        return self.plugins



"@ | Out-File brain\operating_system\plugin_manager.py -Encoding utf8






@"

import datetime
import json

from brain.operating_system.task_queue import TaskQueue
from brain.operating_system.worker_manager import WorkerManager
from brain.operating_system.plugin_manager import PluginManager



class CommandCenter:


    def __init__(self):

        self.queue=TaskQueue()

        self.workers=WorkerManager()

        self.plugins=PluginManager()



    def execute(self,command):


        self.queue.add(command)


        self.workers.register(command)


        return {

        "command":command,

        "workers":
        self.workers.status(),

        "plugins":
        self.plugins.scan(),

        "time":
        str(datetime.datetime.now())

        }




if __name__=="__main__":


    result=CommandCenter().execute(
    "SYSTEM_BOOT"
    )


    print(
    json.dumps(
    result,
    indent=4
    )
    )

"@ | Out-File brain\operating_system\command_center.py -Encoding utf8





git add .

git commit -m "Add AI Furniture OS Operating Layer"

git push origin main



Write-Host ""
Write-Host "================================="
Write-Host " OPERATING LAYER INSTALLED "
Write-Host "================================="


