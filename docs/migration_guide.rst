Guia de Migração AutoIt → Python
=================================

Este guia ajuda na migração de scripts AutoIt para Python moderno.

🎯 **Visão Geral da Migração**
------------------------------

A migração de AutoIt para Python oferece várias vantagens:

* ✅ **Melhor manutenibilidade** com orientação a objetos
* ✅ **Type safety** com type hints
* ✅ **Ecosystem rico** de bibliotecas Python
* ✅ **Testes automatizados** integrados
* ✅ **Performance** com async/await
* ✅ **Portabilidade** entre sistemas operacionais

📊 **Comparação de Sintaxe**
----------------------------

Automação de Janelas
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - AutoIt
     - Python
   * - .. code-block:: autoit

          WinActivate("Calculator")
          WinWaitActive("Calculator")
     - .. code-block:: python

          import pygetwindow as gw
          window = gw.getWindowsWithTitle("Calculator")[0]
          window.activate()
   * - .. code-block:: autoit

          Send("123+456=")
     - .. code-block:: python

          import pyautogui
          pyautogui.write("123+456")
          pyautogui.press("enter")

Controle de Mouse
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - AutoIt
     - Python
   * - .. code-block:: autoit

          MouseClick("left", 100, 200)
     - .. code-block:: python

          import pyautogui
          pyautogui.click(100, 200)
   * - .. code-block:: autoit

          MouseMove(300, 400)
     - .. code-block:: python

          import pyautogui
          pyautogui.moveTo(300, 400)

Controle de Teclado
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - AutoIt
     - Python
   * - .. code-block:: autoit

          Send("{CTRL down}c{CTRL up}")
     - .. code-block:: python

          import pyautogui
          pyautogui.hotkey('ctrl', 'c')
   * - .. code-block:: autoit

          Send("Hello World{ENTER}")
     - .. code-block:: python

          import pyautogui
          pyautogui.write("Hello World")
          pyautogui.press("enter")

🔄 **Processo de Migração Passo a Passo**
-----------------------------------------

Passo 1: Análise do Script AutoIt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Primeiro, analise seu script AutoIt existente:

.. code-block:: autoit

   ; Exemplo de script AutoIt original
   #include <ButtonConstants.au3>
   #include <GUIConstantsEx.au3>
   
   ; Abrir calculadora
   Run("calc.exe")
   WinWaitActive("Calculator")
   
   ; Realizar cálculo
   Send("123")
   Send("+")
   Send("456")
   Send("=")
   
   ; Capturar resultado
   Send("^a")
   Send("^c")
   $result = ClipGet()
   
   ; Salvar resultado
   FileWrite("resultado.txt", $result)
   
   ; Fechar calculadora
   WinClose("Calculator")

Passo 2: Estrutura Python Equivalente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crie a estrutura Python moderna:

.. code-block:: python

   #!/usr/bin/env python3
   """
   Migração do script AutoIt para Python.
   """
   
   import asyncio
   import subprocess
   import pyautogui
   import pygetwindow as gw
   import pyperclip
   from pathlib import Path
   from dataclasses import dataclass
   from typing import Optional
   
   @dataclass
   class CalculatorConfig:
       """Configuração da automação."""
       timeout: int = 5
       output_file: Path = Path("resultado.txt")
   
   class CalculatorAutomation:
       """Automação moderna da calculadora."""
       
       def __init__(self, config: CalculatorConfig):
           self.config = config
       
       async def run(self) -> Optional[str]:
           """Executar automação completa."""
           try:
               # Abrir calculadora
               await self._open_calculator()
               
               # Realizar cálculo
               result = await self._calculate("123+456")
               
               # Salvar resultado
               await self._save_result(result)
               
               # Fechar calculadora
               await self._close_calculator()
               
               return result
               
           except Exception as e:
               print(f"Erro na automação: {e}")
               return None
       
       async def _open_calculator(self):
           """Abrir calculadora."""
           subprocess.Popen(["calc.exe"])
           await asyncio.sleep(2)
           
           # Aguardar janela aparecer
           for _ in range(self.config.timeout):
               windows = gw.getWindowsWithTitle("Calculator")
               if windows:
                   windows[0].activate()
                   return
               await asyncio.sleep(1)
           
           raise Exception("Calculadora não encontrada")
       
       async def _calculate(self, formula: str) -> str:
           """Realizar cálculo."""
           # Enviar fórmula
           pyautogui.write(formula.replace("=", ""))
           pyautogui.press("enter")
           await asyncio.sleep(0.5)
           
           # Capturar resultado
           pyautogui.hotkey("ctrl", "a")
           pyautogui.hotkey("ctrl", "c")
           await asyncio.sleep(0.3)
           
           return pyperclip.paste().strip()
       
       async def _save_result(self, result: str):
           """Salvar resultado em arquivo."""
           with open(self.config.output_file, "w") as f:
               f.write(result)
       
       async def _close_calculator(self):
           """Fechar calculadora."""
           windows = gw.getWindowsWithTitle("Calculator")
           if windows:
               windows[0].close()
   
   # Uso
   async def main():
       config = CalculatorConfig()
       automation = CalculatorAutomation(config)
       result = await automation.run()
       print(f"Resultado: {result}")
   
   if __name__ == "__main__":
       asyncio.run(main())

