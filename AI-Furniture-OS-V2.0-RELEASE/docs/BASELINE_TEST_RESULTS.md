# Baseline Test Results

## Summary

- Baseline status: FAIL
- Python version: 3.14.6
- Test runner used: unittest discovery
- No code files were modified.

## Commands Run

1. `& "C:/Users/windows 1/AppData/Local/Python/pythoncore-3.14-64/python.exe" -m pytest -q`
   - Result: failed immediately because `pytest` is not installed in the current environment.

2. `& "C:/Users/windows 1/AppData/Local/Python/pythoncore-3.14-64/python.exe" -m unittest discover -q`
   - Result: executed and reported import/collection errors.

## Test Counts

- Total tests discovered: 8
- Successful tests: 0
- Failed tests: 8

## Failed Tests and Short Reasons

- `test_brief`
  - ImportError: `No module named 'brain.creative_engine'`

- `test_brief_generator`
  - ImportError: `No module named 'brain.creative_engine'`

- `test_final_prompt`
  - ImportError: `No module named 'brain.context'`

- `test_gemini`
  - ImportError: `No module named 'dotenv'`

- `test_gemini_image`
  - ImportError: `No module named 'google'`

- `test_metadata`
  - ImportError: `No module named 'brain.reference_engine'`

- `test_models`
  - ImportError: `No module named 'google'`

- `test_reference_scan`
  - ImportError: `No module named 'brain.reference_memory'`

## Collection / Import Errors

- The test run failed during module import before any test body could execute.
- The reported failures are import-level issues rather than assertion failures.
