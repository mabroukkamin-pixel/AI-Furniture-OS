from brain.autonomous.autonomous_engine import AutonomousEngine


class DecisionMonitor:


    def check(self):

        return AutonomousEngine().monitor()



if __name__=='__main__':

    print(
        DecisionMonitor().check()
    )
