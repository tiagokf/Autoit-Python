Referência da API
==================

Esta seção documenta todas as classes, funções e módulos do Autoit-Python.

📦 **Módulos Principais**
-------------------------

.. toctree::
   :maxdepth: 2

   api/window_automation
   api/pyautogui_examples
   api/web_automation

🏗️ **Automação de Janelas**
---------------------------

.. automodule:: examples.python_migrations.window_automation
   :members:
   :undoc-members:
   :show-inheritance:

AutomationConfig
~~~~~~~~~~~~~~~~

.. autoclass:: examples.python_migrations.window_automation.AutomationConfig
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemplo de uso:**

   .. code-block:: python

      from pathlib import Path
      from examples.python_migrations.window_automation import AutomationConfig

      config = AutomationConfig(
          app_name="Calculadora",
          timeout=10,
          output_dir=Path("./resultados")
      )

WindowAutomation
~~~~~~~~~~~~~~~~

.. autoclass:: examples.python_migrations.window_automation.WindowAutomation
   :members:
   :undoc-members:
   :show-inheritance:

   **Métodos principais:**

   .. automethod:: examples.python_migrations.window_automation.WindowAutomation.run_automation

   .. automethod:: examples.python_migrations.window_automation.WindowAutomation._open_calculator

   .. automethod:: examples.python_migrations.window_automation.WindowAutomation._find_window

   .. automethod:: examples.python_migrations.window_automation.WindowAutomation._calculate

   **Exemplo de uso:**

   .. code-block:: python

      import asyncio
      from examples.python_migrations.window_automation import (
          AutomationConfig, WindowAutomation
      )

      async def exemplo():
          config = AutomationConfig()
          automation = WindowAutomation(config)
          resultado = await automation.run_automation()
          return resultado

🖱️ **Exemplos PyAutoGUI**
-------------------------

.. automodule:: examples.python_migrations.pyautogui_demo
   :members:
   :undoc-members:
   :show-inheritance:

🌐 **Automação Web**
-------------------

.. automodule:: examples.python_migrations.web_automation
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: examples.python_migrations.selenium_automation
   :members:
   :undoc-members:
   :show-inheritance:

🧪 **Utilitários de Teste**
---------------------------

.. automodule:: tests.conftest
   :members:
   :undoc-members:
   :show-inheritance:

Funções Utilitárias
~~~~~~~~~~~~~~~~~~~

.. autofunction:: tests.conftest.is_ci_environment

.. autofunction:: tests.conftest.is_gui_available

📊 **Tipos e Estruturas de Dados**
----------------------------------

Resultado da Automação
~~~~~~~~~~~~~~~~~~~~~~~

A estrutura de dados retornada pela automação:

.. code-block:: python

   {
       "success": bool,           # Indica se a automação foi bem-sucedida
       "results": List[Dict],     # Lista de resultados dos cálculos
       "error": str               # Mensagem de erro (se houver)
   }

Resultado Individual
~~~~~~~~~~~~~~~~~~~

Cada item na lista de resultados:

.. code-block:: python

   {
       "description": str,        # Descrição do cálculo
       "formula": str,           # Fórmula executada
       "result": str,            # Resultado obtido
       "execution_time": float,  # Tempo de execução em segundos
       "timestamp": str,         # ISO timestamp da execução
       "success": bool,          # Sucesso do cálculo individual
       "error": str              # Erro (se houver)
   }

⚙️ **Configurações e Constantes**
---------------------------------

Configurações Padrão
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Configurações padrão do AutomationConfig
   DEFAULT_APP_NAME = "Calculadora"
   DEFAULT_TIMEOUT = 5
   DEFAULT_OUTPUT_DIR = Path("./output")

Timeouts e Delays
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Delays utilizados na automação
   WINDOW_ACTIVATION_DELAY = 0.5    # Delay após ativar janela
   CALCULATION_DELAY = 0.2          # Delay entre operações
   CLIPBOARD_DELAY = 0.3            # Delay para operações de clipboard

🔧 **Utilitários e Helpers**
----------------------------

Detecção de Ambiente
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tests.conftest import is_ci_environment, is_gui_available

   # Verificar se está rodando em CI/CD
   if is_ci_environment():
       print("Rodando em ambiente CI/CD")

   # Verificar se GUI está disponível
   if is_gui_available():
       print("Interface gráfica disponível")

🚨 **Exceções e Tratamento de Erros**
-------------------------------------

O projeto define várias exceções customizadas:

.. code-block:: python

   # Exceções comuns que podem ser lançadas
   class AutomationError(Exception):
       """Erro geral de automação"""
       pass

   class WindowNotFoundError(AutomationError):
       """Janela não encontrada"""
       pass

   class CalculationError(AutomationError):
       """Erro durante cálculo"""
       pass

**Exemplo de tratamento:**

.. code-block:: python

   try:
       resultado = await automation.run_automation()
   except WindowNotFoundError:
       print("❌ Calculadora não encontrada")
   except CalculationError as e:
       print(f"❌ Erro no cálculo: {e}")
   except Exception as e:
       print(f"❌ Erro inesperado: {e}")

📈 **Performance e Otimizações**
-------------------------------

Dicas para melhor performance:

.. code-block:: python

   # Use async/await para operações não-bloqueantes
   async def automacao_otimizada():
       tasks = []
       for calc in calculos:
           task = asyncio.create_task(executar_calculo(calc))
           tasks.append(task)
       
       resultados = await asyncio.gather(*tasks)
       return resultados

🔍 **Debugging e Logs**
----------------------

O projeto usa Loguru para logging estruturado:

.. code-block:: python

   from loguru import logger

   # Configurar logging para debugging
   logger.add("debug.log", level="DEBUG", rotation="10 MB")

   # Logs disponíveis
   logger.debug("Informação de debug")
   logger.info("Informação geral")
   logger.warning("Aviso")
   logger.error("Erro")
   logger.success("Operação bem-sucedida")

🔗 **Integrações Externas**
--------------------------

Bibliotecas Integradas
~~~~~~~~~~~~~~~~~~~~~~

* **PyAutoGUI**: Automação de GUI
* **PyGetWindow**: Gerenciamento de janelas  
* **Loguru**: Logging estruturado
* **Asyncio**: Programação assíncrona
* **Pathlib**: Manipulação de caminhos
* **JSON**: Serialização de dados

📝 **Exemplos de Uso Avançado**
------------------------------

Automação Customizada
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class MinhaAutomacao(WindowAutomation):
       """Automação customizada estendendo a classe base."""
       
       async def meu_calculo_customizado(self, formula: str) -> Dict:
           """Implementar cálculo personalizado."""
           # Sua lógica aqui
           pass

   # Uso
   config = AutomationConfig(app_name="MeuApp")
   automacao = MinhaAutomacao(config)
   resultado = await automacao.run_automation()

📊 **Métricas e Monitoramento**
------------------------------

O projeto coleta métricas automáticas:

.. code-block:: python

   # Métricas disponíveis nos resultados
   metricas = {
       "total_executions": len(resultados),
       "successful_executions": sum(1 for r in resultados if r["success"]),
       "average_execution_time": statistics.mean(r["execution_time"] for r in resultados),
       "total_time": sum(r["execution_time"] for r in resultados)
   } 