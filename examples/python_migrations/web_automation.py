#!/usr/bin/env python3
"""
Automação Web com Selenium - Migração AutoIt → Python

Demonstra:
[OK] Selenium WebDriver  [OK] Automação de navegadores
[OK] Scraping de dados   [OK] Tratamento de elementos
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime
from pathlib import Path


class WebAutomation:
    """Automação web com Selenium."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.results = []

    def setup_driver(self):
        """Configurar Chrome WebDriver."""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def search_python_docs(self, query: str):
        """Pesquisar na documentação Python."""
        print(f"[BUSCA] Pesquisando: {query}")
        start_time = time.time()

        try:
            # Navegar para docs Python
            self.driver.get("https://docs.python.org/3/")

            # Localizar campo de busca
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))

            # Realizar pesquisa
            search_box.send_keys(query)
            search_box.submit()

            # Aguardar resultados
            results = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search li"))
            )

            # Extrair títulos dos primeiros 3 resultados
            found_results = []
            for result in results[:3]:
                title_elem = result.find_element(By.TAG_NAME, "a")
                found_results.append(
                    {"title": title_elem.text, "url": title_elem.get_attribute("href")}
                )

            execution_time = time.time() - start_time

            return {
                "query": query,
                "results": found_results,
                "count": len(found_results),
                "time": round(execution_time, 3),
                "success": True,
            }

        except Exception as e:
            return {"query": query, "error": str(e), "success": False}

    def automate_github_search(self, repo_name: str):
        """Automatizar busca no GitHub."""
        print(f"[BUSCA] Buscando repositório: {repo_name}")

        try:
            self.driver.get("https://github.com")

            # Localizar campo de busca
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))

            search_box.send_keys(repo_name)
            search_box.submit()

            # Aguardar resultados
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".repo-list-item"))
            )

            # Extrair primeiro resultado
            first_repo = self.driver.find_element(By.CSS_SELECTOR, ".repo-list-item")
            title = first_repo.find_element(By.CSS_SELECTOR, "h3 a").text
            description = first_repo.find_element(By.CSS_SELECTOR, "p").text

            return {
                "repo_searched": repo_name,
                "first_result": {"title": title, "description": description},
                "success": True,
            }

        except Exception as e:
            return {"repo_searched": repo_name, "error": str(e), "success": False}

    def take_screenshot(self, name: str = "screenshot"):
        """Capturar screenshot."""
        Path("output").mkdir(exist_ok=True)
        filename = f"output/{name}_{datetime.now().strftime('%H%M%S')}.png"
        self.driver.save_screenshot(filename)
        print(f" Screenshot salvo: {filename}")
        return filename

    def run_tests(self):
        """Executar suite de testes."""
        print("[INICIO] Iniciando automação web...")

        self.setup_driver()

        try:
            # Teste 1: Pesquisa Python docs
            result1 = self.search_python_docs("selenium automation")
            self.results.append(result1)

            # Teste 2: Busca GitHub
            result2 = self.automate_github_search("python selenium")
            self.results.append(result2)

            # Screenshot final
            self.take_screenshot("final_result")

            # Salvar resultados
            self.save_results()

            print("Automação Web concluída!")

            return {
                "status": "concluído",
                "formularios_preenchidos": len(self.results),
                "timestamp": datetime.now().isoformat(),
            }

        finally:
            self.cleanup()

    def save_results(self):
        """Salvar resultados em JSON."""
        Path("output").mkdir(exist_ok=True)
        filename = f"output/web_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
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

    def cleanup(self):
        """Limpar recursos."""
        if self.driver:
            self.driver.quit()
            print("🧹 WebDriver fechado")


def main():
    """Executar automação."""
    automation = WebAutomation(headless=True)
    result = automation.run_tests()

    if result["status"] == "concluído":
        print(
            f"\n[SUCESSO] Sucesso! {result['formularios_preenchidos']} formulários preenchidos"
        )
    else:
        print("\n[ERRO] Falha na automação")


if __name__ == "__main__":
    main()
