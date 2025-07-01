Instalação
===========

Este guia irá te ajudar a instalar e configurar o Autoit-Python em seu ambiente.

📋 **Requisitos**
-----------------

Antes de começar, certifique-se de ter:

* **Python 3.9+** instalado
* **Git** para clonar o repositório
* **Sistema operacional**: Windows, Linux ou macOS

Verificação do Python
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python --version
   # Deve retornar: Python 3.9.x ou superior

🔧 **Instalação Básica**
------------------------

1. **Clone o repositório**

.. code-block:: bash

   git clone https://github.com/tiagokf/Autoit-Python.git
   cd Autoit-Python

2. **Crie um ambiente virtual** (recomendado)

.. code-block:: bash

   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate

3. **Instale as dependências**

.. code-block:: bash

   # Dependências básicas
   pip install -r requirements.txt

   # Para desenvolvimento (opcional)
   pip install -r requirements-dev.txt

🔍 **Verificação da Instalação**
--------------------------------

Execute os testes para verificar se tudo está funcionando:

.. code-block:: bash

   # Executar todos os testes
   pytest tests/

   # Verificar qualidade do código
   black --check examples/ tests/
   flake8 examples/ tests/

   # Executar exemplo básico
   python examples/python_migrations/window_automation.py

🛠️ **Dependências Principais**
-------------------------------

O projeto utiliza as seguintes bibliotecas principais:

.. code-block:: text

   pyautogui>=0.9.54     # Automação de GUI
   pygetwindow>=0.0.9    # Gerenciamento de janelas
   loguru>=0.7.2         # Logging estruturado
   asyncio               # Programação assíncrona (built-in)

🧪 **Instalação para Desenvolvimento**
--------------------------------------

Se você planeja contribuir com o projeto:

.. code-block:: bash

   # Instalar dependências de desenvolvimento
   pip install -r requirements-dev.txt

   # Configurar pre-commit hooks (opcional)
   pre-commit install

   # Executar verificações completas
   black examples/ tests/
   flake8 examples/ tests/
   mypy examples/
   pytest tests/ --cov=examples

🐧 **Configuração Linux (Headless)**
------------------------------------

Para ambientes Linux sem interface gráfica (servidores):

.. code-block:: bash

   # Instalar Xvfb para display virtual
   sudo apt-get update
   sudo apt-get install -y xvfb

   # Executar com display virtual
   export DISPLAY=:99
   Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

🪟 **Configuração Windows**
---------------------------

No Windows, certifique-se de que:

* O Python está no PATH do sistema
* A calculadora do Windows está disponível (calc.exe)
* Não há bloqueios de antivírus para automação

🍎 **Configuração macOS**
-------------------------

No macOS, você pode precisar conceder permissões de acessibilidade:

1. Vá para **Preferências do Sistema** > **Segurança e Privacidade**
2. Clique na aba **Privacidade**
3. Selecione **Acessibilidade** na lista
4. Adicione o Terminal ou seu IDE à lista de aplicativos permitidos

⚠️ **Solução de Problemas**
---------------------------

Problemas Comuns
~~~~~~~~~~~~~~~~~

**Erro: ModuleNotFoundError**

.. code-block:: bash

   # Certifique-se de que o ambiente virtual está ativado
   pip list
   pip install -r requirements.txt

**Erro: Permission denied (Linux/macOS)**

.. code-block:: bash

   # Use sudo apenas se necessário
   sudo apt-get install python3-dev

**Erro: Calculadora não encontrada**

.. code-block:: bash

   # Windows: Verifique se calc.exe está no PATH
   where calc

   # Linux: Instale uma calculadora
   sudo apt-get install gnome-calculator

🔄 **Atualizações**
-------------------

Para atualizar o projeto:

.. code-block:: bash

   # Atualizar código
   git pull origin master

   # Atualizar dependências
   pip install -r requirements.txt --upgrade

📞 **Suporte**
--------------

Se encontrar problemas:

1. Verifique os `Issues do GitHub <https://github.com/tiagokf/Autoit-Python/issues>`_
2. Consulte a documentação completa
3. Abra um novo issue se necessário

✅ **Próximos Passos**
---------------------

Após a instalação bem-sucedida:

1. Leia o :doc:`quickstart` para começar rapidamente
2. Explore os :doc:`examples` disponíveis
3. Consulte a :doc:`api` para referência completa 