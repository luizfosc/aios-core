# Script Quality Gate Checklist

## Pre-Delivery Checks

### Executability
- [ ] Script runs with `node script.js` without modification
- [ ] No hardcoded credentials (all via .env)
- [ ] No extra dependencies beyond stagehand + zod
- [ ] Imports are correct (ES modules with .js extensions if needed)

### Error Handling
- [ ] try/catch wraps all Stagehand operations
- [ ] Meaningful error messages (not just generic "Error occurred")
- [ ] Timeout handling (custom timeouts where needed)
- [ ] Browser always closes in `finally` block

### Output
- [ ] Script produces expected output (JSON, file, console)
- [ ] Output matches Zod schema (if extraction)
- [ ] Output saved to file (not just console.log)

### Testing
- [ ] Ran with --headed and observed correct behavior
- [ ] Output validated against user expectation
- [ ] Edge case: timeout doesn't crash (graceful failure)
- [ ] Edge case: missing element doesn't crash

### Documentation
- [ ] Script has header comment with usage instructions
- [ ] CLI flags documented (--headed, --headless, --model)
- [ ] Output format documented

### Cost
- [ ] Uses cheapest sufficient model (gpt-4o-mini default)
- [ ] page.* used for deterministic operations (not act/agent)
- [ ] No unnecessary agent mode (extract where possible)

## Verdict

- **PASS:** All checks marked, script works correctly
- **FAIL:** Any check unmarked → fix before delivery
