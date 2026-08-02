import time
import json
import os


STATUS_FILE = (
    "runtime/providers/provider_status.json"
)


class ProviderHealth:


    def __init__(self):

        self.file = STATUS_FILE


        if os.path.exists(self.file):

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                self.status = json.load(f)


        else:

            self.status = {

                "nano_banana": {

                    "available": True,
                    "reason": None,
                    "failures": 0,
                    "last_failure": None,
                    "retry_after": None
                },


                "mock": {

                    "available": True,
                    "reason": None,
                    "failures": 0,
                    "last_failure": None,
                    "retry_after": None
                }

            }

            self.save()



    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.status,
                f,
                indent=4,
                ensure_ascii=False
            )



    def mark_failed(
        self,
        provider,
        reason,
        cooldown=600
    ):


        if provider not in self.status:
            return


        self.status[provider]["available"] = False

        self.status[provider]["reason"] = reason

        self.status[provider]["failures"] += 1


        self.status[provider]["last_failure"] = time.time()


        self.status[provider]["retry_after"] = (
            time.time() + cooldown
        )


        self.save()



    def mark_available(
        self,
        provider
    ):


        if provider not in self.status:
            return


        self.status[provider]["available"] = True

        self.status[provider]["reason"] = None

        self.status[provider]["retry_after"] = None


        self.save()



    def is_available(
        self,
        provider
    ):


        data = self.status.get(
            provider,
            {}
        )


        if not data.get(
            "available",
            False
        ):


            retry = data.get(
                "retry_after"
            )


            if retry and time.time() >= retry:

                self.mark_available(
                    provider
                )

                return True


            return False


        return True



    def get_status(self):

        return self.status