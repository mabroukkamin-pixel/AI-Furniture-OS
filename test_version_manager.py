from runtime.artifacts.version_manager import VersionManager

vm = VersionManager()

print("Next :", vm.next_version("Partition001"))
print("Latest :", vm.latest_version("Partition001"))
print("All :", vm.list_versions("Partition001"))