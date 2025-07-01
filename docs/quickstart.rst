Guia de Início Rápido
=====================

Este guia te ajudará a começar a usar o Autoit-Python em poucos minutos.

⚡ **Início em 5 Minutos**
--------------------------

1. **Instale o projeto**

.. code-block:: bash

   git clone https://github.com/tiagokf/Autoit-Python.git
   cd Autoit-Python
   pip install -r requirements.txt

2. **Execute o exemplo básico**

.. code-block:: bash

   python examples/python_migrations/window_automation.py

3. **Veja os resultados**

O script irá:

* ✅ Abrir a calculadora automaticamente
* ✅ Realizar cálculos matemáticos
* ✅ Salvar resultados em JSON
* ✅ Exibir relatório de execução

🎯 **Primeiro Exemplo Prático**
-------------------------------

Vamos criar uma automação simples:

.. code-block:: python

   import asyncio
   from pathlib import Path
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def minha_primeira_automacao():
       """Exemplo básico de automação."""
       
       # 1. Configurar a automação
       config = AutomationConfig(
           app_name="Calculadora",
           timeout=10,
           output_dir=Path("./meus_resultados")
       )
       
       # 2. Criar instância da automação
       automation = WindowAutomation(config)
       
       # 3. Executar automação
       print("🚀 Iniciando automação...")
       resultado = await automation.run_automation()
       
       # 4. Verificar resultados
       if resultado["success"]:
           print(f"✅ Sucesso! {len(resultado['results'])} cálculos realizados")
           
           # Mostrar cada resultado
           for calc in resultado["results"]:
               if calc["success"]:
                   print(f"  📊 {calc['description']}: {calc['result']}")
               else:
                   print(f"  ❌ Erro em {calc['description']}: {calc['error']}")
       else:
           print(f"❌ Falha na automação: {resultado.get('error')}")

   # Executar
   if __name__ == "__main__":
       asyncio.run(minha_primeira_automacao())

Salve este código como ``meu_exemplo.py`` e execute:

.. code-block:: bash

   python meu_exemplo.py

🔧 **Personalizando a Configuração**
------------------------------------

Você pode personalizar diversos aspectos da automação:

.. code-block:: python

   from pathlib import Path
   from examples.python_migrations.window_automation import AutomationConfig

   # Configuração personalizada
   config = AutomationConfig(
       app_name="Calculadora",           # Nome da aplicação
       timeout=15,                       # Timeout em segundos
       output_dir=Path("./resultados")   # Pasta de saída
   )

   # Verificar configuração
   print(f"App: {config.app_name}")
   print(f"Timeout: {config.timeout}s")
   print(f"Output: {config.output_dir}")

📊 **Entendendo os Resultados**
-------------------------------

A automação gera um arquivo JSON com estrutura detalhada:

.. code-block:: json

   {
     "metadata": {
       "timestamp": "2025-07-01T12:30:45.123456",
       "total": 3,
       "successful": 3
     },
     "results": [
       {
         "description": "123 + 456",
         "formula": "123+456=",
         "result": "579",
         "execution_time": 0.856,
         "timestamp": "2025-07-01T12:30:45.123456",
         "success": true
       }
     ]
   }

🧪 **Executando Testes**
------------------------

Para verificar se tudo está funcionando:

.. code-block:: bash

   # Testes básicos
   pytest tests/test_automation.py -v

   # Testes com cobertura
   pytest tests/ --cov=examples

   # Teste específico
   pytest tests/test_automation.py::TestAutomationConfig::test_default_values -v

🎨 **Verificando Qualidade**
----------------------------

O projeto inclui verificações de qualidade automáticas:

.. code-block:: bash

   # Formatação com Black
   black --check examples/ tests/

   # Linting com Flake8
   flake8 examples/ tests/

   # Type checking com MyPy
   mypy examples/

   # Análise de segurança
   bandit -r examples/

🔍 **Explorando o Código**
--------------------------

Estrutura principal do projeto:

.. code-block::

   examples/python_migrations/
   ├── window_automation.py      # 🎯 Módulo principal
   ├── pyautogui_demo.py        # 🖱️ Demos PyAutoGUI
   ├── selenium_automation.py    # 🌐 Automação web
   └── web_automation.py        # 🔗 Automação web avançada

   tests/
   ├── test_automation.py       # 🧪 Testes principais
   ├── test_window_automation.py # 🪟 Testes de janelas
   └── conftest.py              # ⚙️ Configuração de testes

🚀 **Próximos Passos**
----------------------

Agora que você executou seu primeiro exemplo:

1. **Explore mais exemplos**

   .. code-block:: bash

      # Demo completo do PyAutoGUI
      python examples/python_migrations/pyautogui_demo.py

      # Automação web com Selenium
      python examples/python_migrations/selenium_automation.py

2. **Personalize para suas necessidades**

   * Modifique os cálculos realizados
   * Altere a aplicação alvo
   * Customize o formato de saída

3. **Contribua com o projeto**

   * Reporte bugs ou sugestões
   * Adicione novos exemplos
   * Melhore a documentação

📚 **Recursos Adicionais**
--------------------------

* :doc:`examples` - Exemplos completos e casos de uso
* :doc:`api` - Referência completa da API
* :doc:`migration_guide` - Guia de migração AutoIt → Python
* :doc:`contributing` - Como contribuir com o projeto

🆘 **Precisa de Ajuda?**
-----------------------

* 📖 Consulte a documentação completa
* 🐛 Abra um `issue no GitHub <https://github.com/tiagokf/Autoit-Python/issues>`_
* 💬 Participe das discussões do projeto

✨ **Dicas Importantes**
-----------------------

.. tip::
   **Performance**: Use ``async/await`` para melhor performance em automações complexas.

.. warning::
   **Segurança**: Sempre valide entradas e trate exceções adequadamente.

.. note::
   **Compatibilidade**: O projeto funciona em Windows, Linux e macOS com adaptações automáticas. 