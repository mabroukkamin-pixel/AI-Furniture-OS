class ExperienceEngine:


    def evaluate(self, state):

        score = 0
        reasons = []


        # Decision quality
        if getattr(
            state,
            "decision",
            {}
        ):

            score += 25

            reasons.append(
                "decision_created"
            )


        # Design DNA
        if getattr(
            state,
            "design_dna",
            {}
        ):

            score += 25

            reasons.append(
                "design_dna_created"
            )


        # Prompt audit

        audit = getattr(
            state,
            "audit",
            {}
        )


        if audit:

            score += 25

            reasons.append(
                "prompt_audit_passed"
            )


        # Real generation check

        generation = getattr(
            state,
            "generation",
            {}
        )


        if isinstance(
            generation,
            dict
        ):

            status = generation.get(
                "status"
            )

            image = generation.get(
                "image"
            )


            if (
                status == "success"
                and image
            ):

                score += 25

                reasons.append(
                    "generation_completed"
                )

            else:

                reasons.append(
                    "generation_failed"
                )


        state.experience = {

            "score": score,

            "success":
                score >= 75,

            "reasons":
                reasons
        }


        return state