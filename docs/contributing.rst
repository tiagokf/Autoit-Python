Contribuindo
============

Obrigado pelo interesse em contribuir com o Autoit-Python! Este guia te ajudará a contribuir de forma efetiva.

🎯 **Como Contribuir**
---------------------

Existem várias formas de contribuir:

* 🐛 **Reportar bugs** e problemas
* ✨ **Sugerir melhorias** e novas funcionalidades
* 📝 **Melhorar documentação**
* 🧪 **Adicionar testes**
* 💻 **Contribuir com código**
* 🔍 **Revisar pull requests**

🚀 **Configuração do Ambiente de Desenvolvimento**
--------------------------------------------------

1. **Fork do Repositório**

.. code-block:: bash

   # Fork no GitHub e clone seu fork
   git clone https://github.com/SEU_USUARIO/Autoit-Python.git
   cd Autoit-Python

2. **Configurar Ambiente Virtual**

.. code-block:: bash

   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar ambiente virtual
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate

3. **Instalar Dependências de Desenvolvimento**

.. code-block:: bash

   # Instalar todas as dependências
   pip install -r requirements-dev.txt
   
   # Verificar instalação
   pytest --version
   black --version
   flake8 --version

4. **Configurar Pre-commit Hooks** (Opcional)

.. code-block:: bash

   # Instalar pre-commit
   pip install pre-commit
   
   # Configurar hooks
   pre-commit install
   
   # Testar hooks
   pre-commit run --all-files

📋 **Padrões de Desenvolvimento**
---------------------------------

Estilo de Código
~~~~~~~~~~~~~~~~

Seguimos as melhores práticas Python:

.. code-block:: python

   # ✅ BOM: Type hints e docstrings
   from typing import Optional, List
   
   async def calculate_formula(formula: str, timeout: int = 5) -> Optional[str]:
       """
       Calcular fórmula matemática.
       
       Args:
           formula: Fórmula a ser calculada (ex: "123+456")
           timeout: Timeout em segundos
           
       Returns:
           Resultado do cálculo ou None se falhar
           
       Raises:
           ValueError: Se a fórmula for inválida
       """
       if not formula.strip():
           raise ValueError("Fórmula não pode estar vazia")
       
       # Implementação...
       return result

   # ❌ RUIM: Sem type hints nem documentação
   def calc(f, t=5):
       if not f:
           return None
       # ...

Formatação
~~~~~~~~~~

.. code-block:: bash

   # Aplicar formatação automática
   black examples/ tests/ docs/
   
   # Verificar qualidade
   flake8 examples/ tests/
   
   # Type checking
   mypy examples/

Estrutura de Commits
~~~~~~~~~~~~~~~~~~~

Use mensagens de commit claras e descritivas:

.. code-block:: bash

   # ✅ BOM: Mensagem clara e específica
   git commit -m "🐛 Corrigir timeout na automação de calculadora
   
   - Aumentar timeout padrão de 5s para 10s
   - Adicionar retry logic para janelas lentas
   - Melhorar tratamento de exceções
   
   Fixes #123"
   
   # ❌ RUIM: Mensagem vaga
   git commit -m "fix bug"

Prefixos de Commit
~~~~~~~~~~~~~~~~~

Use emojis e prefixos consistentes:

* 🐛 `:bug:` - Correção de bugs
* ✨ `:sparkles:` - Nova funcionalidade
* 📝 `:memo:` - Documentação
* 🎨 `:art:` - Melhoria de código/estrutura
* ⚡ `:zap:` - Melhoria de performance
* 🧪 `:test_tube:` - Adição/correção de testes
* 🔧 `:wrench:` - Configuração/ferramentas
* 📦 `:package:` - Dependências

🧪 **Testes**
-------------

Sempre adicione testes para suas contribuições:

