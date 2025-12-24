# City of Binds Test Suite Documentation

## Overview

This document describes the comprehensive test suite for the City of Binds library. The test suite is organized into four main categories: unit tests, integration tests, example tests, and performance tests.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── unit/                         # Pure unit tests (fast, isolated)
│   ├── test_bind.py             # Core bind class functionality
│   ├── test_trigger.py          # Trigger parsing and validation
│   ├── test_command.py          # Command creation and validation
│   └── utils/                   # Utility component tests
├── integration/                  # Component interaction tests
│   ├── test_bind_file_operations.py     # File creation and management
│   ├── test_rotating_bind_system.py     # Rotating bind workflows
│   └── test_validation_pipeline.py      # End-to-end validation
├── examples/                     # End-to-end tests as examples
│   ├── test_basic_character_setup.py    # Common character configurations
│   ├── test_complex_rotating_binds.py   # Advanced rotation scenarios
│   └── test_complete_bind_files.py      # Full character setups
└── performance/                  # Performance and stress tests
    └── test_large_bind_files.py         # Scale and performance testing
```

## Test Categories

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual components in isolation without dependencies.

**Characteristics**:
- Fast execution (< 1 second each)
- No file I/O operations
- No external dependencies
- Focus on single class/function behavior
- Comprehensive edge case coverage

**Key Test Files**:

- **`test_bind.py`**: Tests core `Bind` and `WASDBind` classes
  - Initialization with various trigger/command combinations
  - String representation and formatting
  - Equality comparisons and hashing
  - Input validation and error handling

- **`test_trigger.py`**: Tests `_Trigger` and `_WASDTrigger` classes
  - Trigger string parsing and normalization
  - Key and modifier validation
  - Case handling and format consistency
  - Invalid input rejection

- **`test_command.py`**: Tests `_Command` and `_CommandGroup` classes
  - Command string validation and normalization
  - Group operations and iteration
  - Slash command format handling
  - Special character management

**Running Unit Tests**:
```bash
pytest tests/unit/ -v
pytest tests/unit/ -m unit  # Using markers
```

### Integration Tests (`tests/integration/`)

**Purpose**: Test component interactions and workflows.

**Characteristics**:
- Moderate execution time (1-10 seconds each)
- File I/O operations in temporary directories
- Tests component combinations
- Focus on workflow correctness
- Cross-component compatibility

**Key Test Files**:

- **`test_bind_file_operations.py`**: Tests `BindFile` operations
  - File creation and content generation
  - Multiple bind management
  - Write operations and format preservation
  - Complex bind file scenarios

- **`test_rotating_bind_system.py`**: Tests rotating bind workflows
  - Template creation and processing
  - Multi-file generation and linking
  - Cross-file bind coordination
  - State management across rotations

**Running Integration Tests**:
```bash
pytest tests/integration/ -v
pytest tests/integration/ -m integration
```

### Example Tests (`tests/examples/`)

**Purpose**: Comprehensive end-to-end tests that serve as usage examples.

**Characteristics**:
- Longer execution time (up to 30 seconds each)
- Complete workflows from start to finish
- Real-world usage scenarios
- Documentation through code
- Demonstrate best practices

**Key Test Files**:

- **`test_basic_character_setup.py`**: Common character configurations
  - Basic movement bind setups
  - Communication bind systems
  - Power activation patterns
  - Complete character file generation

- **`test_complex_rotating_binds.py`**: Advanced rotation scenarios
  - Multi-trigger rotation systems
  - Form-shifting character management
  - Team leadership coordination
  - RandomWalk implementations

**Example Test Benefits**:
1. **Documentation**: Tests serve as executable documentation
2. **Validation**: Ensure complex scenarios work end-to-end
3. **Regression Prevention**: Catch breaking changes in workflows
4. **User Guidance**: Demonstrate proper library usage

**Running Example Tests**:
```bash
pytest tests/examples/ -v
pytest tests/examples/ -m example
pytest tests/examples/ -s  # Show print output from examples
```

### Performance Tests (`tests/performance/`)

**Purpose**: Validate performance characteristics and identify bottlenecks.

**Characteristics**:
- Variable execution time (can be slow)
- Large dataset testing
- Memory usage validation
- Stress testing scenarios
- Performance regression detection

**Key Test Files**:

- **`test_large_bind_files.py`**: Scale and performance testing
  - Large bind file creation and writing
  - Complex rotation generation performance
  - Memory usage with large datasets
  - Stress tests for extreme scenarios

**Performance Benchmarks**:
- Bind creation rate: > 100 binds/second
- File write operations: < 2 seconds for 50+ binds
- Rotation generation: < 10 seconds for 100-file rotations
- Memory efficiency: Linear scaling with dataset size

**Running Performance Tests**:
```bash
pytest tests/performance/ -v
pytest tests/performance/ -m performance
pytest tests/performance/ -m "performance and not slow"  # Skip slow tests
```

## Test Fixtures

### Shared Fixtures (`conftest.py`)

**Unit Test Fixtures**:
- `sample_trigger_strings`: Various trigger combinations for validation
- `sample_commands`: Command strings for testing
- `sample_power_names`: Game power names for realistic testing

**Integration Test Fixtures**:
- `basic_bind`, `wasd_bind`, `complex_bind`: Pre-built bind objects
- `basic_bind_file`: Standard bind file with WASD movement
- `attack_bind_template`: Template for attack rotations
- `simple_rotating_bind`: Basic rotating bind system

**Example Test Fixtures**:
- `character_power_sets`: Realistic power combinations by archetype
- `team_communication_messages`: Standard team communication
- `sample_bind_files`: Function to create example bind files

**Performance Test Fixtures**:
- `large_power_pool`: 100-power pool for stress testing
- `many_binds`: 50 complex binds for performance testing

**Utility Fixtures**:
- `in_tmp_dir`: Changes to temporary directory for test duration
- `capture_file_operations`: Monitors file I/O operations

## Test Markers

Tests are marked with pytest markers for selective execution:

- `@pytest.mark.unit`: Pure unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.example`: Example/end-to-end tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.slow`: Tests that take significant time

**Running by Marker**:
```bash
pytest -m unit                    # Only unit tests
pytest -m "integration or example" # Integration and examples
pytest -m "not slow"              # Skip slow tests
pytest -m "performance and not slow" # Fast performance tests only
```

## Running Tests

### Complete Test Suite
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=CityOfBinds

# Show print output (useful for examples)
pytest -s
```

