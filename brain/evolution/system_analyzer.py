import os
import json
from datetime import datetime


class SystemAnalyzer:


    def scan(self):

        layers = [

            "brain/core",
            "brain/decision_graph",
            "brain/knowledge",
            "brain/fusion",
            "brain/visual_memory",
            "brain/learning",
            "brain/self_healing",
            "brain/system",
            "runtime"

        ]


        result={}


        for layer in layers:

            result[layer] = (
                "ACTIVE"
                if os.path.exists(layer)
                else
                "MISSING"
            )


        return result



    def report(self):

        return {

            "time":
            datetime.now().isoformat(),

            "layers":
            self.scan()

        }
