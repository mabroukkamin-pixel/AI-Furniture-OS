import datetime


class JobManager:


    def start(self, product):

        return {
            "product": product,
            "started": str(datetime.datetime.now()),
            "status": "running"
        }


    def finish(self, job):

        job["status"] = "completed"

        job["finished"] = str(
            datetime.datetime.now()
        )

        return job