### Selective Test Execution
```bash
# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/examples/
pytest tests/performance/

# Run specific test file
pytest tests/unit/test_bind.py
pytest tests/examples/test_basic_character_setup.py

# Run specific test method
pytest tests/unit/test_bind.py::TestBindInitialization::test_init_trigger_only

# Run tests matching pattern
pytest -k "test_wasd"
pytest -k "rotation"
```

### Performance and Debugging
```bash
# Run with timing information
pytest --durations=10

# Run with detailed output
pytest -vv

# Stop on first failure
pytest -x

# Run in parallel (if pytest-xdist installed)
pytest -n auto
```

## Test Development Guidelines

### Writing Unit Tests

1. **Focus on Single Responsibility**: Test one component/method at a time
2. **Use Descriptive Names**: `test_should_reject_empty_trigger_string()`
3. **Follow AAA Pattern**: Arrange, Act, Assert
4. **Test Edge Cases**: Empty inputs, boundary values, invalid data
5. **Use Parametrization**: Test multiple inputs efficiently

```python
@pytest.mark.parametrize("invalid_trigger", ["", "   ", "INVALID+"])
def test_init_raises_error_for_invalid_triggers(self, BindClass, invalid_trigger):
    with pytest.raises((ValueError, TypeError)):
        BindClass(invalid_trigger)
```

### Writing Integration Tests

1. **Test Realistic Workflows**: Complete operations from start to finish
2. **Use Temporary Directories**: All file operations in `tmp_path`
3. **Verify Side Effects**: Check file creation, content correctness
4. **Test Component Interactions**: How classes work together
5. **Include Error Scenarios**: What happens when things go wrong

```python
def test_bind_file_write_creates_correct_content(self, tmp_path):
    bind_file = BindFile()
    bind_file.add_bind(Bind("W", ["forward"]))
    
    file_path = tmp_path / "test.txt"
    bind_file.write_to_file(file_path)
    
    assert file_path.exists()
    content = file_path.read_text()
    assert 'W "forward"' in content
```

