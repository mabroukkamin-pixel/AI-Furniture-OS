import datetime
import json
import os
import subprocess
import sys


class FinalOrchestrator:


    def __init__(self):

        self.report={

            'system':'AI Furniture OS V2',

            'time':str(datetime.datetime.now()),

            'status':'STARTING',

            'modules':{}

        }


    def check(self,name,path):

        exists=os.path.exists(path)

        self.report['modules'][name]={

            'exists':exists,

            'status':'READY' if exists else 'MISSING'

        }


    def run_brain(self):

        try:

            result=subprocess.run(

                [
                    sys.executable,
                    '-m',
                    'brain.intelligence_core.master_brain'
                ],

                capture_output=True,

                text=True

            )

            self.report['master_brain']='EXECUTED'

        except Exception as e:

            self.report['master_brain']=str(e)



    def run_auto(self):

        try:

            subprocess.run(

                [
                    sys.executable,
                    '-m',
                    'brain.commander.command_router',
                    'AUTO'
                ]

            )

            self.report['auto_loop']='COMPLETED'


        except Exception as e:

            self.report['auto_loop']=str(e)



    def save(self):

        os.makedirs(

            'docs/reports',

            exist_ok=True

        )


        with open(

            'docs/reports/final_orchestrator_report.json',

            'w',

            encoding='utf8'

        ) as f:

            json.dump(

                self.report,

                f,

                indent=4,

                ensure_ascii=False

            )


        print(
            'REPORT:',
            'docs/reports/final_orchestrator_report.json'
        )



    def run(self):


        print('')

        print('=================================')

        print(' AI FURNITURE OS FINAL CORE ')

        print('=================================')



        modules={

            'Brain':'brain',

            'Decision Graph':'brain/decision_graph',

            'Visual Memory':'brain/visual_memory',

            'Learning':'brain/learning',

            'Evolution':'brain/evolution',

            'Production':'brain/production',

            'Intelligence Core':'brain/intelligence_core',

            'Runtime':'runtime'

        }



        for name,path in modules.items():

            self.check(name,path)



        print('')

        print('MASTER BRAIN')

        self.run_brain()



        print('')

        print('AUTO LEARNING LOOP')

        self.run_auto()



        self.report['status']='READY'


        self.save()


        print('')

        print('=================================')

        print(' AI FURNITURE OS READY ')

        print('=================================')



if __name__=='__main__':

    FinalOrchestrator().run()

