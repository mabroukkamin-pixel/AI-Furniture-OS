from brain.intelligence_core.master_brain import MasterBrain


class DecisionOrchestrator:


    def decide(self):

        return MasterBrain().run()



if __name__=='__main__':

    print(
        DecisionOrchestrator().decide()
    )

