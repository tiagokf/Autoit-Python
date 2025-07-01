#!/usr/bin/env python3
"""
Testes para WindowAutomation - Demonstração de competências em testing

[OK] Testes unitários e integração
[OK] Mocks e fixtures
[OK] Cobertura de código
[OK] Parametrização
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Adicionar path para import
project_root = Path(__file__).parent.parent
examples_path = project_root / "examples" / "python_migrations"
sys.path.insert(0, str(examples_path))

try:
    from window_automation import WindowAutomation, AutomationConfig
except ImportError as e:
    pytest.skip(f"Módulo window_automation não encontrado: {e}", allow_module_level=True)


class TestAutomationConfig:
    """Testes para configuração."""

    def test_default_values(self):
        """Testar valores padrão."""
        config = AutomationConfig()
        assert config.app_name == "Calculadora"
        assert config.timeout == 5
        assert config.output_dir == Path("./output")

    def test_custom_values(self):
        """Testar valores customizados."""
        config = AutomationConfig(app_name="Test", timeout=10, output_dir=Path("/tmp"))
        assert config.app_name == "Test"
        assert config.timeout == 10
        assert config.output_dir == Path("/tmp")


class TestWindowAutomation:
    """Testes principais."""

    @pytest.fixture
    def config(self, tmp_path):
        """Fixture de configuração."""
        return AutomationConfig(output_dir=tmp_path)

    @pytest.fixture
    def automation(self, config):
        """Fixture de automação."""
        with patch("window_automation.logger"):
            return WindowAutomation(config)

    def test_initialization(self, automation):
        """Testar inicialização."""
        assert automation.results == []
        assert automation.config.output_dir.exists()

    @pytest.mark.asyncio
    @patch("window_automation.subprocess.Popen")
    @patch("window_automation.gw.getWindowsWithTitle")
    async def test_open_calculator_success(self, mock_windows, mock_popen, automation):
        """Testar abertura da calculadora."""
        mock_windows.return_value = [MagicMock()]

        await automation._open_calculator()

        mock_popen.assert_called()
        mock_windows.assert_called()

    @pytest.mark.asyncio
    @patch("window_automation.subprocess.Popen")
    @patch("window_automation.gw.getWindowsWithTitle")
    async def test_open_calculator_failure(self, mock_windows, mock_popen, automation):
        """Testar falha na abertura."""
        mock_windows.return_value = []

        with pytest.raises(Exception):
            await automation._open_calculator()

    @pytest.mark.asyncio
    @patch("window_automation.gw.getWindowsWithTitle")
    async def test_find_window(self, mock_windows, automation):
        """Testar busca por janela."""
        mock_window = MagicMock()
        mock_windows.return_value = [mock_window]

        result = await automation._find_window()

        assert result == mock_window
        mock_window.activate.assert_called()

    @pytest.mark.asyncio
    @patch("window_automation.pyautogui")
    @patch("pyperclip.paste")
    async def test_calculate(self, mock_paste, mock_gui, automation):
        """Testar cálculo."""
        mock_paste.return_value = "42"
        mock_window = MagicMock()

        result = await automation._calculate(mock_window, "Test", "1+1=")

        assert result["success"] is True
        assert result["result"] == "42"
        assert "execution_time" in result

    @pytest.mark.asyncio
    async def test_save_results(self, automation):
        """Testar salvamento."""
        automation.results = [{"test": "data"}]

        await automation._save_results()

        # Verificar se arquivo foi criado
        json_files = list(automation.config.output_dir.glob("*.json"))
        assert len(json_files) >= 1

    @pytest.mark.parametrize(
        "success_count,total_count",
        [
            (3, 3),  # Todos sucessos
            (2, 3),  # Algumas falhas
            (0, 3),  # Todas falhas
        ],
    )
    @pytest.mark.asyncio
    async def test_multiple_results(self, success_count, total_count, automation):
        """Testar múltiplos resultados."""
        automation.results = [{"success": i < success_count} for i in range(total_count)]

        await automation._save_results()

        assert len(automation.results) == total_count

    @pytest.mark.asyncio
    async def test_full_flow_success(self, automation):
        """Teste de integração completo."""
        with (
            patch.object(automation, "_open_calculator") as mock_open,
            patch.object(automation, "_find_window", return_value=MagicMock()),
            patch.object(automation, "_calculate", return_value={"success": True}),
            patch.object(automation, "_save_results"),
            patch.object(automation, "_close_app"),
        ):
            result = await automation.run_automation()

            assert result["success"] is True
            mock_open.assert_called_once()

    @pytest.mark.asyncio
    async def test_full_flow_error(self, automation):
        """Teste de tratamento de erro."""
        with patch.object(automation, "_open_calculator", side_effect=Exception("Test error")):
            result = await automation.run_automation()

            assert result["success"] is False
            assert "error" in result


# Testes de integração
@pytest.mark.integration
class TestIntegration:
    """Testes de integração."""

    @pytest.mark.asyncio
    async def test_config_integration(self, tmp_path):
        """Testar integração com configuração."""
        config = AutomationConfig(output_dir=tmp_path)

        with patch("window_automation.logger"):
            automation = WindowAutomation(config)

        assert automation.config.output_dir == tmp_path
        assert tmp_path.exists()


# Configuração do pytest
def pytest_configure(config):
    """Configurar markers do pytest."""
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "slow: marca testes lentos")


if __name__ == "__main__":
    # Executar testes com cobertura
    pytest.main([__file__, "-v", "--tb=short"])
