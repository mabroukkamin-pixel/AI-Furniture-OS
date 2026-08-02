
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



