; ===============================================================================
; Script AutoIt Original - Automação de Janelas
; Funcionalidade: Automatiza interações com aplicações Windows
; Problema: Difícil manutenção, sem testes, documentação limitada
; ===============================================================================

#include <MsgBoxConstants.au3>
#include <FileConstants.au3>
#include <WinAPIFiles.au3>

; Configurações globais
Global $APP_TITLE = "Calculadora"
Global $TIMEOUT = 5000
Global $LOG_FILE = @ScriptDir & "\automation.log"

; Função principal
Main()

Func Main()
    ; Inicializar log
    WriteLog("=== Iniciando automação de calculadora ===")
    
    ; Abrir calculadora
    If Not OpenCalculator() Then
        WriteLog("ERRO: Falha ao abrir calculadora")
        Exit 1
    EndIf
    
    ; Aguardar janela aparecer
    WinWaitActive($APP_TITLE, "", $TIMEOUT)
    If @error Then
        WriteLog("ERRO: Timeout aguardando calculadora")
        Exit 1
    EndIf
    
    ; Realizar cálculos
    PerformCalculations()
    
    ; Salvar resultado
    SaveResult()
    
    ; Fechar aplicação
    CloseCalculator()
    
    WriteLog("=== Automação concluída com sucesso ===")
EndFunc

Func OpenCalculator()
    WriteLog("Abrindo calculadora...")
    
    ; Tentar via Run
    Run("calc.exe")
    Sleep(2000)
    
    ; Verificar se abriu
    If WinExists($APP_TITLE) Then
        WriteLog("Calculadora aberta com sucesso")
        Return True
    Else
        ; Tentar método alternativo
        ShellExecute("calc")
        Sleep(2000)
        
        If WinExists($APP_TITLE) Then
            WriteLog("Calculadora aberta via ShellExecute")
            Return True
        EndIf
    EndIf
    
    Return False
EndFunc

Func PerformCalculations()
    WriteLog("Iniciando cálculos...")
    
    ; Focar na janela
    WinActivate($APP_TITLE)
    
    ; Limpar calculadora
    Send("{ESC}")
    Sleep(500)
    
    ; Cálculo 1: 123 + 456
    WriteLog("Calculando: 123 + 456")
    Send("123{+}456{=}")
    Sleep(1000)
    
    ; Capturar resultado (simulado)
    Local $result1 = GetCalculatorResult()
    WriteLog("Resultado 1: " & $result1)
    
    ; Limpar para próximo cálculo
    Send("{ESC}")
    Sleep(500)
    
    ; Cálculo 2: 789 * 12
    WriteLog("Calculando: 789 * 12")
    Send("789{*}12{=}")
    Sleep(1000)
    
    Local $result2 = GetCalculatorResult()
    WriteLog("Resultado 2: " & $result2)
    
    ; Salvar resultados em arquivo
    Local $results = $result1 & @CRLF & $result2
    FileWrite(@ScriptDir & "\results.txt", $results)
EndFunc

Func GetCalculatorResult()
    ; Simula captura de resultado da calculadora
    ; Em implementação real, usaria OCR ou análise de imagem
    
    ; Copiar resultado para clipboard
    Send("^c")
    Sleep(200)
    
    Local $result = ClipGet()
    If @error Then
        WriteLog("ERRO: Falha ao capturar resultado")
        Return "ERRO"
    EndIf
    
    Return $result
EndFunc

Func SaveResult()
    WriteLog("Salvando resultados...")
    
    ; Criar relatório detalhado
    Local $report = ""
    $report &= "=== RELATÓRIO DE AUTOMAÇÃO ===" & @CRLF
    $report &= "Data: " & @YEAR & "/" & @MON & "/" & @MDAY & @CRLF
    $report &= "Hora: " & @HOUR & ":" & @MIN & ":" & @SEC & @CRLF
    $report &= "Status: Sucesso" & @CRLF
    $report &= "==============================" & @CRLF
    
    ; Salvar em múltiplos formatos
    FileWrite(@ScriptDir & "\report.txt", $report)
    
    ; Enviar por email (simulado)
    WriteLog("Enviando relatório por email...")
    ; EmailSend() - função customizada não implementada
    
    WriteLog("Resultados salvos com sucesso")
EndFunc

Func CloseCalculator()
    WriteLog("Fechando calculadora...")
    
    If WinExists($APP_TITLE) Then
        WinClose($APP_TITLE)
        
        ; Aguardar fechamento
        WinWaitClose($APP_TITLE, "", 3000)
        
        If @error Then
            WriteLog("Forçando fechamento...")
            WinKill($APP_TITLE)
        EndIf
    EndIf
    
    WriteLog("Calculadora fechada")
EndFunc

Func WriteLog($message)
    Local $timestamp = @YEAR & "-" & @MON & "-" & @MDAY & " " & @HOUR & ":" & @MIN & ":" & @SEC
    Local $logEntry = "[" & $timestamp & "] " & $message & @CRLF
    
    ; Escrever no console
    ConsoleWrite($logEntry)
    
    ; Escrever no arquivo
    FileWrite($LOG_FILE, $logEntry)
EndFunc

; Tratamento de erros global
Func ErrorHandler()
    WriteLog("ERRO CRÍTICO: " & @error)
    
    ; Limpar recursos
    If WinExists($APP_TITLE) Then
        WinKill($APP_TITLE)
    EndIf
    
    ; Salvar log de erro
    FileWrite(@ScriptDir & "\error.log", "Erro em: " & @ScriptLineNumber)
    
    Exit @error
EndFunc

; Configurar tratamento de erro
OnAutoItExitRegister("ErrorHandler") 