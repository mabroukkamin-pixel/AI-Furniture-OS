from brain.intelligence_core.master_brain import MasterBrain


class IntelligenceReporter:


    def report(self):

        return MasterBrain().run()



if __name__=='__main__':

    print(
        IntelligenceReporter().report()
    )

