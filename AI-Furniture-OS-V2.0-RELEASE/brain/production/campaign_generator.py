import datetime


class CampaignGenerator:


    def generate(self,product):

        return {

            'product':product,

            'campaign':'Luxury Gulf Campaign',

            'channels':[

                'Instagram',
                'TikTok',
                'Facebook'

            ],

            'status':'CREATED',

            'time':str(datetime.datetime.now())

        }



if __name__=='__main__':

    print(
        CampaignGenerator().generate('Partition001')
    )
