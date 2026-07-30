from brain.reference_memory.reference_scanner import ReferenceScanner


scanner = ReferenceScanner(
    "reference_library"
)


result = scanner.scan_all()


print(result)