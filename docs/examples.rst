Exemplos Práticos
==================

Esta seção apresenta exemplos práticos e casos de uso do Autoit-Python.

🎯 **Exemplo 1: Automação Básica de Calculadora**
-------------------------------------------------

Este é o exemplo mais simples, perfeito para começar:

.. code-block:: python

   import asyncio
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def calculadora_basica():
       """Automação básica da calculadora."""
       
       # Configuração simples
       config = AutomationConfig(app_name="Calculadora")
       automation = WindowAutomation(config)
       
       # Executar automação
       resultado = await automation.run_automation()
       
       # Mostrar resultados
       if resultado["success"]:
           print("✅ Automação concluída com sucesso!")
           for calc in resultado["results"]:
               print(f"📊 {calc['description']}: {calc['result']}")
       else:
           print(f"❌ Erro: {resultado.get('error')}")

   # Executar
   asyncio.run(calculadora_basica())

🔧 **Exemplo 2: Configuração Personalizada**
--------------------------------------------

Exemplo com configurações avançadas:

.. code-block:: python

   import asyncio
   from pathlib import Path
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def automacao_personalizada():
       """Automação com configurações personalizadas."""
       
       # Configuração avançada
       config = AutomationConfig(
           app_name="Calculadora",
           timeout=15,  # Timeout maior para operações lentas
           output_dir=Path("./resultados_personalizados")
       )
       
       # Criar pasta se não existir
       config.output_dir.mkdir(exist_ok=True)
       
       automation = WindowAutomation(config)
       
       print(f"🚀 Iniciando automação personalizada...")
       print(f"📁 Resultados serão salvos em: {config.output_dir}")
       
       resultado = await automation.run_automation()
       
       if resultado["success"]:
           print(f"✅ {len(resultado['results'])} cálculos realizados")
           
           # Mostrar estatísticas
           tempos = [r["execution_time"] for r in resultado["results"]]
           print(f"⏱️ Tempo médio por cálculo: {sum(tempos)/len(tempos):.3f}s")
           print(f"⏱️ Tempo total: {sum(tempos):.3f}s")

   asyncio.run(automacao_personalizada())

🧪 **Exemplo 3: Tratamento de Erros Robusto**
---------------------------------------------

Exemplo com tratamento completo de erros:

.. code-block:: python

   import asyncio
   import logging
   from pathlib import Path
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   # Configurar logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   async def automacao_robusta():
       """Automação com tratamento robusto de erros."""
       
       try:
           # Configuração com validação
           config = AutomationConfig(
               app_name="Calculadora",
               timeout=10,
               output_dir=Path("./resultados_robustos")
           )
           
           # Validar configuração
           if not config.output_dir.exists():
               config.output_dir.mkdir(parents=True)
               logger.info(f"📁 Pasta criada: {config.output_dir}")
           
           automation = WindowAutomation(config)
           
           logger.info("🚀 Iniciando automação robusta...")
           resultado = await automation.run_automation()
           
           if resultado["success"]:
               sucessos = sum(1 for r in resultado["results"] if r["success"])
               total = len(resultado["results"])
               
               logger.info(f"✅ Automação concluída: {sucessos}/{total} sucessos")
               
               # Salvar relatório detalhado
               relatorio_path = config.output_dir / "relatorio_detalhado.txt"
               with open(relatorio_path, "w", encoding="utf-8") as f:
                   f.write("RELATÓRIO DE AUTOMAÇÃO\n")
                   f.write("=" * 50 + "\n\n")
                   
                   for i, calc in enumerate(resultado["results"], 1):
                       f.write(f"Cálculo {i}: {calc['description']}\n")
                       if calc["success"]:
                           f.write(f"  ✅ Resultado: {calc['result']}\n")
                           f.write(f"  ⏱️ Tempo: {calc['execution_time']:.3f}s\n")
                       else:
                           f.write(f"  ❌ Erro: {calc.get('error', 'Desconhecido')}\n")
                       f.write("\n")
               
               logger.info(f"📄 Relatório salvo: {relatorio_path}")
               
           else:
               logger.error(f"❌ Falha na automação: {resultado.get('error')}")
               
       except FileNotFoundError as e:
           logger.error(f"❌ Arquivo não encontrado: {e}")
       except PermissionError as e:
           logger.error(f"❌ Erro de permissão: {e}")
       except Exception as e:
           logger.error(f"❌ Erro inesperado: {e}")
           raise

   asyncio.run(automacao_robusta())

🔄 **Exemplo 4: Automação em Lote**
-----------------------------------

Processamento de múltiplas automações:

