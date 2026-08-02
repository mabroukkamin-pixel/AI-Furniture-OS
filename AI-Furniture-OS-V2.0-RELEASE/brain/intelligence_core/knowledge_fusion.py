from brain.intelligence_core.master_brain import MasterBrain


class KnowledgeFusion:


    def fuse(self):

        return {

            'fusion':'ACTIVE',

            'brain':MasterBrain().run()

        }



if __name__=='__main__':

    print(
        KnowledgeFusion().fuse()
    )

