import datetime


class ProductManager:


    def analyze(self,product):

        return {

            'product':product,

            'status':'ANALYZED',

            'time':str(datetime.datetime.now()),

            'score':95

        }



if __name__=='__main__':

    print(
        ProductManager().analyse('Partition001')
    )
