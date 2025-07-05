#!/usr/bin/env python3
"""
Panorama - Documentation and Context Aggregator

Collects high-level documentation and folder structure from all defined repositories
in the foundry ecosystem and outputs a unified context document suitable
for AI agent ingestion or comprehensive developer reference.
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PanoramaCollector:
    """Main collector class for aggregating repository documentation and context."""
    
    def __init__(self, repos_yaml_path: str, output_dir: str = "output"):
        self.repos_yaml_path = Path(repos_yaml_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.repos_data = self._load_repos_yaml()
        
    def _load_repos_yaml(self) -> Dict[str, Any]:
        """Load and parse the repos.yaml configuration file."""
        try:
            with open(self.repos_yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"repos.yaml not found at {self.repos_yaml_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing repos.yaml: {e}")
            sys.exit(1)
    
    def _expand_path(self, path: str) -> Path:
        """Expand user path and resolve to absolute path."""
        return Path(os.path.expanduser(path)).resolve()
    
    def _read_file_content(self, file_path: Path) -> Optional[str]:
        """Read file content with error handling."""
        try:
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    logger.warning(f"Empty file: {file_path}")
                    return None
                return content
        except UnicodeDecodeError:
            logger.warning(f"Could not decode file (likely binary): {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def _get_folder_structure(self, repo_path: Path, max_depth: int = 3) -> str:
        """Get folder structure for a repository."""
        structure = []
        
        def add_to_structure(path: Path, depth: int, prefix: str):
            if depth > max_depth:
                return
            
            # Skip hidden directories and common build artifacts
            if path.name.startswith('.') or path.name in ['__pycache__', 'node_modules', '.git', 'build', 'dist']:
                return
            
            if path.is_dir():
                structure.append(f"{prefix}📁 {path.name}/")
                try:
                    for item in sorted(path.iterdir()):
                        add_to_structure(item, depth + 1, prefix + "  ")
                except PermissionError:
                    structure.append(f"{prefix}  🔒 (permission denied)")
            elif path.is_file():
                # Only show important file types
                if path.suffix in ['.md', '.yaml', '.yml', '.json', '.txt', '.py', '.sh', '.zsh']:
                    structure.append(f"{prefix}📄 {path.name}")
        
        try:
            for item in sorted(repo_path.iterdir()):
                add_to_structure(item, 0, "")
        except PermissionError:
            structure.append("🔒 (permission denied)")
        
        return "\n".join(structure) if structure else "No accessible files"
    
    def _should_include_file(self, file_path: Path, category: str) -> bool:
        """Determine if a file should be included based on its type and category."""
        # Always include documentation files
        if category.startswith('documentation'):
            return True
        
        # Include configuration files
        if category == 'config':
            return file_path.suffix in ['.yaml', '.yml', '.json', '.txt']
        
        # Include schema files
        if category == 'data' and 'schema' in str(file_path):
            return True
        
        # Include examples (but not code)
        if category == 'examples':
            return file_path.suffix in ['.md', '.yaml', '.yml', '.json', '.txt']
        
        # Skip code files, tests, and other implementation details
        if category in ['code', 'tests']:
            return False
        
        # For other categories, be conservative
        return file_path.suffix in ['.md', '.yaml', '.yml', '.json', '.txt']
    
    def _format_file_section(self, file_path: Path, content: str, category: str) -> str:
        """Format a file section with header and content."""
        relative_path = file_path.name
        extension = file_path.suffix.lower()
        
        # Determine language for syntax highlighting
        lang_map = {
            '.md': 'markdown',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.txt': 'text'
        }
        lang = lang_map.get(extension, 'text')
        
        section = f"\n### {relative_path}\n\n"
        section += f"**Path:** `{file_path}`\n"
        section += f"**Category:** {category}\n\n"
        section += f"```{lang}\n{content}\n```\n"
        
        return section
    
    def _collect_repo_files(self, repo_config: Dict[str, Any]) -> str:
        """Collect high-level documentation and structure for a single repository."""
        repo_name = repo_config['name']
        repo_path = self._expand_path(repo_config['path'])
        description = repo_config.get('description', 'No description provided')
        
        logger.info(f"Processing repository: {repo_name}")
        
        # Start repository section
        section = f"\n{'='*80}\n"
        section += f"# {repo_name}\n"
        section += f"{'='*80}\n\n"
        section += f"**Description:** {description}\n\n"
        
        # Add repository metadata
        if 'remotes' in repo_config:
            section += "**Remotes:**\n"
            for remote_name, remote_url in repo_config['remotes'].items():
                section += f"- {remote_name}: {remote_url}\n"
            section += "\n"
        
        if 'type' in repo_config:
            section += f"**Type:** {repo_config['type']}\n\n"
        
        if 'integration_quality' in repo_config:
            iq = repo_config['integration_quality']
            section += "**Integration Quality:**\n"
            for key, value in iq.items():
                if key != 'notes':
                    section += f"- {key.replace('_', ' ').title()}: {value}\n"
            if 'notes' in iq:
                section += f"- Notes: {iq['notes']}\n"
            section += "\n"
        
        # Add folder structure
        section += "## Repository Structure\n\n"
        section += "```\n"
        section += self._get_folder_structure(repo_path)
        section += "\n```\n\n"
        
        # Collect documentation files only
        if 'documentation' in repo_config:
            section += "## Documentation\n\n"
            for doc_category, doc_files in repo_config['documentation'].items():
                if isinstance(doc_files, list):
                    for doc_file in doc_files:
                        file_path = repo_path / doc_file
                        content = self._read_file_content(file_path)
                        if content:
                            section += self._format_file_section(file_path, content, f"documentation/{doc_category}")
                else:
                    # Single file
                    file_path = repo_path / doc_files
                    content = self._read_file_content(file_path)
                    if content:
                        section += self._format_file_section(file_path, content, f"documentation/{doc_category}")
        
        # Collect only high-level context files
        if 'context_files' in repo_config:
            section += "## Key Configuration Files\n\n"
            for context_category, context_files in repo_config['context_files'].items():
                # Skip code and test categories
                if context_category in ['code', 'tests']:
                    continue
                
                section += f"### {context_category.title()}\n\n"
                for context_file in context_files:
                    file_path = repo_path / context_file
                    
                    # Check if we should include this file
                    if not self._should_include_file(file_path, context_category):
                        continue
                    
                    content = self._read_file_content(file_path)
                    if content:
                        section += self._format_file_section(file_path, content, context_category)
        
        return section
    
    def collect_all(self) -> str:
        """Collect high-level documentation and structure from all repositories."""
        logger.info("Starting panorama collection...")
        
        # Header
        content = "# Foundry Ecosystem - Panorama Context\n\n"
        content += "This document aggregates high-level documentation and repository structure "
        content += "from all repositories in the foundry ecosystem. It serves as a concise reference "
        content += "for AI agents, onboarding tools, and internal dashboards.\n\n"
        content += f"Generated on: {Path().cwd()}\n"
        content += f"Source: {self.repos_yaml_path}\n\n"
        content += f"Total repositories: {len(self.repos_data.get('repos', []))}\n\n"
        content += "**Note:** This context focuses on documentation and structure only. "
        content += "Code implementation details are excluded for conciseness.\n\n"
        
        # Process each repository
        repos = self.repos_data.get('repos', [])
        for repo_config in repos:
            try:
                repo_section = self._collect_repo_files(repo_config)
                content += repo_section
            except Exception as e:
                logger.error(f"Error processing repository {repo_config.get('name', 'unknown')}: {e}")
                content += f"\n## Error Processing Repository\n\n"
                content += f"Repository: {repo_config.get('name', 'unknown')}\n"
                content += f"Error: {e}\n\n"
        
        # Footer
        content += f"\n{'='*80}\n"
        content += "# End of Panorama Context\n"
        content += f"{'='*80}\n"
        
        return content
    
    def write_output(self, content: str, output_format: str = "md") -> None:
        """Write the collected content to output file."""
        if output_format == "md":
            output_file = self.output_dir / "context.md"
        elif output_format == "json":
            output_file = self.output_dir / "context.json"
            # For JSON output, we'd need to structure the content differently
            # For now, just write the markdown content
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Output written to: {output_file}")
        except Exception as e:
            logger.error(f"Error writing output file: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Panorama - Documentation and Context Aggregator")
    parser.add_argument(
        "--repos-yaml", 
        default="config/repos.yaml",
        help="Path to repos.yaml configuration file"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for generated files"
    )
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Output format (markdown or JSON)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create collector and run
    collector = PanoramaCollector(args.repos_yaml, args.output_dir)
    content = collector.collect_all()
    collector.write_output(content, args.format)
    
    logger.info("Panorama collection completed successfully!")


if __name__ == "__main__":
    main() 