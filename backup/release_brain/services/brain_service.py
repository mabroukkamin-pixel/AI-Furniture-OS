from brain.services.knowledge_service import KnowledgeService
from brain.services.decision_service import DecisionService
from brain.services.context_service import ContextService


class BrainService:

    def __init__(self, brain):

        self.brain = brain

        self.knowledge = KnowledgeService(brain)

        self.decision = DecisionService(brain)

        self.context = ContextService(brain)