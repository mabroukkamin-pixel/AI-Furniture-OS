
from brain.orchestrator.master_orchestrator import MasterOrchestrator


print("")
print("=================================")
print(" AI FURNITURE OS MASTER CONTROL ")
print("=================================")


system=MasterOrchestrator()


report=system.execute()


for item in report["health"]:

    print(
    item["module"],
    ":",
    item["status"]
    )


print("")
print("MASTER ORCHESTRATOR READY")

