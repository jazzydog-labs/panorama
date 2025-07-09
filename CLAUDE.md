# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Workflow
```bash
# Run all tests (should maintain >80% coverage)
just test

# Run CI pipeline (tests + formatting + linting + typechecking + security scans)
just ci

# Run demo scripts for new features
just demo
```

### Running the Main Script
```bash
# Generate context from default repos.yaml location
python collect.py

# Specify custom repos.yaml location
python collect.py --repos-yaml path/to/repos.yaml

# Output to custom directory
python collect.py --output-dir /path/to/output

# Enable verbose logging
python collect.py --verbose

# Generate JSON format instead of markdown
python collect.py --format json
```

### Utility Scripts
```bash
# Update config from bill-of-materials repository
python update_config.py

# Run tests
python test_collect.py
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

## Commit Workflow

This repository uses a story-based commit tracking system:

1. **Pending work** is tracked in `commits/open/` directory with files named `000x_<commit_name>.md`
2. Each file contains a story describing the work to be done
3. To work on a commit:
   - Pick the lowest numbered open commit
   - Complete the work described in the story
   - Write tests to maintain >80% coverage with all tests passing
   - Create a demo script for new features (accessible via `just demo`)
   - Move the story file from `commits/open/` to `commits/closed/`
   - Commit with a descriptive message header and body

### Development Standards

- **Testing**: All new code must have tests with >80% coverage
- **CI Pipeline**: Run `just ci` before committing to ensure:
  - All tests pass
  - Code formatting is correct
  - Linting checks pass
  - Type checking passes
  - Security scans pass
- **Demos**: Every new feature should have a demo script
- **Note**: Demo scripts and tests are excluded from linting/checking requirements

## Architecture

### Overview
Panorama is a documentation and context aggregator for the Foundry ecosystem. It collects high-level documentation, configuration files, and repository structure from multiple repositories and aggregates them into a single output file suitable for AI agent ingestion.

### Core Components

1. **collect.py** - Main script containing the `PanoramaCollector` class that:
   - Loads repository configurations from `repos.yaml`
   - Traverses each repository to collect documentation and structure
   - Aggregates content into a unified output file
   - Supports both markdown and JSON output formats

2. **config/repos.yaml** - Declarative configuration file that defines:
   - Which repositories to process
   - Which files to include from each repository
   - Documentation categories and paths
   - Integration quality metrics

3. **update_config.py** - Utility script to update `repos.yaml` from the bill-of-materials repository

4. **test_collect.py** - Test suite for the collector functionality

### Key Design Principles

- **Documentation Focus**: Only collects high-level documentation and configuration files, excluding implementation code for conciseness
- **Declarative Configuration**: All repository and file selections are defined in `repos.yaml`
- **Error Resilience**: Gracefully handles missing files and encoding issues
- **Extensible Output**: Supports multiple output formats through the `--format` flag

### Integration with Foundry Ecosystem

The `repos.yaml` configuration is maintained in the `bill-of-materials` repository as the canonical source. Use `update_config.py` to sync the local configuration with the upstream source.

### Adding New Repositories

1. Update `repos.yaml` in the bill-of-materials repository
2. Run `python update_config.py` to sync the configuration
3. Run `python collect.py` to regenerate the context document

### Output Structure

The generated context file (`output/context.md` by default) includes:
- Header with generation metadata
- Repository sections containing:
  - Repository metadata (description, remotes, type)
  - Integration quality metrics
  - Repository structure (folder layout)
  - Documentation files organized by category
  - Key configuration files
- Footer marker

### Commit Workflow
When working on tasks from `commits/open/`:
1. Complete the implementation as described in the commit file
2. Update the commit file to mark all tasks as completed and add "Status: COMPLETED ✓"
3. Move the commit file from `commits/open/` to `commits/closed/` as part of your changes
4. Include this file move in your git commit along with the implementation


## Demos
- When adding any feature, please demo that feature in a `scripts/demos/*` script, and make sure that if you're creating a new demo script we are also adding it to `just demo`


## Demo Guidelines

When creating demos, ALWAYS start with a "killer feature" that is:
- **Concise**: Show the most impressive capability in 2-3 lines of code
- **Attention-grabbing**: Demonstrate immediate value
- **To the point**: No setup, just the wow factor
- **Practical**: Show why users should care

Example format:
```python
def demo_killer_feature():
    """The ONE thing that makes this feature amazing."""
    print("=== KILLER FEATURE: Transform any idea into 10 refined versions in seconds ===")
    idea = Idea.create("Basic concept", score=5.0)
    best_version = idea.auto_refine(iterations=10).get_best_version()
    print(f"Original score: 5.0 → Best score: {best_version.score} (+{best_version.score - 5.0} improvement!)")
```

Then proceed with the detailed demo sections.