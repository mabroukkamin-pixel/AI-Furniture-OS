
from brain.commander.command_router import CommandRouter

if __name__=="__main__":

    result = CommandRouter().route("PRODUCTION")

    print(result)