.. code-block:: python

   import asyncio
   from pathlib import Path
   from datetime import datetime
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def automacao_em_lote():
       """Executar múltiplas automações em lote."""
       
       # Configurações para diferentes cenários
       configuracoes = [
           {
               "nome": "Teste_Rapido",
               "timeout": 5,
               "pasta": "resultados_rapido"
           },
           {
               "nome": "Teste_Completo", 
               "timeout": 15,
               "pasta": "resultados_completo"
           },
           {
               "nome": "Teste_Extenso",
               "timeout": 30,
               "pasta": "resultados_extenso"
           }
       ]
       
       resultados_lote = []
       
       for i, cfg in enumerate(configuracoes, 1):
           print(f"\n🔄 Executando lote {i}/{len(configuracoes)}: {cfg['nome']}")
           
           try:
               config = AutomationConfig(
                   app_name="Calculadora",
                   timeout=cfg["timeout"],
                   output_dir=Path(cfg["pasta"])
               )
               
               config.output_dir.mkdir(exist_ok=True)
               
               automation = WindowAutomation(config)
               resultado = await automation.run_automation()
               
               # Adicionar metadados
               resultado["lote_nome"] = cfg["nome"]
               resultado["lote_index"] = i
               resultado["timestamp"] = datetime.now().isoformat()
               
               resultados_lote.append(resultado)
               
               if resultado["success"]:
                   print(f"  ✅ {cfg['nome']}: {len(resultado['results'])} cálculos")
               else:
                   print(f"  ❌ {cfg['nome']}: {resultado.get('error')}")
                   
           except Exception as e:
               print(f"  💥 Erro em {cfg['nome']}: {e}")
               resultados_lote.append({
                   "success": False,
                   "error": str(e),
                   "lote_nome": cfg["nome"],
                   "lote_index": i
               })
       
       # Relatório final do lote
       print("\n📊 RELATÓRIO FINAL DO LOTE")
       print("=" * 50)
       
       sucessos = sum(1 for r in resultados_lote if r["success"])
       total = len(resultados_lote)
       
       print(f"✅ Sucessos: {sucessos}/{total}")
       print(f"❌ Falhas: {total - sucessos}/{total}")
       print(f"📈 Taxa de sucesso: {(sucessos/total)*100:.1f}%")
       
       # Salvar relatório consolidado
       import json
       relatorio_path = Path("relatorio_lote.json")
       with open(relatorio_path, "w", encoding="utf-8") as f:
           json.dump(resultados_lote, f, indent=2, ensure_ascii=False)
       
       print(f"💾 Relatório salvo: {relatorio_path}")

   asyncio.run(automacao_em_lote())

🎨 **Exemplo 5: Interface de Linha de Comando**
-----------------------------------------------

Criando uma CLI para a automação:

.. code-block:: python

   import asyncio
   import argparse
   import sys
   from pathlib import Path
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   async def cli_automation(args):
       """Automação via linha de comando."""
       
       # Configurar baseado nos argumentos
       config = AutomationConfig(
           app_name=args.app or "Calculadora",
           timeout=args.timeout,
           output_dir=Path(args.output)
       )
       
       # Criar pasta de saída
       config.output_dir.mkdir(parents=True, exist_ok=True)
       
       if args.verbose:
           print(f"🔧 Configuração:")
           print(f"  App: {config.app_name}")
           print(f"  Timeout: {config.timeout}s")
           print(f"  Output: {config.output_dir}")
           print()
       
       automation = WindowAutomation(config)
       
       if not args.quiet:
           print("🚀 Iniciando automação...")
       
       resultado = await automation.run_automation()
       
       if resultado["success"]:
           if not args.quiet:
               print(f"✅ Automação concluída!")
               print(f"📊 Resultados: {len(resultado['results'])} cálculos")
           
           if args.verbose:
               for calc in resultado["results"]:
                   status = "✅" if calc["success"] else "❌"
                   print(f"  {status} {calc['description']}: {calc.get('result', calc.get('error'))}")
           
           return 0  # Código de sucesso
       else:
           if not args.quiet:
               print(f"❌ Falha na automação: {resultado.get('error')}")
           return 1  # Código de erro

   def main():
       """Função principal da CLI."""
       parser = argparse.ArgumentParser(
           description="Autoit-Python - Automação de Calculadora",
           formatter_class=argparse.RawDescriptionHelpFormatter,
           epilog="""
   Exemplos de uso:
     python cli_automation.py --verbose
     python cli_automation.py --app Calculator --timeout 20
     python cli_automation.py --output ./meus_resultados --quiet
           """
       )
       
       parser.add_argument(
           "--app", 
           default="Calculadora",
           help="Nome da aplicação (padrão: Calculadora)"
       )
       
       parser.add_argument(
           "--timeout", 
           type=int, 
           default=10,
           help="Timeout em segundos (padrão: 10)"
       )
       
       parser.add_argument(
           "--output", 
           default="./output",
           help="Pasta de saída (padrão: ./output)"
       )
       
       parser.add_argument(
           "--verbose", "-v",
           action="store_true",
           help="Modo verboso"
       )
       
       parser.add_argument(
           "--quiet", "-q",
           action="store_true", 
           help="Modo silencioso"
       )
       
       args = parser.parse_args()
       
       # Executar automação
       try:
           exit_code = asyncio.run(cli_automation(args))
           sys.exit(exit_code)
       except KeyboardInterrupt:
           print("\n⚠️ Automação interrompida pelo usuário")
           sys.exit(130)
       except Exception as e:
           print(f"💥 Erro inesperado: {e}")
           sys.exit(1)

   if __name__ == "__main__":
       main()

