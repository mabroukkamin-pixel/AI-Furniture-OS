import os
import json
import datetime


class SystemAnalyzer:

    def __init__(self):
        self.result = {
            "time": str(datetime.datetime.now()),
            "modules": {},
            "score": 0,
            "status": "UNKNOWN"
        }


    def check(self,name,path):

        exists = os.path.exists(path)

        self.result["modules"][name] = {
            "exists": exists,
            "path": path
        }

        if exists:
            self.result["score"] += 10


    def analyze(self):

        modules = {
            "brain":"brain/core",
            "decision_graph":"brain/decision_graph",
            "fusion":"brain/fusion",
            "visual_memory":"brain/visual_memory",
            "learning":"brain/learning",
            "self_healing":"brain/self_healing",
            "runtime":"runtime",
            "knowledge":"brain/knowledge"
        }


        for name,path in modules.items():
            self.check(name,path)


        if self.result["score"] >= 80:
            self.result["status"]="HEALTHY"
        else:
            self.result["status"]="NEEDS_IMPROVEMENT"


        return self.result



if __name__=="__main__":

    analyzer = SystemAnalyzer()

    report = analyzer.analyze()


    os.makedirs(
        "docs/reports",
        exist_ok=True
    )


    with open(
        "docs/reports/evolution_report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )


    print(json.dumps(
        report,
        indent=4
    ))
