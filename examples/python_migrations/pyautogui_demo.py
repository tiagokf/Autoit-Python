#!/usr/bin/env python3
"""
Automação Desktop com PyAutoGUI - Migração AutoIt → Python

[OK] Automação de interface gráfica
[OK] Controle de mouse e teclado
[OK] Screenshots e detecção
[OK] Segurança com failsafe
"""

import pyautogui
import time
import json
from datetime import datetime
from pathlib import Path


class DesktopAutomation:
    """Automação desktop com PyAutoGUI."""

    def __init__(self):
        # Configurações de segurança
        pyautogui.FAILSAFE = True  # Mouse no canto = parar
        pyautogui.PAUSE = 0.3  # Pausa entre comandos

        self.screen_size = pyautogui.size()
        self.results = []

        print(f" Tela: {self.screen_size}")

    def test_mouse_control(self):
        """Testar controle do mouse."""
        print(" Testando controle do mouse...")

        try:
            # Posição inicial
            start_pos = pyautogui.position()

            # Movimento em círculo pequeno
            center_x, center_y = self.screen_size[0] // 2, self.screen_size[1] // 2

            # Mover para centro
            pyautogui.moveTo(center_x, center_y, duration=0.5)

            # Movimento circular
            for angle in [0, 90, 180, 270]:
                x = center_x + 50 * (1 if angle in [0, 90] else -1)
                y = center_y + 50 * (1 if angle in [90, 180] else -1)
                pyautogui.moveTo(x, y, duration=0.3)

            # Voltar ao centro
            pyautogui.moveTo(center_x, center_y, duration=0.3)

            return {
                "test": "mouse_control",
                "start_position": list(start_pos),
                "center_used": [center_x, center_y],
                "success": True,
            }

        except Exception as e:
            return {"test": "mouse_control", "error": str(e), "success": False}

    def test_keyboard_input(self):
        """Testar entrada de teclado."""
        print("⌨ Testando teclado...")

        try:
            # Texto de teste
            test_text = "Automação Python com PyAutoGUI"

            # Simular abertura do bloco de notas (Windows)
            pyautogui.hotkey("win", "r")  # Executar
            time.sleep(0.5)

            pyautogui.write("notepad")
            pyautogui.press("enter")
            time.sleep(2)  # Aguardar abrir

            # Escrever texto
            pyautogui.write(test_text, interval=0.05)
            time.sleep(0.5)

            # Selecionar tudo e copiar
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")

            # Nova linha e colar
            pyautogui.press("end")
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "v")

            return {
                "test": "keyboard_input",
                "text_length": len(test_text),
                "operations": ["open_notepad", "write", "select", "copy", "paste"],
                "success": True,
            }

        except Exception as e:
            return {"test": "keyboard_input", "error": str(e), "success": False}

    def test_screenshot(self):
        """Testar captura de tela."""
        print(" Testando screenshot...")

        try:
            # Capturar tela
            screenshot = pyautogui.screenshot()

            # Salvar
            Path("output").mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"output/screenshot_{timestamp}.png"
            screenshot.save(filename)

            # Informações da imagem
            return {
                "test": "screenshot",
                "filename": filename,
                "size": screenshot.size,
                "mode": screenshot.mode,
                "success": True,
            }

        except Exception as e:
            return {"test": "screenshot", "error": str(e), "success": False}

    def cleanup_notepad(self):
        """Fechar bloco de notas sem salvar."""
        try:
            # Alt+F4 para fechar
            pyautogui.hotkey("alt", "f4")
            time.sleep(0.5)

            # Pressionar 'N' para não salvar (se aparecer diálogo)
            pyautogui.press("n")

        except Exception:
            pass  # Ignorar erros na limpeza

    def run_tests(self):
        """Executar todos os testes."""
        print("[INICIO] Iniciando automação desktop...")
        print("[AVISO] Mova mouse para canto superior esquerdo para parar")

        # Aguardar preparação
        for i in range(3, 0, -1):
            print(f"⏳ Iniciando em {i}...")
            time.sleep(1)

        try:
            # Teste 1: Mouse
            result1 = self.test_mouse_control()
            self.results.append(result1)

            # Teste 2: Teclado
            result2 = self.test_keyboard_input()
            self.results.append(result2)

            # Teste 3: Screenshot
            result3 = self.test_screenshot()
            self.results.append(result3)

            # Limpeza
            self.cleanup_notepad()

            # Salvar resultados
            self.save_results()

            successful = sum(1 for r in self.results if r.get("success"))

            print(f"[OK] Automação concluída!")
            print(f"[DADOS] Sucessos: {successful}/{len(self.results)}")

            return {
                "success": True,
                "tests_run": len(self.results),
                "tests_passed": successful,
            }

        except pyautogui.FailSafeException:
            print(" Parado pelo usuário (mouse no canto)")
            return {"success": False, "error": "Interrompido pelo usuário"}

        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            return {"success": False, "error": str(e)}

    def save_results(self):
        """Salvar resultados."""
        Path("output").mkdir(exist_ok=True)
        filename = f"output/pyautogui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "screen_size": list(self.screen_size),
                    "results": self.results,
                    "summary": {
                        "total": len(self.results),
                        "successful": sum(1 for r in self.results if r.get("success")),
                    },
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f" Resultados salvos: {filename}")


def main():
    """Executar automação."""
    automation = DesktopAutomation()
    result = automation.run_tests()

    if result["success"]:
        print(f"\n[SUCESSO] {result['tests_passed']}/{result['tests_run']} testes passaram!")
    else:
        print(f"\n[AVISO] Falha: {result.get('error')}")

    print("PyAutoGUI Demo concluído!")

    screenshots = []  # Lista para armazenar screenshots
    return {
        "status": "concluído",
        "screenshots_capturados": len(screenshots),
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    main()
