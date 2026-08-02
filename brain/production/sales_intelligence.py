import datetime


class SalesIntelligence:


    def analyze(self):

        return {

            'sales_state':'READY',

            'recommendation':

            'increase luxury furniture campaigns',

            'time':str(datetime.datetime.now())

        }



if __name__=='__main__':

    print(
        SalesIntelligence().analyse()
    )
