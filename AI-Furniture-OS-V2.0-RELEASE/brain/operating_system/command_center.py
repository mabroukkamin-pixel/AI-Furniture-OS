
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