### Writing Example Tests

1. **Document Through Code**: Use docstrings to explain scenarios
2. **Use Realistic Data**: Actual game powers, commands, scenarios
3. **Show Best Practices**: Demonstrate proper library usage
4. **Include Print Output**: Help users understand what's generated
5. **Test Complete Workflows**: From creation to file generation

```python
def test_complete_character_setup(self, tmp_path):
    """
    Example: Create a complete bind file for a character.
    
    This example demonstrates a full character setup combining
    movement, powers, communication, and utility binds.
    """
    # ... implementation with detailed comments
    print(f"Generated complete character setup with {bind_count} binds")
```

### Writing Performance Tests

1. **Set Realistic Thresholds**: Based on actual performance requirements
2. **Test Scale Scenarios**: How does performance change with size?
3. **Monitor Resource Usage**: Memory, file handles, etc.
4. **Use `@pytest.mark.slow`**: For tests that take significant time
5. **Provide Benchmarks**: Help identify performance regressions

```python
@pytest.mark.performance
def test_large_bind_file_creation(self, many_binds):
    start_time = time.time()
    # ... operation under test
    execution_time = time.time() - start_time
    
    assert execution_time < 1.0  # 1 second threshold
    print(f"Created {len(many_binds)} binds in {execution_time:.3f} seconds")
```

## Continuous Integration

### Test Configuration

The test suite is designed for CI/CD environments:

- **Fast Feedback**: Unit tests run first (< 30 seconds total)
- **Staged Execution**: Integration tests after unit tests pass
- **Optional Performance**: Performance tests can be optional/scheduled
- **Failure Isolation**: Tests are independent and don't affect each other

### Recommended CI Pipeline

```yaml
test_stages:
  - name: "Unit Tests"
    command: "pytest tests/unit/ -v"
    timeout: 60s
    
  - name: "Integration Tests" 
    command: "pytest tests/integration/ -v"
    timeout: 300s
    depends_on: "Unit Tests"
    
  - name: "Example Tests"
    command: "pytest tests/examples/ -v -s"
    timeout: 600s
    depends_on: "Integration Tests"
    
  - name: "Performance Tests"
    command: "pytest tests/performance/ -m 'performance and not slow'"
    timeout: 300s
    optional: true
```

## Coverage and Quality

### Coverage Goals

- **Unit Tests**: > 95% line coverage for core components
- **Integration Tests**: > 90% branch coverage for workflows  
- **Example Tests**: Ensure all major features are exercised
- **Performance Tests**: Cover performance-critical paths

### Quality Metrics

- **Test Speed**: Unit tests average < 100ms each
- **Reliability**: < 1% flaky test rate
- **Maintainability**: Tests should be easy to understand and modify
- **Documentation**: Every example test should teach library usage

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `CityOfBinds` is in Python path
2. **File Permission Errors**: Tests should use `tmp_path` fixture
3. **Timing Issues**: Use appropriate timeouts for performance tests
4. **Fixture Scope**: Understand when fixtures are created/destroyed

### Debugging Tips

1. **Use `-s` Flag**: See print output from tests
2. **Use `-vv`**: Extra verbose output for debugging
3. **Use `--pdb`**: Drop into debugger on failure
4. **Check Fixtures**: Ensure fixtures provide expected data
5. **Isolate Tests**: Run single test to isolate issues

### Performance Debugging

```bash
# Profile test execution
pytest --profile

# Show slowest tests
pytest --durations=0

# Memory profiling (if memory_profiler installed)
pytest --memprof
```

## Future Enhancements

### Planned Additions

1. **Property-Based Testing**: Use `hypothesis` for edge case generation
2. **Mutation Testing**: Ensure tests catch actual bugs
3. **Visual Regression**: Test generated file formats
4. **Load Testing**: Simulate high-volume usage scenarios
5. **Documentation Tests**: Ensure examples in docs work

### Test Infrastructure

1. **Parallel Execution**: Speed up test runs with `pytest-xdist`
2. **Test Reporting**: Generate detailed HTML reports
3. **Coverage Tracking**: Monitor coverage trends over time
4. **Automated Benchmarking**: Track performance regressions

This comprehensive test suite ensures the City of Binds library is reliable, performant, and well-documented for users creating City of Heroes keybind systems.