Passo 3: Melhorias Adicionais
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adicione melhorias modernas:

.. code-block:: python

   import logging
   from loguru import logger
   
   # Configurar logging
   logger.add("automation.log", rotation="10 MB")
   
   class EnhancedCalculatorAutomation(CalculatorAutomation):
       """Versão melhorada com logging e tratamento de erros."""
       
       async def run(self) -> Optional[str]:
           """Executar com logging detalhado."""
           logger.info("Iniciando automação da calculadora")
           
           try:
               result = await super().run()
               logger.success(f"Automação concluída: {result}")
               return result
               
           except Exception as e:
               logger.error(f"Falha na automação: {e}")
               raise

🛠️ **Ferramentas de Migração**
------------------------------

Bibliotecas Python Equivalentes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Funcionalidade
     - AutoIt
     - Python
   * - **Automação GUI**
     - Built-in
     - PyAutoGUI
   * - **Janelas**
     - WinAPI
     - PyGetWindow
   * - **Clipboard**
     - ClipGet/ClipPut
     - Pyperclip
   * - **Arquivos**
     - FileRead/FileWrite
     - Pathlib
   * - **Processes**
     - Run/ProcessExists
     - Subprocess
   * - **Delays**
     - Sleep
     - Asyncio.sleep
   * - **Logging**
     - ConsoleWrite
     - Loguru

Mapeamento de Funções
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Mapeamento direto de funções AutoIt → Python
   
   # AutoIt: WinActivate("Title")
   # Python:
   import pygetwindow as gw
   gw.getWindowsWithTitle("Title")[0].activate()
   
   # AutoIt: Send("text")
   # Python:
   import pyautogui
   pyautogui.write("text")
   
   # AutoIt: MouseClick("left", x, y)
   # Python:
   pyautogui.click(x, y)
   
   # AutoIt: Sleep(1000)
   # Python:
   await asyncio.sleep(1)
   
   # AutoIt: FileWrite("file.txt", "content")
   # Python:
   Path("file.txt").write_text("content")

🧪 **Adicionando Testes**
-------------------------

Uma grande vantagem do Python é o suporte nativo para testes:

.. code-block:: python

   import pytest
   from unittest.mock import patch, MagicMock
   
   class TestCalculatorAutomation:
       """Testes para automação da calculadora."""
       
       @pytest.fixture
       def automation(self):
           """Fixture para automação."""
           config = CalculatorConfig()
           return CalculatorAutomation(config)
       
       @patch('pyautogui.write')
       @patch('pyautogui.press')
       @patch('pyperclip.paste')
       async def test_calculate(self, mock_paste, mock_press, mock_write, automation):
           """Testar cálculo."""
           mock_paste.return_value = "579"
           
           result = await automation._calculate("123+456")
           
           mock_write.assert_called_with("123+456")
           mock_press.assert_called_with("enter")
           assert result == "579"
       
       async def test_config_validation(self):
           """Testar validação de configuração."""
           config = CalculatorConfig(timeout=10)
           assert config.timeout == 10
           assert config.output_file == Path("resultado.txt")

