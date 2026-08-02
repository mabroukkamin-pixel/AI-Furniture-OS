
from brain.autonomous.agent_core import AutonomousAgent
from brain.control.command_center import CommandCenter


class MasterOrchestrator:


    def start(self):

        return {

            "command_center":
                CommandCenter().status(),

            "autonomous":
                AutonomousAgent().run(),

            "status":"ONLINE"

        }


if __name__=="__main__":

    print(
        MasterOrchestrator().start()
    )
