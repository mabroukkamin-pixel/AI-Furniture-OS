from brain.intelligence_core.master_brain import MasterBrain


class ContextManager:


    def build(self):

        return MasterBrain().run()



if __name__=='__main__':

    print(
        ContextManager().build()
    )

