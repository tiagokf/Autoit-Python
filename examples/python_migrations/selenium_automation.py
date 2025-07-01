#!/usr/bin/env python3
"""
Exemplo de Automação Web com Selenium
Migração de AutoIt para Python

Demonstra competências em:
[OK] Selenium WebDriver
[OK] Automação de navegadores
[OK] Scraping de dados
[OK] Tratamento de elementos web
[OK] Configuração de drivers
"""

import time
from typing import Dict, List, Optional
from pathlib import Path
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
from selenium.webdriver.chrome.service import Service


class WebAutomation:
    """Automação web com Selenium - Migração de AutoIt."""

    def __init__(self, browser: str = "chrome", headless: bool = False):
        """
        Inicializar automação web.

        Args:
            browser: Navegador a usar (chrome, firefox, edge)
            headless: Executar sem interface gráfica
        """
        self.browser = browser
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.results: List[Dict] = []

        self.wait = WebDriverWait(self.driver, 10)
        logger.info("WebAutomation inicializada")

    def setup_driver(self) -> None:
        """Configurar WebDriver com opções otimizadas."""
        logger.info("Configurando WebDriver...")

        if self.browser.lower() == "chrome":
            options = ChromeOptions()

            # Opções anti-detecção de bot
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # User agent mais realista
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
            options.add_argument(f"--user-agent={user_agent}")

            # Configurações de janela
            if self.headless:
                options.add_argument("--headless")
            else:
                options.add_argument("--start-maximized")

            # Configurar driver
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)

        elif self.browser.lower() == "firefox":
            # Configuração para Firefox (opcional)
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
            self.wait = WebDriverWait(self.driver, 10)

        else:
            raise ValueError(
                f"Navegador não suportado: {self.browser}. " "Use 'chrome' ou 'firefox'"
            )

        # Configurar timeouts aumentados
        self.driver.implicitly_wait(15)
        self.driver.set_page_load_timeout(45)

        # Configurar WebDriverWait com timeout maior
        self.wait = WebDriverWait(self.driver, 20)

        logger.success("WebDriver configurado com sucesso")

    def search_google(self, query: str) -> Dict:
        """
        Pesquisar no Google e extrair resultados.

        Args:
            query: Termo de pesquisa

        Returns:
            Dicionário com resultados da pesquisa
        """
        logger.info(f"Pesquisando no Google: {query}")
        start_time = time.time()

        try:
            # Navegar para o Google
            self.driver.get("https://www.google.com")

            # Aguardar página carregar
            time.sleep(2)

            # Tentar aceitar cookies se aparecer
            try:
                accept_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(text(), 'Aceitar') or "
                            "contains(text(), 'Accept') or "
                            "contains(text(), 'I agree')]",
                        )
                    )
                )
                accept_button.click()
                time.sleep(1)
                logger.info("Cookies aceitos")
            except TimeoutException:
                logger.info("Popup de cookies não encontrado ou já aceito")
            except Exception as e:
                logger.debug(f"Não foi possível aceitar cookies: {e}")

            # Localizar campo de pesquisa (múltiplos seletores)
            search_box = None
            selectors = [
                (By.NAME, "q"),
                (By.CSS_SELECTOR, "input[name='q']"),
                (By.CSS_SELECTOR, "textarea[name='q']"),
                (By.CSS_SELECTOR, "[title='Pesquisar']"),
                (By.CSS_SELECTOR, "[title='Search']"),
            ]

            for by, selector in selectors:
                try:
                    search_box = self.wait.until(
                        EC.presence_of_element_located((by, selector))
                    )
                    logger.info(f"Campo de pesquisa encontrado com: {selector}")
                    break
                except TimeoutException:
                    continue

            if not search_box:
                raise Exception("Campo de pesquisa não encontrado")

            # Realizar pesquisa com timing mais humano
            search_box.clear()
            time.sleep(0.5)

            # Digitar com pequenos intervalos para simular digitação humana
            for char in query:
                search_box.send_keys(char)
                time.sleep(0.05)  # 50ms entre caracteres

            time.sleep(0.5)
            search_box.send_keys(Keys.RETURN)

            # Aguardar resultados com múltiplos seletores
            results_found = False
            result_selectors = [
                (By.ID, "search"),
                (By.CSS_SELECTOR, "#search"),
                (By.CSS_SELECTOR, "[data-async-context*='query']"),
                (By.CSS_SELECTOR, ".g"),
                (By.CSS_SELECTOR, "[data-ved]"),
            ]

            for by, selector in result_selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((by, selector)))
                    results_found = True
                    logger.info(f"Resultados encontrados com: {selector}")
                    break
                except TimeoutException:
                    continue

            if not results_found:
                raise Exception("Página de resultados não carregou")

            # Aguardar um pouco mais para garantir carregamento completo
            time.sleep(2)

            # Extrair resultados
            results = self._extract_search_results()

            execution_time = time.time() - start_time

            result = {
                "query": query,
                "results_count": len(results),
                "results": results,
                "execution_time": round(execution_time, 3),
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }

            logger.success(
                f"Pesquisa concluída",
                query=query,
                results=len(results),
                time=f"{execution_time:.3f}s",
            )

            return result

        except Exception as e:
            logger.error(f"Erro na pesquisa: {query}", error=str(e))

            # Capturar screenshot para debug
            try:
                debug_screenshot = self.take_screenshot(
                    f"debug_google_error_{int(time.time())}.png"
                )
                logger.info(f"Screenshot de debug salvo: {debug_screenshot}")
            except BaseException:
                pass

            return {
                "query": query,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }

    def _extract_search_results(self) -> List[Dict]:
        """Extrair resultados da pesquisa do Google."""
        results = []

        try:
            # Múltiplos seletores para elementos de resultado
            result_selectors = [
                "div.g",  # Seletor clássico
                "[data-ved] h3..",  # Baseado em atributos do Google
                ".yuRUbf",  # Seletor mais novo
                ".tF2Cxc",  # Outro seletor comum
                "[jscontroller] h3..",  # Baseado em JS controller
            ]

            result_elements = []
            for selector in result_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        result_elements = elements
                        logger.info(f"Resultados encontrados com seletor: {selector}")
                        break
                except Exception:
                    continue

            if not result_elements:
                logger.warning("Nenhum elemento de resultado encontrado")
                return results

            # Processar até 5 resultados
            for i, element in enumerate(result_elements[:5]):
                try:
                    # Múltiplos seletores para título
                    title = ""
                    title_selectors = ["h3", ".LC20lb", "[role='heading']", ".DKV0Md"]
                    for t_selector in title_selectors:
                        try:
                            title_elem = element.find_element(By.CSS_SELECTOR, t_selector)
                            if title_elem and title_elem.text:
                                title = title_elem.text.strip()
                                break
                        except NoSuchElementException:
                            continue

                    # Múltiplos seletores para link
                    link = ""
                    link_selectors = ["a", ".yuRUbf a", "h3 a", "[href]"]
                    for l_selector in link_selectors:
                        try:
                            link_elem = element.find_element(By.CSS_SELECTOR, l_selector)
                            if link_elem:
                                link = link_elem.get_attribute("href")
                                if link and link.startswith("http"):
                                    break
                        except NoSuchElementException:
                            continue

                    # Múltiplos seletores para snippet
                    snippet = ""
                    snippet_selectors = [
                        ".VwiC3b",
                        "[data-sncf]",
                        ".s3v9rd",
                        ".st",
                        "[data-snhf]",
                    ]
                    for s_selector in snippet_selectors:
                        try:
                            snippet_elem = element.find_element(By.CSS_SELECTOR, s_selector)
                            if snippet_elem and snippet_elem.text:
                                snippet = snippet_elem.text.strip()
                                break
                        except NoSuchElementException:
                            continue

                    # Adicionar resultado se tiver título e link válidos
                    if title and link and not link.startswith("/search"):
                        results.append(
                            {
                                "position": i + 1,
                                "title": title,
                                "link": link,
                                "snippet": snippet or "Sem descrição",
                            }
                        )
                        logger.debug(f"Resultado {i + 1}: {title[:50]}...")

                except Exception as e:
                    logger.debug(f"Erro ao processar resultado {i + 1}: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Erro ao extrair resultados: {e}")

        logger.info(f"Total de resultados extraídos: {len(results)}")
        return results

    def automate_form_filling(self, form_data: Dict) -> Dict:
        """
        Automatizar preenchimento de formulário.

        Args:
            form_data: Dados para preenchimento

        Returns:
            Resultado da automação
        """
        logger.info("Automatizando preenchimento de formulário")
        start_time = time.time()

        try:
            # Navegar para página de exemplo
            self.driver.get("https://httpbin.org/forms/post")

            # Aguardar página carregar completamente
            time.sleep(2)

            # Aguardar formulário carregar
            self.wait.until(EC.presence_of_element_located((By.NAME, "custname")))

            logger.info("Formulário carregado, iniciando preenchimento...")

            # Preencher campos
            fields_filled = 0

            # Nome do cliente
            if "customer_name" in form_data:
                try:
                    name_field = self.driver.find_element(By.NAME, "custname")
                    name_field.clear()
                    name_field.send_keys(form_data["customer_name"])
                    fields_filled += 1
                    logger.debug("Campo 'nome' preenchido")
                except Exception as e:
                    logger.warning(f"Erro ao preencher nome: {e}")

            # Email
            if "email" in form_data:
                try:
                    email_field = self.driver.find_element(By.NAME, "custemail")
                    email_field.clear()
                    email_field.send_keys(form_data["email"])
                    fields_filled += 1
                    logger.debug("Campo 'email' preenchido")
                except Exception as e:
                    logger.warning(f"Erro ao preencher email: {e}")

            # Tamanho da pizza (radio button)
            if "pizza_size" in form_data:
                try:
                    size_radio = self.driver.find_element(
                        By.CSS_SELECTOR, f"input[value='{form_data['pizza_size']}']"
                    )
                    self.driver.execute_script("arguments[0].click();", size_radio)
                    fields_filled += 1
                    logger.debug(f"Tamanho de pizza '{form_data['pizza_size']}' selecionado")
                except Exception as e:
                    logger.warning(f"Erro ao selecionar tamanho da pizza: {e}")

            # Toppings (checkboxes)
            if "toppings" in form_data:
                for topping in form_data["toppings"]:
                    try:
                        topping_checkbox = self.driver.find_element(
                            By.CSS_SELECTOR, f"input[value='{topping}']"
                        )
                        if not topping_checkbox.is_selected():
                            self.driver.execute_script(
                                "arguments[0].click();", topping_checkbox
                            )
                            fields_filled += 1
                            logger.debug(f"Topping '{topping}' selecionado")
                    except NoSuchElementException:
                        logger.warning(f"Topping '{topping}' não encontrado")
                        continue

            # Comentários
            if "comments" in form_data:
                try:
                    comments_field = self.driver.find_element(By.NAME, "comments")
                    comments_field.clear()
                    comments_field.send_keys(form_data["comments"])
                    fields_filled += 1
                    logger.debug("Campo 'comentários' preenchido")
                except Exception as e:
                    logger.warning(f"Erro ao preencher comentários: {e}")

            # Aguardar um pouco antes de submeter
            time.sleep(1)

            # Submeter formulário - múltiplos seletores
            submit_success = False
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "input[value='Submit order']",
                "button:contains('Submit')",
                ".submit-btn",
                "[type='submit']",
            ]

            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        # Rolar até o botão para garantir que está visível
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", submit_button
                        )
                        time.sleep(0.5)

                        # Tentar clicar
                        self.driver.execute_script("arguments[0].click();", submit_button)
                        logger.info(f"Formulário submetido com seletor: {selector}")
                        submit_success = True
                        break
                except Exception as e:
                    logger.debug(f"Seletor '{selector}' falhou: {e}")
                    continue

            if not submit_success:
                # Última tentativa: pressionar Enter no último campo
                try:
                    comments_field = self.driver.find_element(By.NAME, "comments")
                    comments_field.send_keys(Keys.RETURN)
                    logger.info("Formulário submetido via Enter")
                    submit_success = True
                except Exception:
                    pass

            if not submit_success:
                raise Exception(
                    "Não foi possível submeter o formulário - botão submit não encontrado"
                )

            # Aguardar resposta - múltiplos seletores
            response_found = False
            response_selectors = [
                (By.TAG_NAME, "pre"),
                (By.CSS_SELECTOR, "pre"),
                (By.XPATH, "//pre"),
                (By.CSS_SELECTOR, ".response"),
                (By.CSS_SELECTOR, "[data-response]"),
            ]

            for by, selector in response_selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((by, selector)))
                    response_found = True
                    logger.info(f"Resposta encontrada com: {selector}")
                    break
                except TimeoutException:
                    continue

            if not response_found:
                logger.warning("Resposta não detectada, mas formulário foi submetido")

            execution_time = time.time() - start_time

            result = {
                "form_data": form_data,
                "fields_filled": fields_filled,
                "execution_time": round(execution_time, 3),
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }

            logger.success(
                "Formulário preenchido com sucesso",
                fields=fields_filled,
                time=f"{execution_time:.3f}s",
            )

            return result

        except Exception as e:
            logger.error(f"Erro no preenchimento: {e}")

            # Capturar screenshot para debug
            try:
                debug_screenshot = self.take_screenshot(
                    f"debug_form_error_{int(time.time())}.png"
                )
                logger.info(f"Screenshot de debug salvo: {debug_screenshot}")
            except BaseException:
                pass

            return {
                "form_data": form_data,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }

    def test_simple_form(self) -> Dict:
        """
        Testar automação com formulário mais simples.

        Returns:
            Resultado do teste
        """
        logger.info("Testando formulário simples")
        start_time = time.time()

        try:
            # Criar página HTML simples para teste
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Teste de Formulário</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .form-group { margin: 10px 0; }
                    label { display: block; margin-bottom: 5px; }
                    input, textarea, select { 
                        padding: 5px; 
                        margin-bottom: 10px; 
                        width: 200px; 
                    }
                    button { 
                        padding: 10px 20px; 
                        background-color: #007bff; 
                        color: white; 
                        border: none; 
                        border-radius: 4px; 
                        cursor: pointer; 
                    }
                </style>
            </head>
            <body>
                <h1>Formulário de Teste</h1>
                <form id="testForm">
                    <div class="form-group">
                        <label for="nome">Nome:</label>
                        <input type="text" id="nome" name="nome" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="idade">Idade:</label>
                        <input type="number" id="idade" name="idade" min="1" max="120">
                    </div>
                    <div class="form-group">
                        <label for="comentarios">Comentários:</label>
                        <textarea id="comentarios" name="comentarios" rows="4"></textarea>
                    </div>
                    <button type="submit" id="submitBtn">Enviar</button>
                </form>
                <div id="resultado" style="margin-top: 20px; display: none;">
                    <h2>Formulário enviado com sucesso!</h2>
                </div>
                <script>
                    document.getElementById('testForm').addEventListener(
                        'submit', function(e) {
                        e.preventDefault();
                        document.getElementById('resultado').style.display = 'block';
                    });
                </script>
            </body>
            </html>
            """

            # Salvar arquivo HTML temporário
            temp_file = Path("output") / "test_form.html"
            temp_file.parent.mkdir(exist_ok=True)

            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Navegar para o arquivo local
            file_url = f"file:///{temp_file.absolute().as_posix()}"
            self.driver.get(file_url)

            # Aguardar carregamento
            self.wait.until(EC.presence_of_element_located((By.ID, "nome")))

            logger.info("Formulário de teste carregado")

            # Preencher campos
            fields_filled = 0

            # Nome
            nome_field = self.driver.find_element(By.ID, "nome")
            nome_field.clear()
            nome_field.send_keys("João Automação")
            fields_filled += 1

            # Email
            email_field = self.driver.find_element(By.ID, "email")
            email_field.clear()
            email_field.send_keys("joao@teste.com")
            fields_filled += 1

            # Idade
            idade_field = self.driver.find_element(By.ID, "idade")
            idade_field.clear()
            idade_field.send_keys("25")
            fields_filled += 1

            # Comentários
            comments_field = self.driver.find_element(By.ID, "comentarios")
            comments_field.clear()
            comments_field.send_keys("Teste de automação com Selenium Python")
            fields_filled += 1

            # Submeter formulário
            submit_button = self.driver.find_element(By.ID, "submitBtn")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(0.5)
            submit_button.click()

            # Aguardar resultado aparecer
            self.wait.until(EC.visibility_of_element_located((By.ID, "resultado")))

            # Aguardar um pouco para ver o resultado
            time.sleep(2)

            execution_time = time.time() - start_time

            # Limpar arquivo temporário
            try:
                temp_file.unlink()
            except BaseException:
                pass

            result = {
                "test_type": "simple_form",
                "fields_filled": fields_filled,
                "execution_time": round(execution_time, 3),
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }

            logger.success(
                "Teste de formulário simples concluído",
                fields=fields_filled,
                time=f"{execution_time:.3f}s",
            )

            return result

        except Exception as e:
            logger.error(f"Erro no teste de formulário simples: {e}")

            return {
                "test_type": "simple_form",
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }

    def take_screenshot(self, filename: str = None) -> str:
        """
        Capturar screenshot da página atual.

        Args:
            filename: Nome do arquivo (opcional)

        Returns:
            Path do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        filepath = Path("output") / filename
        filepath.parent.mkdir(exist_ok=True)

        self.driver.save_screenshot(str(filepath))
        logger.info(f"Screenshot salvo: {filepath}")

        return str(filepath)

    def run_automation_suite(self) -> Dict:
        """Executar suite completa de automação."""
        logger.info("=== Iniciando suite de automação web ===")

        try:
            self.setup_driver()

            # Teste 1: Formulário simples (mais confiável)
            simple_form_result = self.test_simple_form()
            self.results.append(simple_form_result)

            # Teste 2: Pesquisa no Google (pode falhar devido a proteções
            # anti-bot)
            try:
                search_result = self.search_google("Python automation selenium")
                self.results.append(search_result)
            except Exception as e:
                logger.warning(f"Teste de pesquisa Google pulado: {e}")
                self.results.append(
                    {
                        "query": "Python automation selenium",
                        "error": f"Pulado devido a proteções anti-bot: {str(e)}",
                        "success": False,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            # Teste 3: Preenchimento de formulário externo (httpbin.org)
            try:
                form_data = {
                    "customer_name": "Teste Automação",
                    "email": "teste@automation.com",
                    "pizza_size": "large",
                    "toppings": ["bacon", "cheese"],
                    "comments": "Pedido de teste via automação Python",
                }

                form_result = self.automate_form_filling(form_data)
                self.results.append(form_result)
            except Exception as e:
                logger.warning(f"Teste de formulário externo pulado: {e}")
                self.results.append(
                    {
                        "form_data": "httpbin.org test",
                        "error": f"Site externo indisponível: {str(e)}",
                        "success": False,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            # Capturar screenshot final
            screenshot_path = self.take_screenshot("automation_final.png")

            # Salvar resultados
            self._save_results()

            # Calcular estatísticas
            total_tests = len(self.results)
            successful_tests = sum(1 for r in self.results if r.get("success", False))
            success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0

            logger.success("=== Suite de automação concluída ===")
            logger.info(
                f"Taxa de sucesso: {success_rate:.1f}% ({successful_tests}/{total_tests})"
            )

            return {
                "success": True,
                "results": self.results,
                "screenshot": screenshot_path,
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": round(success_rate, 1),
            }

        except Exception as e:
            logger.error(f"Erro na suite de automação: {e}")

            return {"success": False, "error": str(e), "results": self.results}

        finally:
            self.cleanup()

    def _save_results(self) -> None:
        """Salvar resultados em arquivo JSON."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"selenium_results_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "browser": self.browser,
                        "headless": self.headless,
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

        logger.info(f"Resultados salvos: {filename}")

    def cleanup(self) -> None:
        """Limpeza de recursos."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver fechado")
            except Exception as e:
                logger.warning(f"Erro ao fechar WebDriver: {e}")


def main():
    """Função principal."""
    print("🚀 INICIANDO AUTOMAÇÃO WEB COM SELENIUM")
    print("=" * 50)

    # Executar automação
    automation = WebAutomation(browser="chrome", headless=True)
    result = automation.run_automation_suite()

    # Mostrar resultado
    print("\n" + "=" * 50)
    if result["success"]:
        print("✅ [SUCESSO] Automação web concluída!")
        print(f"📊 Testes executados: {result['total_tests']}")
        print(f"✔️  Sucessos: {result['successful_tests']}")
        falhas = result["total_tests"] - result["successful_tests"]
        print(f"❌ Falhas: {falhas}")
        print(f"📈 Taxa de sucesso: {result['success_rate']}%")
        print(f"📸 Screenshot: {result['screenshot']}")

        # Detalhar resultados
        print("\n📋 DETALHES DOS TESTES:")
        print("-" * 30)
        for i, test_result in enumerate(result["results"], 1):
            status = "✅ PASSOU" if test_result.get("success", False) else "❌ FALHOU"
            test_name = test_result.get("test_type", test_result.get("query", "Formulário"))

            print(f"{i}. {test_name}: {status}")

            if test_result.get("success", False):
                if "execution_time" in test_result:
                    print(f"   ⏱️  Tempo: {test_result['execution_time']}s")
                if "results_count" in test_result:
                    print(f"   📄 Resultados encontrados: {test_result['results_count']}")
                if "fields_filled" in test_result:
                    print(f"   📝 Campos preenchidos: {test_result['fields_filled']}")
            else:
                error_msg = test_result.get("error", "Erro desconhecido")
                if len(error_msg) > 80:
                    error_msg = error_msg[:77] + "..."
                print(f"   ❌ Erro: {error_msg}")

        resumo = f"{result['successful_tests']} de {result['total_tests']} testes passaram!"
        print(f"\n🎯 RESUMO: {resumo}")

    else:
        print(f"❌ [ERRO] Falha na automação: {result.get('error')}")
        if result.get("results"):
            print(f"📊 Testes parciais executados: {len(result['results'])}")

    print("=" * 50)


if __name__ == "__main__":
    main()