🚀 **Melhorias Arquiteturais**
------------------------------

Padrões de Design
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from abc import ABC, abstractmethod
   from typing import Protocol
   
   class AutomationStrategy(Protocol):
       """Protocol para estratégias de automação."""
       
       async def execute(self, command: str) -> str:
           """Executar comando de automação."""
           ...
   
   class CalculatorStrategy:
       """Estratégia específica para calculadora."""
       
       async def execute(self, command: str) -> str:
           # Implementação específica
           pass
   
   class AutomationContext:
       """Context para diferentes estratégias."""
       
       def __init__(self, strategy: AutomationStrategy):
           self.strategy = strategy
       
       async def run_automation(self, command: str) -> str:
           return await self.strategy.execute(command)

Injeção de Dependências
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from typing import Protocol
   
   class WindowManager(Protocol):
       """Interface para gerenciamento de janelas."""
       
       def activate_window(self, title: str) -> bool:
           """Ativar janela por título."""
           ...
   
   class PyGetWindowManager:
       """Implementação com PyGetWindow."""
       
       def activate_window(self, title: str) -> bool:
           windows = gw.getWindowsWithTitle(title)
           if windows:
               windows[0].activate()
               return True
           return False
   
   class CalculatorAutomation:
       """Automação com dependências injetadas."""
       
       def __init__(self, window_manager: WindowManager):
           self.window_manager = window_manager

📈 **Performance e Otimização**
-------------------------------

Programação Assíncrona
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async def batch_calculations(formulas: list[str]) -> list[str]:
       """Executar múltiplos cálculos em paralelo."""
       
       tasks = []
       for formula in formulas:
           task = asyncio.create_task(calculate_async(formula))
           tasks.append(task)
       
       results = await asyncio.gather(*tasks, return_exceptions=True)
       return [r for r in results if isinstance(r, str)]

Caching e Memoização
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from functools import lru_cache
   
   class CachedCalculator:
       """Calculadora com cache de resultados."""
       
       @lru_cache(maxsize=128)
       def calculate_cached(self, formula: str) -> str:
           """Calcular com cache para fórmulas repetidas."""
           # Implementação com cache automático
           pass

🔍 **Debugging e Monitoramento**
-------------------------------

.. code-block:: python

   import time
   from contextlib import asynccontextmanager
   
   @asynccontextmanager
   async def performance_monitor(operation_name: str):
       """Context manager para monitorar performance."""
       start_time = time.time()
       logger.info(f"Iniciando: {operation_name}")
       
       try:
           yield
       finally:
           elapsed = time.time() - start_time
           logger.info(f"Concluído: {operation_name} em {elapsed:.3f}s")
   
   # Uso
   async def monitored_calculation():
       async with performance_monitor("Cálculo complexo"):
           result = await complex_calculation()
       return result

📋 **Checklist de Migração**
----------------------------

.. code-block:: text

   ✅ Análise do script AutoIt original
   ✅ Identificação de dependências
   ✅ Mapeamento de funções AutoIt → Python
   ✅ Criação da estrutura de classes
   ✅ Implementação de configuração
   ✅ Adição de type hints
   ✅ Implementação de logging
   ✅ Tratamento de exceções
   ✅ Criação de testes unitários
   ✅ Documentação do código
   ✅ Configuração de CI/CD
   ✅ Validação em múltiplos ambientes

🎯 **Resultado Final**
---------------------

Após a migração, você terá:

* **Código mais limpo** e manutenível
* **Testes automatizados** garantindo qualidade
* **Logging estruturado** para debugging
* **Performance melhorada** com async/await
* **Portabilidade** entre sistemas operacionais
* **Ecosystem Python** para extensões futuras

🔗 **Próximos Passos**
---------------------

1. Analise seu script AutoIt atual
2. Siga o processo de migração passo a passo
3. Adicione testes para validar o comportamento
4. Configure CI/CD para automação de qualidade
5. Explore o :doc:`examples` para casos mais complexos 