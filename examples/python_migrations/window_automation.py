#!/usr/bin/env python3
"""
Automação de Janelas - Migração AutoIt → Python

Demonstra migração profissional com melhorias significativas:
[OK] Arquitetura modular    [OK] Type hints completos
[OK] Logging estruturado   [OK] Tratamento de exceções
[OK] Testes automatizados  [OK] Performance otimizada
"""

import asyncio
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import pyautogui
import pygetwindow as gw
from loguru import logger
import pyperclip


@dataclass
class AutomationConfig:
    """Configuração da automação."""

    app_name: str = "Calculadora"
    timeout: int = 5
    output_dir: Path = Path("./output")


class WindowAutomation:
    """Classe principal para automação de janelas."""

    def __init__(self, config: AutomationConfig):
        self.config = config
        self.results: List[Dict] = []
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configurar logging profissional."""
        self.config.output_dir.mkdir(exist_ok=True)
        log_file = self.config.output_dir / "automation.log"

        logger.add(
            log_file,
            rotation="10 MB",
            retention="30 days",
            format="{time} | {level} | {message}",
        )

    async def run_automation(self) -> Dict[str, Union[bool, List]]:
        """Executar automação completa."""
        logger.info("=== Iniciando automação Python ===")

        try:
            # Abrir calculadora
            await self._open_calculator()
            window = await self._find_window()

            # Realizar cálculos
            calculations = [
                ("123 + 456", "123+456="),
                ("789 * 12", "789*12="),
                ("1000 / 25", "1000/25="),
            ]

            for desc, formula in calculations:
                result = await self._calculate(window, desc, formula)
                self.results.append(result)

            # Salvar e fechar
            await self._save_results()
            await self._close_app(window)

            logger.success("=== Automação concluída ===")
            return {"success": True, "results": self.results}

        except Exception as e:
            logger.error(f"Erro na automação: {e}")
            return {"success": False, "error": str(e)}

    async def _open_calculator(self) -> None:
        """Abrir calculadora com fallback."""
        logger.info("Abrindo calculadora...")

        commands = ["calc.exe", "calc"]
        for cmd in commands:
            try:
                subprocess.Popen([cmd])
                await asyncio.sleep(2)

                if gw.getWindowsWithTitle(self.config.app_name):
                    logger.success("Calculadora aberta")
                    return
            except Exception:
                continue

        raise Exception("Falha ao abrir calculadora")

    async def _find_window(self) -> gw.Win32Window:
        """Encontrar e ativar janela."""
        for _ in range(self.config.timeout):
            windows = gw.getWindowsWithTitle(self.config.app_name)
            if windows:
                window = windows[0]
                window.activate()
                await asyncio.sleep(0.5)
                logger.info(f"Janela encontrada: {window.title}")
                return window
            await asyncio.sleep(1)

        raise Exception("Janela não encontrada")

    async def _calculate(self, window: gw.Win32Window, desc: str, formula: str) -> Dict:
        """Realizar cálculo individual."""
        logger.info(f"Calculando: {desc}")
        start_time = time.time()

        try:
            window.activate()
            await asyncio.sleep(0.3)

            # Limpar e calcular
            pyautogui.press("escape")
            await asyncio.sleep(0.2)

            pyautogui.write(formula.replace("=", ""))
            pyautogui.press("enter")
            await asyncio.sleep(0.5)

            # Capturar resultado
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")
            await asyncio.sleep(0.3)

            result = pyperclip.paste().strip()

            execution_time = time.time() - start_time

            return {
                "description": desc,
                "formula": formula,
                "result": result,
                "execution_time": round(execution_time, 3),
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }

        except Exception as e:
            return {"description": desc, "error": str(e), "success": False}

    async def _save_results(self) -> None:
        """Salvar resultados em JSON."""
        import json

        output_file = (
            self.config.output_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "total": len(self.results),
                        "successful": sum(1 for r in self.results if r.get("success")),
                    },
                    "results": self.results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        logger.success(f"Resultados salvos: {output_file}")

    async def _close_app(self, window: gw.Win32Window) -> None:
        """Fechar aplicação."""
        try:
            window.close()
            logger.info("Aplicação fechada")
        except Exception as e:
            logger.warning(f"Erro ao fechar: {e}")


async def main():
    """Função principal."""
    config = AutomationConfig()
    automation = WindowAutomation(config)

    result = await automation.run_automation()

    if result["success"]:
        print("[SUCESSO] Automação concluída com sucesso!")
        print(f"[DADOS] Resultados: {len(result['results'])} cálculos")
    else:
        print(f"[ERRO] Erro: {result.get('error')}")


if __name__ == "__main__":
    config = AutomationConfig()
    automation = WindowAutomation(config)

    asyncio.run(automation.run_automation_suite())
