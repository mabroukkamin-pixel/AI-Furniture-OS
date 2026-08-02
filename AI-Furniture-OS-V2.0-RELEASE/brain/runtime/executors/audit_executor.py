class AuditExecutor:

    def __init__(self, auditor):
        self.auditor = auditor

    def execute(self, state):

        state.audit = self.auditor.audit(state)

        return state