.. code-block:: python

   import pytest
   from unittest.mock import patch, MagicMock
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   class TestWindowAutomation:
       """Testes para automação de janelas."""
       
       @pytest.fixture
       def config(self):
           """Fixture para configuração."""
           return AutomationConfig(
               app_name="TestApp",
               timeout=10
           )
       
       @pytest.fixture
       def automation(self, config):
           """Fixture para automação."""
           return WindowAutomation(config)
       
       @patch('subprocess.Popen')
       async def test_open_calculator(self, mock_popen, automation):
           """Testar abertura da calculadora."""
           mock_popen.return_value = MagicMock()
           
           # Simular janela encontrada
           with patch('pygetwindow.getWindowsWithTitle') as mock_get_windows:
               mock_window = MagicMock()
               mock_get_windows.return_value = [mock_window]
               
               await automation._open_calculator()
               
               mock_popen.assert_called_once()
               mock_window.activate.assert_called_once()
       
       async def test_config_validation(self):
           """Testar validação de configuração."""
           # Teste com valores válidos
           config = AutomationConfig(app_name="Test", timeout=15)
           assert config.app_name == "Test"
           assert config.timeout == 15
           
           # Teste com valores padrão
           config_default = AutomationConfig()
           assert config_default.app_name == "Calculadora"
           assert config_default.timeout == 5

Executar Testes
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Executar todos os testes
   pytest tests/ -v
   
   # Executar com cobertura
   pytest tests/ --cov=examples --cov-report=html
   
   # Executar testes específicos
   pytest tests/test_automation.py::TestAutomationConfig -v
   
   # Executar testes em paralelo
   pytest tests/ -n auto

📝 **Documentação**
-------------------

Sempre documente suas contribuições:

Docstrings
~~~~~~~~~~

.. code-block:: python

   class NewFeature:
       """
       Nova funcionalidade para automação.
       
       Esta classe implementa uma nova funcionalidade que permite...
       
       Args:
           param1: Descrição do primeiro parâmetro
           param2: Descrição do segundo parâmetro
           
       Example:
           >>> feature = NewFeature("valor1", 42)
           >>> result = await feature.execute()
           >>> print(result)
           "resultado esperado"
       """
       
       def __init__(self, param1: str, param2: int):
           """
           Inicializar nova funcionalidade.
           
           Args:
               param1: Parâmetro de configuração
               param2: Valor numérico para processamento
           """
           self.param1 = param1
           self.param2 = param2
       
       async def execute(self) -> str:
           """
           Executar funcionalidade.
           
           Returns:
               Resultado da execução
               
           Raises:
               ValueError: Se parâmetros forem inválidos
               RuntimeError: Se execução falhar
           """
           # Implementação...
           pass

Atualizar Documentação
~~~~~~~~~~~~~~~~~~~~~~

Se adicionar nova funcionalidade, atualize a documentação:

.. code-block:: bash

   # Gerar documentação localmente
   cd docs/
   make html
   
   # Visualizar no navegador
   # Windows:
   start _build/html/index.html
   # Linux:
   xdg-open _build/html/index.html
   # macOS:
   open _build/html/index.html

🔄 **Processo de Pull Request**
-------------------------------

1. **Criar Branch**

.. code-block:: bash

   # Criar branch para sua feature
   git checkout -b feature/minha-nova-funcionalidade
   
   # Ou para bugfix
   git checkout -b bugfix/corrigir-problema-x

2. **Implementar Mudanças**

.. code-block:: bash

   # Fazer suas mudanças
   # Adicionar testes
   # Atualizar documentação

3. **Verificar Qualidade**

.. code-block:: bash

   # Formatação
   black examples/ tests/
   
   # Linting
   flake8 examples/ tests/
   
   # Type checking
   mypy examples/
   
   # Testes
   pytest tests/ -v
   
   # Segurança
   bandit -r examples/

4. **Commit e Push**

.. code-block:: bash

   # Adicionar arquivos
   git add .
   
   # Commit com mensagem descritiva
   git commit -m "✨ Adicionar nova funcionalidade X
   
   - Implementar classe NewFeature
   - Adicionar testes unitários
   - Atualizar documentação
   - Exemplo de uso incluído"
   
   # Push para seu fork
   git push origin feature/minha-nova-funcionalidade

5. **Abrir Pull Request**

No GitHub, abra um PR com:

