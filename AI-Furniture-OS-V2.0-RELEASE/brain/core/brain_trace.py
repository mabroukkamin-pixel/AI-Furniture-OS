class BrainTrace:


    def __init__(self):

        self.records = []


    def append(self, item):

        self.records.append(item)


    def record(
        self,
        stage,
        output_data
    ):

        self.records.append({

            "stage": stage,

            "output": output_data

        })


    def export(self):

        return self.records


    def clear(self):

        self.records = []