#!/usr/bin/env python3
"""
Test suite for update_config.py using pytest.
"""

import pytest
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import update_config


class TestUpdateConfig:
    """Test cases for update_config module."""

    def test_update_config_function_exists(self):
        """Test that the update_config function exists."""
        assert hasattr(update_config, "update_config")
        assert callable(update_config.update_config)

    @patch("update_config.shutil.copy2")
    @patch("update_config.Path")
    def test_update_config_successful(self, mock_path, mock_copy):
        """Test update_config function with successful copy."""
        # Mock path objects
        mock_bom_path = MagicMock()
        mock_bom_path.exists.return_value = True
        mock_panorama_path = MagicMock()
        mock_stat = MagicMock()
        mock_stat.st_size = 1024
        mock_stat.st_mtime = 1234567890
        mock_panorama_path.stat.return_value = mock_stat

        mock_path.side_effect = [mock_bom_path, mock_panorama_path]

        # This should work without error
        update_config.update_config()

        # Verify copy was called
        mock_copy.assert_called_once_with(mock_bom_path, mock_panorama_path)

    @patch("update_config.Path")
    def test_update_config_file_not_found(self, mock_path):
        """Test update_config function when BOM file not found."""
        # Mock path objects
        mock_bom_path = MagicMock()
        mock_bom_path.exists.return_value = False
        mock_panorama_path = MagicMock()

        mock_path.side_effect = [mock_bom_path, mock_panorama_path]

        # Should handle the error gracefully
        with pytest.raises(SystemExit):
            update_config.update_config()

    @patch("update_config.shutil.copy2")
    @patch("update_config.Path")
    def test_update_config_copy_error(self, mock_path, mock_copy):
        """Test update_config function with copy error."""
        # Mock path objects
        mock_bom_path = MagicMock()
        mock_bom_path.exists.return_value = True
        mock_panorama_path = MagicMock()

        mock_path.side_effect = [mock_bom_path, mock_panorama_path]
        mock_copy.side_effect = Exception("Copy error")

        # Should handle the error gracefully
        with pytest.raises(SystemExit):
            update_config.update_config()
