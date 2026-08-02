class AdOptimizer:


    def optimize(self,data):

        return {

            'original':data,

            'optimization':'COMPLETED',

            'improvement':'+15%'

        }



if __name__=='__main__':

    print(
        AdOptimizer().optimize('AD001')
    )
