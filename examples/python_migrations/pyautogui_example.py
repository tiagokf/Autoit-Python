#!/usr/bin/env python3
"""
Automação de Interface Gráfica com PyAutoGUI
Migração de AutoIt → Python

Demonstra:
[OK] PyAutoGUI para automação desktop
[OK] Controle de mouse e teclado
[OK] Detecção de imagens na tela
[OK] Captura de screenshots
[OK] Automação multiplataforma
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import json
import os

import pyautogui


class DesktopAutomation:
    """Automação desktop com PyAutoGUI."""

    def __init__(self):
        """Inicializar automação desktop."""
        # Configurações de segurança
        pyautogui.FAILSAFE = True  # Mover mouse para canto = parar
        pyautogui.PAUSE = 0.5  # Pausa entre comandos

        # Configurar resolução da tela
        self.screen_width, self.screen_height = pyautogui.size()

        # Resultados dos testes
        self.results: List[Dict] = []

        print(f"  Resolução da tela: {self.screen_width}x{self.screen_height}")
        print(f"[PASTA] Diretório de trabalho: {os.getcwd()}")

    def safe_click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> bool:
        """
        Clique seguro com validação de coordenadas.

        Args:
            x, y: Coordenadas do clique
            button: Botão do mouse ('left', 'right', 'middle')
            clicks: Número de cliques

        Returns:
            True se o clique foi executado com sucesso
        """
        try:
            # Validar coordenadas
            if 0 <= x <= self.screen_width and 0 <= y <= self.screen_height:
                pyautogui.click(x, y, button=button, clicks=clicks)
                print(f"  Clique em ({x}, {y}) - {clicks}x {button}")
                return True
            else:
                print(f"[ERRO] Coordenadas inválidas: ({x}, {y})")
                return False

        except Exception as e:
            print(f"[ERRO] Erro no clique: {e}")
            return False

    def find_and_click_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """
        Localizar imagem na tela e clicar nela.

        Args:
            image_path: Caminho para imagem de referência
            confidence: Confiança da detecção (0.0 a 1.0)

        Returns:
            True se a imagem foi encontrada e clicada
        """
        try:
            if not os.path.exists(image_path):
                print(f"[ERRO] Imagem não encontrada: {image_path}")
                return False

            # Localizar imagem na tela
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)

            if location:
                # Calcular centro da imagem
                center = pyautogui.center(location)

                # Clicar no centro
                pyautogui.click(center)
                print(f"[OK] Imagem encontrada e clicada: {center}")
                return True
            else:
                print(f"[ERRO] Imagem não encontrada na tela: {image_path}")
                return False

        except Exception as e:
            print(f"[ERRO] Erro na detecção de imagem: {e}")
            return False

    def type_text_safely(self, text: str, interval: float = 0.05) -> bool:
        """
        Digitar texto com segurança.

        Args:
            text: Texto para digitar
            interval: Intervalo entre caracteres

        Returns:
            True se o texto foi digitado com sucesso
        """
        try:
            pyautogui.write(text, interval=interval)
            print(f"⌨  Texto digitado: '{text[:30]}{'...' if len(text) > 30 else ''}'")
            return True

        except Exception as e:
            print(f"[ERRO] Erro ao digitar: {e}")
            return False

    def perform_keyboard_shortcuts(self) -> Dict:
        """Testar atalhos de teclado comuns."""
        print("⌨  Testando atalhos de teclado...")
        start_time = time.time()

        shortcuts_tested = []

        try:
            # Aguardar um pouco
            time.sleep(1)

            # Ctrl+C (copiar)
            pyautogui.hotkey("ctrl", "c")
            shortcuts_tested.append("Ctrl+C")
            time.sleep(0.5)

            # Ctrl+V (colar)
            pyautogui.hotkey("ctrl", "v")
            shortcuts_tested.append("Ctrl+V")
            time.sleep(0.5)

            # Alt+Tab (alternar janelas)
            pyautogui.hotkey("alt", "tab")
            shortcuts_tested.append("Alt+Tab")
            time.sleep(0.5)

            # Windows key (menu iniciar)
            pyautogui.press("win")
            shortcuts_tested.append("Win")
            time.sleep(1)

            # Escape (fechar menu)
            pyautogui.press("escape")
            shortcuts_tested.append("Escape")

            execution_time = time.time() - start_time

            return {
                "test": "keyboard_shortcuts",
                "shortcuts_tested": shortcuts_tested,
                "count": len(shortcuts_tested),
                "execution_time": round(execution_time, 3),
                "success": True,
            }

        except Exception as e:
            return {
                "test": "keyboard_shortcuts",
                "shortcuts_tested": shortcuts_tested,
                "error": str(e),
                "success": False,
            }

    def mouse_movement_test(self) -> Dict:
        """Testar movimentos de mouse."""
        print("  Testando movimentos de mouse...")
        start_time = time.time()

        try:
            # Salvar posição inicial
            initial_pos = pyautogui.position()

            # Movimento em quadrado
            square_size = 100
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2

            positions = [
                (center_x - square_size, center_y - square_size),  # Top-left
                (center_x + square_size, center_y - square_size),  # Top-right
                (center_x + square_size, center_y + square_size),  # Bottom-right
                (center_x - square_size, center_y + square_size),  # Bottom-left
                (center_x - square_size, center_y - square_size),  # Back to start
            ]

            for i, (x, y) in enumerate(positions):
                pyautogui.moveTo(x, y, duration=0.5)
                time.sleep(0.2)
                print(f"  [POSICAO] Posição {i + 1}: ({x}, {y})")

            # Voltar para posição inicial
            pyautogui.moveTo(initial_pos.x, initial_pos.y, duration=0.5)

            execution_time = time.time() - start_time

            return {
                "test": "mouse_movement",
                "positions_visited": len(positions),
                "initial_position": [initial_pos.x, initial_pos.y],
                "execution_time": round(execution_time, 3),
                "success": True,
            }

        except Exception as e:
            return {"test": "mouse_movement", "error": str(e), "success": False}

    def screen_analysis(self) -> Dict:
        """Analisar informações da tela."""
        print("[DADOS] Analisando tela...")

        try:
            # Capturar screenshot
            screenshot = pyautogui.screenshot()

            # Salvar screenshot
            Path("output").mkdir(exist_ok=True)
            screenshot_path = f"output/screen_analysis_{datetime.now().strftime('%H%M%S')}.png"
            screenshot.save(screenshot_path)

            # Analisar cores dominantes (simplificado)
            colors = screenshot.getcolors(maxcolors=256 * 256 * 256)
            if colors:
                # Encontrar cor mais comum
                most_common_color = max(colors, key=lambda x: x[0])
                dominant_color = most_common_color[1]
            else:
                dominant_color = None

            # Informações do mouse
            mouse_pos = pyautogui.position()

            return {
                "test": "screen_analysis",
                "screen_size": [self.screen_width, self.screen_height],
                "screenshot_path": screenshot_path,
                "screenshot_size": screenshot.size,
                "dominant_color": dominant_color,
                "mouse_position": [mouse_pos.x, mouse_pos.y],
                "success": True,
            }

        except Exception as e:
            return {"test": "screen_analysis", "error": str(e), "success": False}

    def simulate_text_editing(self) -> Dict:
        """Simular edição de texto."""
        print("[NOTA] Simulando edição de texto...")
        start_time = time.time()

        try:
            # Texto de exemplo
            sample_text = "Este é um teste de automação com PyAutoGUI em Python!"

            # Simular digitação
            self.type_text_safely(sample_text, interval=0.02)
            time.sleep(0.5)

            # Selecionar tudo
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.3)

            # Copiar
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.3)

            # Colar (duplicar texto)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)

            execution_time = time.time() - start_time

            return {
                "test": "text_editing",
                "text_length": len(sample_text),
                "operations": ["type", "select_all", "copy", "paste"],
                "execution_time": round(execution_time, 3),
                "success": True,
            }

        except Exception as e:
            return {"test": "text_editing", "error": str(e), "success": False}

    def run_automation_suite(self) -> Dict:
        """Executar suite completa de automação desktop."""
        print("[INICIO] Iniciando suite de automação desktop...")
        print("[AVISO]  ATENÇÃO: Mova o mouse para o canto superior esquerdo para parar")

        # Aguardar 3 segundos para preparação
        print(" Iniciando em 3 segundos...")
        time.sleep(3)

        try:
            # Teste 1: Análise de tela
            result1 = self.screen_analysis()
            self.results.append(result1)

            # Teste 2: Movimentos de mouse
            result2 = self.mouse_movement_test()
            self.results.append(result2)

            # Teste 3: Atalhos de teclado
            result3 = self.perform_keyboard_shortcuts()
            self.results.append(result3)

            # Teste 4: Edição de texto
            result4 = self.simulate_text_editing()
            self.results.append(result4)

            # Salvar resultados
            self.save_results()

            # Calcular estatísticas
            successful_tests = sum(1 for r in self.results if r.get("success", False))

            print("[OK] Suite de automação desktop concluída!")
            print(f"[DADOS] Testes executados: {len(self.results)}")
            print(f"[OK] Sucessos: {successful_tests}")

            return {
                "success": True,
                "total_tests": len(self.results),
                "successful_tests": successful_tests,
                "results": self.results,
            }

        except pyautogui.FailSafeException:
            print(" Automação interrompida pelo usuário (mouse no canto)")
            return {
                "success": False,
                "error": "Interrompido pelo usuário",
                "results": self.results,
            }

        except Exception as e:
            print(f"[ERRO] Erro na suite: {e}")
            return {"success": False, "error": str(e), "results": self.results}

    def save_results(self) -> None:
        """Salvar resultados em arquivo JSON."""
        Path("output").mkdir(exist_ok=True)
        filename = f"output/pyautogui_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "screen_resolution": f"{self.screen_width}x{self.screen_height}",
                        "total_tests": len(self.results),
                        "successful_tests": sum(
                            1 for r in self.results if r.get("success", False)
                        ),
                    },
                    "results": self.results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f" Resultados salvos: {filename}")


def main():
    """Função principal."""
    print("[OBJETIVO] Automação Desktop com PyAutoGUI")
    print("=" * 50)

    automation = DesktopAutomation()
    result = automation.run_automation_suite()

    if result["success"]:
        print(f"\n[SUCESSO] Automação concluída com sucesso!")
        success_rate = f"{result['successful_tests']}/{result['total_tests']}"
        print(f"[CRESCIMENTO] Taxa de sucesso: {success_rate}")
    else:
        print(f"\n[AVISO]  Automação interrompida: {result.get('error', 'Erro desconhecido')}")

    print("PyAutoGUI Example concluído!")

    return {
        "status": "concluído",
        "testes_executados": len(automation.results),
        "capturas_feitas": len([r for r in automation.results if "screenshot" in r]),
    }


if __name__ == "__main__":
    main()
