from brain.autonomous.autonomous_engine import AutonomousEngine


class TaskManager:


    def run(self):

        engine=AutonomousEngine()

        return engine.optimize()



if __name__=='__main__':

    print(
        TaskManager().run()
    )
