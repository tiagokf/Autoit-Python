Autoit-Python - Migração AutoIt para Python
========================================

.. image:: https://img.shields.io/badge/Python-3.9%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://github.com/tiagokf/Autoit-Python/workflows/CI/badge.svg
   :target: https://github.com/tiagokf/Autoit-Python/actions
   :alt: CI Status

**Autoit-Python** é um projeto de migração profissional de scripts AutoIt para Python, demonstrando como modernizar automações legadas com melhorias significativas em arquitetura, performance e manutenibilidade.

🎯 **Objetivo Principal**
------------------------

Demonstrar a migração completa de automações AutoIt para Python com:

* ✅ **Arquitetura modular** e orientada a objetos
* ✅ **Type hints** completos para melhor IDE support
* ✅ **Logging estruturado** com Loguru
* ✅ **Tratamento robusto** de exceções
* ✅ **Testes automatizados** com pytest
* ✅ **Performance otimizada** com async/await
* ✅ **CI/CD pipeline** completo

🚀 **Recursos Implementados**
-----------------------------

Automação de Janelas
~~~~~~~~~~~~~~~~~~~~~

O módulo principal demonstra automação de calculadora com:

* Abertura automática de aplicações
* Detecção e ativação de janelas
* Operações de mouse e teclado
* Captura e processamento de resultados
* Salvamento em formato JSON estruturado

Qualidade de Código
~~~~~~~~~~~~~~~~~~~

* **Black**: Formatação automática de código
* **Flake8**: Análise de qualidade e style guide
* **MyPy**: Verificação de tipos estática
* **Bandit**: Análise de segurança
* **Safety**: Verificação de vulnerabilidades

Testes Automatizados
~~~~~~~~~~~~~~~~~~~~

* **Pytest**: Framework de testes moderno
* **Coverage**: Relatórios de cobertura de código
* **Mocks**: Testes isolados e determinísticos
* **CI/CD**: Testes em múltiplos ambientes (Windows/Linux)

📚 **Guia de Uso**
------------------

.. toctree::
   :maxdepth: 2
   :caption: Documentação:

   installation
   quickstart
   examples
   api
   migration_guide
   contributing

🔧 **Instalação Rápida**
------------------------

.. code-block:: bash

   # Clone o repositório
   git clone https://github.com/tiagokf/Autoit-Python.git
   cd Autoit-Python

   # Instale as dependências
   pip install -r requirements.txt

   # Execute os testes
   pytest tests/

   # Execute a automação
   python examples/python_migrations/window_automation.py

📖 **Exemplo de Uso**
---------------------

.. code-block:: python

   import asyncio
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def main():
       # Configurar automação
       config = AutomationConfig(
           app_name="Calculadora",
           timeout=5
       )
       
       # Executar automação
       automation = WindowAutomation(config)
       result = await automation.run_automation()
       
       if result["success"]:
           print(f"✅ Automação concluída: {len(result['results'])} cálculos")
       else:
           print(f"❌ Erro: {result.get('error')}")

   if __name__ == "__main__":
       asyncio.run(main())

🏗️ **Arquitetura**
------------------

O projeto segue uma arquitetura modular:

.. code-block::

   Autoit-Python/
   ├── examples/
   │   ├── autoit_originals/     # Scripts AutoIt originais
   │   ├── comparisons/          # Análises comparativas
   │   └── python_migrations/    # Versões Python migradas
   ├── tests/                    # Testes automatizados
   ├── docs/                     # Documentação
   └── .github/workflows/        # Pipeline CI/CD

🔄 **Comparação AutoIt vs Python**
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspecto
     - AutoIt
     - Python (Migrado)
   * - **Arquitetura**
     - Script monolítico
     - Classes modulares
   * - **Type Safety**
     - Tipagem dinâmica
     - Type hints + MyPy
   * - **Logging**
     - Print básico
     - Loguru estruturado
   * - **Testes**
     - Manual
     - Pytest automatizado
   * - **Performance**
     - Síncrono
     - Async/await
   * - **Manutenibilidade**
     - Baixa
     - Alta (SOLID)

🤝 **Contribuindo**
-------------------

Contribuições são bem-vindas! Veja o :doc:`contributing` para detalhes.

📄 **Licença**
--------------

Este projeto está licenciado sob a MIT License - veja o arquivo `LICENSE` para detalhes.

🔗 **Links Úteis**
------------------

* `GitHub Repository <https://github.com/tiagokf/Autoit-Python>`_
* `CI/CD Pipeline <https://github.com/tiagokf/Autoit-Python/actions>`_
* `Issues <https://github.com/tiagokf/Autoit-Python/issues>`_
* `Pull Requests <https://github.com/tiagokf/Autoit-Python/pulls>`_

Índices e Tabelas
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 