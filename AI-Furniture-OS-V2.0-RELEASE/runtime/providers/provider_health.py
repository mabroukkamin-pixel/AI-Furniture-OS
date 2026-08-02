import time
import json
import os


STATUS_FILE = (
    "runtime/providers/provider_status.json"
)


DEFAULT_COOLDOWN = 60


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

            self.status = self.default_status()
            self.save()



    def default_status(self):

        return {

            "nano_banana": {

                "available": True,
                "reason": None,
                "failures": 0,
                "last_failure": None,
                "cooldown_until": None

            },


            "mock": {

                "available": True,
                "reason": None,
                "failures": 0,
                "last_failure": None,
                "cooldown_until": None

            }

        }



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
        reason
    ):


        if provider not in self.status:

            return


        now = time.time()


        self.status[provider]["available"] = False

        self.status[provider]["reason"] = reason

        self.status[provider]["failures"] += 1

        self.status[provider]["last_failure"] = now


        self.status[provider]["cooldown_until"] = (
            now + DEFAULT_COOLDOWN
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

        self.status[provider]["cooldown_until"] = None


        self.save()



    def is_available(
        self,
        provider
    ):


        data = self.status.get(
            provider,
            {}
        )


        if not data:

            return False



        cooldown = data.get(
            "cooldown_until"
        )


        if cooldown:


            if time.time() >= cooldown:


                self.mark_available(
                    provider
                )

                return True



        return data.get(
            "available",
            False
        )



    def get_status(self):

        return self.status