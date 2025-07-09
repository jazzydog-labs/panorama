# Panorama

Documentation and Context Aggregator for the Foundry Ecosystem

## Purpose

Panorama aggregates high-level documentation and repository structure from all repositories in the foundry ecosystem — including READMEs, design documents, configuration files, and folder layouts — into a single output file suitable for AI agent ingestion or comprehensive developer reference. **Code implementation details are excluded for conciseness.**

### Key Features

- **Declarative Configuration**: Uses `repos.yaml` to define which files to include from each repository
- **Structured Output**: Organizes content by repository and category with clear headings
- **Repository Structure**: Includes folder layouts and file organization
- **Documentation Focus**: Includes only high-level documentation and configuration
- **Code Exclusion**: Excludes implementation code for conciseness
- **Error Handling**: Gracefully handles missing files and encoding issues
- **Multiple Output Formats**: Supports markdown and JSON output formats

## Structure

```
panorama/
├── collect.py                # Main script to generate the context output
├── config/
│   └── repos.yaml            # Declares repo metadata and documentation sources
├── output/
│   └── context.md            # Unified context document
├── README.md
```

## Usage

### Helper Scripts

```bash
# Update config from bill-of-materials
python update_config.py

# Run tests
python test_collect.py
```

### Basic Usage

```bash
# Generate context from default repos.yaml location
python collect.py

# Specify custom repos.yaml location
python collect.py --repos-yaml path/to/repos.yaml

# Output to custom directory
python collect.py --output-dir /path/to/output

# Enable verbose logging
python collect.py --verbose
```

### Command Line Options

- `--repos-yaml`: Path to repos.yaml configuration file (default: `config/repos.yaml`)
- `--output-dir`: Output directory for generated files (default: `output`)
- `--format`: Output format - `md` or `json` (default: `md`)
- `--verbose, -v`: Enable verbose logging

## Configuration

The `repos.yaml` file defines which repositories to process and which files to include. Each repository entry includes:

### Repository Metadata

```yaml
- name: repository-name
  path: ~/path/to/repository
  description: Repository description
  remotes:
    origin: https://github.com/org/repo.git
  type: repository-type
```

### Documentation Sources

```yaml
documentation:
  readme: README.md
  architecture:
    - docs/architecture.md
    - docs/design.md
  guides:
    - docs/getting-started.md
```

### Context Files

```yaml
context_files:
  config:
    - config/settings.yaml
    - config/defaults.json
  code:
    - src/main.py
    - scripts/setup.sh
  tests:
    - tests/test_main.py
```

### Integration Quality

```yaml
integration_quality:
  documentation_completeness: excellent
  bom_integration: complete
  context_file_coverage: comprehensive
  last_updated: "2025-01-27"
  notes: "Additional notes about integration quality"
```

## Output Format

The generated `context.md` file includes:

1. **Header**: Overview and generation metadata
2. **Repository Sections**: One section per repository with:
   - Repository metadata (description, remotes, type)
   - Integration quality metrics
   - Repository structure (folder layout)
   - Documentation files organized by category
   - Key configuration files (excluding code)
3. **Footer**: End marker

Each file is presented with:
- File path and category
- Syntax-highlighted content
- Preserved formatting

**Note**: Implementation code, test files, and other detailed source files are excluded to maintain conciseness.

## Integration with Foundry Ecosystem

### Bill of Materials Integration

Panorama integrates with the `bill-of-materials` repository as the canonical source of `repos.yaml`. The configuration file is copied from `bill-of-materials/repos.yaml` to maintain consistency across the ecosystem.

### Use Cases

1. **AI Agent Context**: Provides comprehensive context for LLM agents working with the foundry ecosystem
2. **Developer Onboarding**: Single reference document for new developers
3. **Documentation Audits**: Overview of documentation completeness across repositories
4. **Integration Analysis**: Assessment of repository integration quality

## Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
just install-hooks
```

### Development Commands

This project uses [just](https://github.com/casey/just) for task automation:

```bash
# Run tests with coverage (must maintain >80%)
just test

# Run full CI pipeline (tests + formatting + linting + typechecking + security)
just ci

# Run demo scripts
just demo

# Format code with black
just format

# Lint with ruff
just lint

# Type check with mypy
just typecheck

# Security scan with bandit
just security

# Clean generated files
just clean
```

### Tmux Session Management

Panorama includes a `pano` command for managing a tmux session that displays all foundry repositories simultaneously:

#### Installation

```bash
# Install the pano command
./scripts/install_pano.sh
```

#### Usage

```bash
# Open panorama view (creates session if needed)
pano

# Check session status
pano status

# Close the panorama session
pano close

# Refresh session with updated repo list
pano refresh

# Run a command in all repository panes
pano run "git status"
pano run "git pull"
pano run "pwd"

# Collapse prompts to simple '>' for cleaner view
pano prompt-collapse
```

#### Features

- **Multi-repo view**: Displays all 12 foundry repositories in a tiled tmux layout
- **Automatic session management**: Creates named session "panorama" for easy access
- **Graceful error handling**: Handles missing repositories and shows warnings
- **Repository awareness**: Each pane starts in the correct repository directory
- **Easy navigation**: Use standard tmux commands to navigate between panes
- **Bulk command execution**: Run commands across all repositories simultaneously with `pano run`
- **Auto-collapsed prompts**: Automatically simplifies prompts to `>` for cleaner multi-pane viewing
- **Pane titles**: Shows `<repo name>:<working directory>` at the top of each pane

#### Requirements

- tmux (install with `brew install tmux` on macOS)
- Python 3 with PyYAML

### Adding New Repositories

1. Add repository metadata to `bill-of-materials/repos.yaml`
2. Update panorama config: `python update_config.py`
3. Run `python collect.py` to regenerate context

### Extending File Categories

To add new file categories:

1. Update the `repos.yaml` schema in `bill-of-materials`
2. Add category to repository configurations
3. The collector will automatically handle new categories

### Custom Output Formats

The collector supports extensible output formats. To add a new format:

1. Implement format-specific logic in `write_output()`
2. Add format option to argument parser
3. Update documentation

## TODOs

- [ ] Add support for configurable summaries or truncation per section
- [ ] Integrate with `bill-of-materials` as a canonical source of `repos.yaml`
- [ ] Optionally generate per-agent context slices or token-aware outputs
- [ ] Add support for file filtering and exclusion patterns
- [ ] Implement incremental updates (only process changed files)
- [ ] Add support for external documentation sources (web URLs, etc.)

## Dependencies

- Python 3.7+
- PyYAML
- Standard library modules (os, sys, pathlib, logging, argparse)

## License

Part of the Foundry Ecosystem - see individual repository licenses for details. 