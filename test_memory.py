from brain.memory.memory_manager import MemoryManager


memory = MemoryManager()


print(
    "LOAD:"
)

print(
    memory.get(
        "Partition001"
    )
)


print(
    "ALL:"
)

print(
    memory.all()
)