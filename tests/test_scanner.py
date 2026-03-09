"""
test_scanner.py
---------------
Unit tests for the Python Port Scanner.

Run with: pytest tests/ -v
"""

import pytest
from unittest.mock import patch, MagicMock
import socket

from scanner.port_scanner import parse_port_range, scan_port, PortResult, TOP_PORTS
from scanner.host_discovery import resolve_host
from scanner.report_generator import colorize, Color


# ──────────────────────────────────────────────
# parse_port_range tests
# ──────────────────────────────────────────────

class TestParsePortRange:
    def test_single_port(self):
        assert parse_port_range("80") == [80]

    def test_port_range(self):
        result = parse_port_range("1-5")
        assert result == [1, 2, 3, 4, 5]

    def test_comma_separated(self):
        result = parse_port_range("22,80,443")
        assert result == [22, 80, 443]

    def test_mixed(self):
        result = parse_port_range("22,80-82,443")
        assert result == [22, 80, 81, 82, 443]

    def test_top_ports(self):
        result = parse_port_range("top")
        assert result == TOP_PORTS
        assert 80 in result
        assert 443 in result

    def test_top_ports_case_insensitive(self):
        assert parse_port_range("TOP") == TOP_PORTS

    def test_deduplication(self):
        result = parse_port_range("80,80,80")
        assert result == [80]


# ──────────────────────────────────────────────
# scan_port tests (mocked socket)
# ──────────────────────────────────────────────

class TestScanPort:
    @patch("scanner.port_scanner.socket.socket")
    def test_open_port(self, mock_socket_class):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0  # 0 = success
        mock_socket_class.return_value.__enter__.return_value = mock_sock

        result = scan_port("127.0.0.1", 80)

        assert isinstance(result, PortResult)
        assert result.state == "open"
        assert result.port == 80

    @patch("scanner.port_scanner.socket.socket")
    def test_closed_port(self, mock_socket_class):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 111  # ECONNREFUSED
        mock_socket_class.return_value.__enter__.return_value = mock_sock

        result = scan_port("127.0.0.1", 9999)

        assert result.state == "closed"

    @patch("scanner.port_scanner.socket.socket")
    def test_known_service_label(self, mock_socket_class):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket_class.return_value.__enter__.return_value = mock_sock

        result = scan_port("127.0.0.1", 22)
        assert result.service == "SSH"

    @patch("scanner.port_scanner.socket.socket")
    def test_unknown_service_label(self, mock_socket_class):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket_class.return_value.__enter__.return_value = mock_sock

        result = scan_port("127.0.0.1", 12345)
        assert result.service == "unknown"


# ──────────────────────────────────────────────
# resolve_host tests
# ──────────────────────────────────────────────

class TestResolveHost:
    @patch("scanner.host_discovery.socket.gethostbyname")
    def test_valid_ip(self, mock_resolve):
        mock_resolve.return_value = "93.184.216.34"
        result = resolve_host("example.com")
        assert result == "93.184.216.34"

    @patch("scanner.host_discovery.socket.gethostbyname")
    def test_invalid_host_raises(self, mock_resolve):
        mock_resolve.side_effect = socket.gaierror
        with pytest.raises(ValueError, match="Could not resolve host"):
            resolve_host("notarealhost.xyz")


# ──────────────────────────────────────────────
# report_generator tests
# ──────────────────────────────────────────────

class TestColorize:
    def test_returns_string(self):
        result = colorize("test", Color.GREEN)
        assert isinstance(result, str)
        assert "test" in result
