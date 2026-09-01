"""Tests for CLI."""

from typer.testing import CliRunner

from agi_runtime.cli.app import app

runner = CliRunner()


def test_cli_status():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "AGI Cognitive Runtime" in result.output


def test_cli_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "initialized" in result.output


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AGI Cognitive Runtime" in result.output


def test_cli_classify():
    result = runner.invoke(app, ["classify", "Fix the bug"])
    assert result.exit_code == 0
    assert "Task:" in result.output


def test_cli_inspect_invalid():
    result = runner.invoke(app, ["inspect", "invalid_target"])
    assert result.exit_code == 1


def test_cli_inspect_valid():
    result = runner.invoke(app, ["inspect", "status"])
    assert result.exit_code == 0
