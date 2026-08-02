from brain.audit.audit_rules import AuditRules
from brain.audit.audit_score import AuditScore
from brain.audit.audit_report import AuditReport


class PromptAuditor:

    def __init__(self):

        self.rules = AuditRules()

        self.score = AuditScore()

        self.report = AuditReport()


    def audit(self, context):

        rules = self.rules.check(
            context
        )

        score = self.score.calculate(
            rules
        )

        report = self.report.build(
            rules,
            score
        )

        print(report)

        return {

            "rules": rules,

            "score": score,

            "report": report

        }