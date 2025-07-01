"""
Configuração global para testes - Compatibilidade entre ambientes.

Este arquivo configura automaticamente os testes para funcionarem tanto
no ambiente local (Windows/Linux com GUI) quanto no CI/CD (headless).
"""

import os
import sys
import pytest
from unittest.mock import MagicMock

# Mock preventivo para PyAutoGUI em ambiente headless
if os.getenv("CI") or os.getenv("GITHUB_ACTIONS") or not os.getenv("DISPLAY"):
    # Mock do mouseinfo que causa problemas no CI
    sys.modules["mouseinfo"] = MagicMock()

    # Mock do Xlib que causa problemas de autenticação
    sys.modules["Xlib"] = MagicMock()
    sys.modules["Xlib.display"] = MagicMock()
    sys.modules["Xlib.xauth"] = MagicMock()

    # Mock do pygetwindow que não funciona no Linux
    mock_pygetwindow = MagicMock()
    mock_window = MagicMock()
    mock_window.activate = MagicMock()
    mock_window.close = MagicMock()
    mock_pygetwindow.getWindowsWithTitle.return_value = [mock_window]
    sys.modules["pygetwindow"] = mock_pygetwindow

    # Mock do pyautogui antes da importação
    mock_pyautogui = MagicMock()
    mock_pyautogui.screenshot.return_value = MagicMock()
    mock_pyautogui.size.return_value = (1920, 1080)
    mock_pyautogui.position.return_value = MagicMock(x=100, y=100)
    sys.modules["pyautogui"] = mock_pyautogui

    # Mock de outros módulos problemáticos no Linux
    sys.modules["pyperclip"] = MagicMock()

    # Mock do loguru para evitar problemas de logging
    mock_logger = MagicMock()
    mock_logger.add = MagicMock()
    mock_logger.info = MagicMock()
    mock_logger.success = MagicMock()
    mock_logger.error = MagicMock()
    mock_logger.warning = MagicMock()
    sys.modules["loguru"] = MagicMock()
    sys.modules["loguru"].logger = mock_logger

    # Não fazemos mock do subprocess para evitar problemas com pytest-metadata


def is_ci_environment():
    """Detectar se estamos rodando no CI/CD."""
    return any(
        [
            os.getenv("CI"),
            os.getenv("GITHUB_ACTIONS"),
            os.getenv("TRAVIS"),
            os.getenv("JENKINS_URL"),
            os.getenv("HEADLESS") == "true",
        ]
    )


def is_gui_available():
    """Verificar se GUI está disponível."""
    if sys.platform == "win32":
        return True  # Windows sempre tem GUI disponível

    # Linux/macOS - verificar DISPLAY
    return bool(os.getenv("DISPLAY"))


# Configurar marcadores para diferentes tipos de teste
def pytest_configure(config):
    """Configurar marcadores customizados."""
    config.addinivalue_line("markers", "gui: marca testes que requerem interface gráfica")
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "slow: marca testes que demoram mais para executar")
    config.addinivalue_line("markers", "windows_only: marca testes específicos do Windows")


def pytest_collection_modifyitems(config, items):
    """Modificar coleta de testes baseado no ambiente."""

    # Pular testes GUI se não houver interface disponível
    if is_ci_environment() and not is_gui_available():
        skip_gui = pytest.mark.skip(reason="GUI não disponível no ambiente CI")
        for item in items:
            if "gui" in item.keywords:
                item.add_marker(skip_gui)

    # Pular testes específicos do Windows em outros sistemas
    if sys.platform != "win32":
        skip_windows = pytest.mark.skip(reason="Teste específico do Windows")
        for item in items:
            if "windows_only" in item.keywords:
                item.add_marker(skip_windows)
