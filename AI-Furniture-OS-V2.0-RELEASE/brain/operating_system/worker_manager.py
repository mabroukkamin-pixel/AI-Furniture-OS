
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



