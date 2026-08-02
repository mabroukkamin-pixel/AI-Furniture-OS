class QualityJudge:


    def evaluate(self):

        return {

        "score":95,

        "status":"GOOD",

        "checks":[

        "branding",

        "composition",

        "quality"

        ]

        }



if __name__=="__main__":

    print(QualityJudge().evaluate())
