# Integration Tests

This directory contains integration tests for the Skyrim TTRPG Campaign Manager custom content.

## Running Tests

To run all integration tests:

```bash
cd tests
python3 test_integration.py
```

## Test Coverage

The integration test suite validates:

1. **Dragonbreak Manager** - Timeline fracture system
   - Creating timeline fractures
   - Tracking NPCs across branches
   - Tracking factions across branches
   - Tracking quests across branches
   - Defining and triggering consequences

2. **Story Manager Integration** - Dragonbreak support in Story Manager
   - Dragonbreak Manager integration
   - Initiating dragonbreaks through story manager
   - Tracking parallel events

3. **Faction Allegations** - Side Plot C mechanics
   - Loading faction data
   - Adding allegations
   - Updating evidence
   - Retrieving allegations
   - Tracking Thalmor plots
   - Advancing plot clocks

4. **Documentation Updates** - Campaign module documentation
   - Removal of Dragonborn-focused content
   - Civil War narrative focus
   - Dragonbreak system references
   - Neutral faction references

## Test Results

All tests should pass. If any tests fail, check:
- Required data files exist in `../data/`
- Python scripts are in `../scripts/`
- Documentation is in `../docs/`

## Notes

- Tests use temporary state directories to avoid modifying campaign data
- Test artifacts are automatically cleaned up after execution
