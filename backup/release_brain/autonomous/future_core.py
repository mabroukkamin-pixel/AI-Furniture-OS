from brain.evolution.evolution_engine import EvolutionEngine
from brain.autonomous.manager import AutonomousManager
from brain.quality.quality_judge import QualityJudge


class FutureCore:


    def run(self):

        return {

        "evolution":
        EvolutionEngine().analysis(),

        "manager":
        AutonomousManager().run(),

        "quality":
        QualityJudge().evaluate()

        }
