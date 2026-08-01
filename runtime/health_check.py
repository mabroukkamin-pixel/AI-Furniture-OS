from runtime.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    is_gemini_configured
)


print("==============================")
print("AI FURNITURE OS HEALTH CHECK")
print("==============================")


print("MODEL:")
print(GEMINI_MODEL)

print()

print("API KEY:")
if GEMINI_API_KEY:
    print("FOUND")
else:
    print("MISSING")

print()

print("CONFIG:")
print(
    is_gemini_configured()
)