**Salve como `cli_automation.py` e use:**

.. code-block:: bash

   # Uso básico
   python cli_automation.py

   # Com opções
   python cli_automation.py --verbose --timeout 20 --output ./resultados

   # Modo silencioso
   python cli_automation.py --quiet

🔍 **Exemplo 6: Monitoramento e Métricas**
------------------------------------------

Automação com coleta de métricas detalhadas:

.. code-block:: python

   import asyncio
   import time
   import statistics
   from datetime import datetime
   from pathlib import Path
   from examples.python_migrations.window_automation import (
       AutomationConfig, WindowAutomation
   )

   class AutomationMonitor:
       """Monitor para coleta de métricas de automação."""
       
       def __init__(self):
           self.start_time = None
           self.end_time = None
           self.metrics = {
               "executions": 0,
               "successes": 0,
               "failures": 0,
               "total_time": 0,
               "execution_times": [],
               "errors": []
           }
       
       def start(self):
           """Iniciar monitoramento."""
           self.start_time = time.time()
           print("📊 Monitoramento iniciado")
       
       def record_execution(self, resultado):
           """Registrar execução."""
           self.metrics["executions"] += 1
           
           if resultado["success"]:
               self.metrics["successes"] += 1
               
               # Coletar tempos de execução
               for calc in resultado["results"]:
                   if "execution_time" in calc:
                       self.metrics["execution_times"].append(calc["execution_time"])
           else:
               self.metrics["failures"] += 1
               self.metrics["errors"].append(resultado.get("error", "Erro desconhecido"))
       
       def stop(self):
           """Parar monitoramento e gerar relatório."""
           self.end_time = time.time()
           self.metrics["total_time"] = self.end_time - self.start_time
           
           print("\n📈 RELATÓRIO DE MÉTRICAS")
           print("=" * 50)
           print(f"⏱️ Tempo total: {self.metrics['total_time']:.3f}s")
           print(f"🔄 Execuções: {self.metrics['executions']}")
           print(f"✅ Sucessos: {self.metrics['successes']}")
           print(f"❌ Falhas: {self.metrics['failures']}")
           
           if self.metrics["execution_times"]:
               times = self.metrics["execution_times"]
               print(f"⚡ Tempo médio por operação: {statistics.mean(times):.3f}s")
               print(f"⚡ Tempo mínimo: {min(times):.3f}s")
               print(f"⚡ Tempo máximo: {max(times):.3f}s")
           
           if self.metrics["failures"] > 0:
               print(f"\n🚨 Erros encontrados:")
               for i, error in enumerate(self.metrics["errors"], 1):
                   print(f"  {i}. {error}")
           
           # Taxa de sucesso
           if self.metrics["executions"] > 0:
               success_rate = (self.metrics["successes"] / self.metrics["executions"]) * 100
               print(f"\n📊 Taxa de sucesso: {success_rate:.1f}%")

   async def automacao_com_metricas():
       """Automação com monitoramento de métricas."""
       
       monitor = AutomationMonitor()
       monitor.start()
       
       try:
           # Múltiplas execuções para coletar métricas
           for i in range(3):
               print(f"\n🔄 Execução {i+1}/3")
               
               config = AutomationConfig(
                   app_name="Calculadora",
                   timeout=10,
                   output_dir=Path(f"metricas_exec_{i+1}")
               )
               
               config.output_dir.mkdir(exist_ok=True)
               
               automation = WindowAutomation(config)
               resultado = await automation.run_automation()
               
               monitor.record_execution(resultado)
               
               if resultado["success"]:
                   print(f"  ✅ Execução {i+1}: {len(resultado['results'])} cálculos")
               else:
                   print(f"  ❌ Execução {i+1}: {resultado.get('error')}")
               
               # Pequena pausa entre execuções
               await asyncio.sleep(1)
       
       finally:
           monitor.stop()

   asyncio.run(automacao_com_metricas())

📝 **Dicas de Uso**
-------------------

1. **Performance**: Use `async/await` para operações não-bloqueantes
2. **Logging**: Configure logs adequados para debugging
3. **Tratamento de Erros**: Sempre trate exceções específicas
4. **Configuração**: Use arquivos de configuração para ambientes diferentes
5. **Testes**: Execute testes regularmente para validar funcionamento

🔗 **Próximos Passos**
---------------------

* Explore a :doc:`api` para referência completa
* Consulte o :doc:`migration_guide` para migrar scripts AutoIt
* Veja :doc:`contributing` para contribuir com o projeto 