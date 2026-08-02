class MarketPredictor:


    def predict(self,market):

        return {

            'market':market,

            'trend':'luxury_home',

            'confidence':95

        }



if __name__=='__main__':

    print(
        MarketPredictor().predict('Kuwait')
    )
