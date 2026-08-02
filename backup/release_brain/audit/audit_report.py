class AuditReport:

    def build(self, rules, score):

        lines = []

        lines.append(
            "========================================"
        )

        lines.append(
            "PROMPT AUDIT REPORT"
        )

        lines.append(
            "========================================"
        )

        lines.append("")

        for name, passed in rules.items():

            status = "PASS" if passed else "FAIL"

            lines.append(
                f"{name.upper():20} {status}"
            )

        lines.append("")
        lines.append(
            "----------------------------------------"
        )

        lines.append(
            f"Score : {score['score']} / {score['maximum']}"
        )

        lines.append(
            f"Success : {score['percentage']}%"
        )

        return "\n".join(lines)