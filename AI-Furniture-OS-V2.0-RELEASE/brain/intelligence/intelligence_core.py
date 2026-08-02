
from brain.intelligence.agent_manager import AgentManager
from brain.intelligence.expert_council import ExpertCouncil
from brain.intelligence.planner import Planner
from brain.intelligence.reasoning_engine import ReasoningEngine



class IntelligenceCore:


    def __init__(self):

        self.agents=AgentManager()

        self.experts=ExpertCouncil()

        self.planner=Planner()

        self.reasoner=ReasoningEngine()



    def run(self,task):

        return {

        "task":task,

        "plan":
        self.planner.create_plan(task),

        "experts":
        self.experts.consult(),

        "reason":
        self.reasoner.reason(task)

        }



if __name__=="__main__":

    print(
    IntelligenceCore().run(
    "Furniture Product Analysis"
    )
    )