* **Título claro** descrevendo a mudança
* **Descrição detalhada** do que foi implementado
* **Referência a issues** relacionadas (se houver)
* **Screenshots** se aplicável
* **Checklist** de verificação

Template de PR:

.. code-block:: markdown

   ## 📋 Descrição
   
   Breve descrição das mudanças implementadas.
   
   ## 🔄 Tipo de Mudança
   
   - [ ] 🐛 Correção de bug
   - [ ] ✨ Nova funcionalidade
   - [ ] 📝 Documentação
   - [ ] 🎨 Refatoração
   - [ ] ⚡ Melhoria de performance
   
   ## 🧪 Testes
   
   - [ ] Testes unitários adicionados/atualizados
   - [ ] Todos os testes passando
   - [ ] Cobertura de código mantida/melhorada
   
   ## 📝 Documentação
   
   - [ ] Docstrings atualizadas
   - [ ] Documentação Sphinx atualizada
   - [ ] Exemplos de uso incluídos
   
   ## ✅ Checklist
   
   - [ ] Código formatado com Black
   - [ ] Linting com Flake8 passou
   - [ ] Type checking com MyPy passou
   - [ ] Testes unitários passando
   - [ ] Documentação atualizada
   
   ## 🔗 Issues Relacionadas
   
   Closes #123
   Related to #456

🐛 **Reportando Bugs**
---------------------

Para reportar bugs, use o template:

.. code-block:: markdown

   ## 🐛 Descrição do Bug
   
   Descrição clara e concisa do bug.
   
   ## 🔄 Passos para Reproduzir
   
   1. Vá para '...'
   2. Clique em '...'
   3. Execute '...'
   4. Veja o erro
   
   ## ✅ Comportamento Esperado
   
   Descrição do que deveria acontecer.
   
   ## ❌ Comportamento Atual
   
   Descrição do que realmente acontece.
   
   ## 🖥️ Ambiente
   
   - OS: [e.g. Windows 10, Ubuntu 20.04]
   - Python: [e.g. 3.9.7]
   - Versão do projeto: [e.g. 1.0.0]
   
   ## 📎 Logs/Screenshots
   
   Adicione logs de erro ou screenshots se aplicável.

💡 **Sugerindo Melhorias**
-------------------------

Para sugerir melhorias:

.. code-block:: markdown

   ## 💡 Descrição da Melhoria
   
   Descrição clara da melhoria proposta.
   
   ## 🎯 Problema que Resolve
   
   Qual problema esta melhoria resolve?
   
   ## 💻 Solução Proposta
   
   Descrição detalhada da solução.
   
   ## 🔄 Alternativas Consideradas
   
   Outras soluções que foram consideradas.
   
   ## 📈 Benefícios
   
   - Melhoria de performance
   - Melhor experiência do usuário
   - Código mais limpo
   
   ## 📋 Tarefas
   
   - [ ] Implementar funcionalidade X
   - [ ] Adicionar testes
   - [ ] Atualizar documentação

🏆 **Reconhecimento**
--------------------

Contribuidores são reconhecidos:

* **README.md** - Lista de contribuidores
* **CHANGELOG.md** - Créditos por release
* **Documentação** - Seção de agradecimentos
* **Issues/PRs** - Menção e agradecimento

📞 **Suporte**
--------------

Se precisar de ajuda:

* 💬 **Discussões**: Use as GitHub Discussions
* 🐛 **Issues**: Para bugs e problemas técnicos
* 📧 **Email**: Para questões privadas
* 📖 **Documentação**: Consulte a documentação completa

🔗 **Links Úteis**
------------------

* `Repositório GitHub <https://github.com/tiagokf/Autoit-Python>`_
* `Issues <https://github.com/tiagokf/Autoit-Python/issues>`_
* `Pull Requests <https://github.com/tiagokf/Autoit-Python/pulls>`_
* `Discussões <https://github.com/tiagokf/Autoit-Python/discussions>`_
* `CI/CD Pipeline <https://github.com/tiagokf/Autoit-Python/actions>`_

🙏 **Obrigado!**
----------------

Sua contribuição faz a diferença! Juntos, tornamos o Autoit-Python melhor para toda a comunidade Python. 🐍✨ 