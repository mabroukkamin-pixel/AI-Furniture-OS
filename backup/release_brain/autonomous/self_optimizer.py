from brain.autonomous.autonomous_engine import AutonomousEngine


class SelfOptimizer:


    def optimize(self):

        return AutonomousEngine().optimize()



if __name__=='__main__':

    print(
        SelfOptimizer().optimize()
    )
