#!/usr/bin/env python3
"""
Test suite for panorama collector using pytest.
"""

import pytest
import shutil
from pathlib import Path
from collect import PanoramaCollector


@pytest.fixture
def collector():
    """Create a collector instance for testing."""
    return PanoramaCollector("config/repos.yaml", "test_output")


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test output directory after each test."""
    yield
    test_output_dir = Path("test_output")
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)


class TestPanoramaCollector:
    """Test cases for PanoramaCollector."""

    def test_load_repos_yaml(self, collector):
        """Test loading repos.yaml configuration."""
        repos_data = collector.repos_data
        assert "repos" in repos_data, "repos.yaml should contain 'repos' key"

        repos = repos_data["repos"]
        assert len(repos) > 0, "Should have at least one repository defined"

    def test_path_expansion(self, collector):
        """Test path expansion functionality."""
        test_path = "~/dev/jazzydog-labs/foundry/foundry-bootstrap"
        expanded = collector._expand_path(test_path)
        assert expanded.exists(), f"Expanded path should exist: {expanded}"

    def test_file_reading(self, collector):
        """Test file reading functionality."""
        test_path = "~/dev/jazzydog-labs/foundry/foundry-bootstrap"
        expanded = collector._expand_path(test_path)
        readme_path = expanded / "README.md"

        content = collector._read_file_content(readme_path)
        assert content is not None, "Should be able to read README.md"
        assert len(content) > 0, "README.md should not be empty"

    def test_file_reading_nonexistent(self, collector):
        """Test file reading with nonexistent file."""
        nonexistent_path = Path("/nonexistent/file.md")
        content = collector._read_file_content(nonexistent_path)
        assert content is None, "Should return None for nonexistent file"

    def test_file_reading_empty(self, collector, tmp_path):
        """Test file reading with empty file."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")

        content = collector._read_file_content(empty_file)
        assert content is None, "Should return None for empty file"

    def test_should_include_file(self, collector):
        """Test file inclusion logic."""
        # Documentation files should always be included
        doc_file = Path("README.md")
        assert collector._should_include_file(doc_file, "documentation")

        # Config files should be included
        config_file = Path("config.yaml")
        assert collector._should_include_file(config_file, "config")

        # Code files should be excluded
        code_file = Path("main.py")
        assert not collector._should_include_file(code_file, "code")

        # Test files should be excluded
        test_file = Path("test_main.py")
        assert not collector._should_include_file(test_file, "tests")

    def test_format_file_section(self, collector):
        """Test file section formatting."""
        file_path = Path("test.md")
        content = "# Test Content"
        category = "documentation"

        section = collector._format_file_section(file_path, content, category)
        assert "### test.md" in section
        assert "**Path:** `test.md`" in section
        assert "**Category:** documentation" in section
        assert "```markdown" in section
        assert "# Test Content" in section

    def test_get_folder_structure(self, collector, tmp_path):
        """Test folder structure generation."""
        # Create test directory structure
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "README.md").write_text("test")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("print('test')")
        (tmp_path / ".git").mkdir()  # Should be ignored

        structure = collector._get_folder_structure(tmp_path)
        assert "📁 docs/" in structure
        assert "📁 src/" in structure
        assert "📄 README.md" in structure
        assert "📄 main.py" in structure
        assert ".git" not in structure

    def test_collect_repo_files(self, collector):
        """Test repository file collection."""
        repos = collector.repos_data["repos"]
        first_repo = repos[0]

        repo_section = collector._collect_repo_files(first_repo)
        assert len(repo_section) > 0, "Repository section should not be empty"
        assert first_repo["name"] in repo_section, "Repository name should be in section"
        assert "Repository Structure" in repo_section

    def test_collect_all(self, collector):
        """Test full collection process."""
        content = collector.collect_all()
        assert len(content) > 0, "Collection should generate content"
        assert "Foundry Ecosystem - Panorama Context" in content
        assert "End of Panorama Context" in content

    def test_write_output_markdown(self, collector, tmp_path):
        """Test writing markdown output."""
        collector.output_dir = tmp_path
        test_content = "# Test Content"

        collector.write_output(test_content, "md")

        output_file = tmp_path / "context.md"
        assert output_file.exists()
        assert output_file.read_text() == test_content

    def test_write_output_json(self, collector, tmp_path):
        """Test writing JSON output."""
        collector.output_dir = tmp_path
        test_content = "# Test Content"

        collector.write_output(test_content, "json")

        output_file = tmp_path / "context.json"
        assert output_file.exists()

    def test_write_output_invalid_format(self, collector):
        """Test writing output with invalid format."""
        with pytest.raises(ValueError, match="Unsupported output format"):
            collector.write_output("test", "invalid")

    def test_collector_initialization(self):
        """Test collector initialization with custom paths."""
        custom_collector = PanoramaCollector("config/repos.yaml", "custom_output")
        assert custom_collector.output_dir == Path("custom_output")

        # Clean up
        if Path("custom_output").exists():
            shutil.rmtree("custom_output")

    def test_invalid_repos_yaml(self, tmp_path):
        """Test handling of invalid repos.yaml file."""
        invalid_yaml = tmp_path / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")

        with pytest.raises(SystemExit):
            PanoramaCollector(str(invalid_yaml))

    def test_missing_repos_yaml(self, tmp_path):
        """Test handling of missing repos.yaml file."""
        missing_yaml = tmp_path / "missing.yaml"

        with pytest.raises(SystemExit):
            PanoramaCollector(str(missing_yaml))


class TestMainFunction:
    """Test cases for the main function."""

    def test_main_function_basic(self, monkeypatch, tmp_path):
        """Test main function with basic arguments."""
        # Mock sys.argv
        test_args = ["collect.py", "--repos-yaml", "config/repos.yaml", "--output-dir", str(tmp_path)]
        monkeypatch.setattr("sys.argv", test_args)

        # Import and run main
        from collect import main

        # This should run without error
        main()

        # Check that output was created
        assert (tmp_path / "context.md").exists()

    def test_main_function_verbose(self, monkeypatch, tmp_path):
        """Test main function with verbose flag."""
        test_args = ["collect.py", "--repos-yaml", "config/repos.yaml", "--output-dir", str(tmp_path), "--verbose"]
        monkeypatch.setattr("sys.argv", test_args)

        from collect import main

        main()

        assert (tmp_path / "context.md").exists()

    def test_main_function_json_format(self, monkeypatch, tmp_path):
        """Test main function with JSON output format."""
        test_args = [
            "collect.py",
            "--repos-yaml",
            "config/repos.yaml",
            "--output-dir",
            str(tmp_path),
            "--format",
            "json",
        ]
        monkeypatch.setattr("sys.argv", test_args)

        from collect import main

        main()

        assert (tmp_path / "context.json").exists()
