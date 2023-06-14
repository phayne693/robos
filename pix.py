 # from more_itertools import numeric_range
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import glob
from selenium.common.exceptions import ElementClickInterceptedException
import requests

# def bevi_download():
# definindo opcoes para o navegador
options = Options()
options.add_argument('--disabel-blink-features=AutomationControlled')
options.add_experimental_option("UseAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# iniciando o servico
page = Service(ChromeDriverManager().install())
# localizacao falsa
location = '{"latitude": -23.5102, "logitude": -46.6590}'
# defininso as ocnfiguracoes do navegador
options.add_argument(f"--geolocation={location}")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_experimental_option("prefs", {
    "donwload.default.directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"
})
prefs = {"download.default_directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"}
opt = webdriver.ChromeOptions()
opt.add_argument('--headless')
opt.add_experimental_option("prefs", prefs)


def robo_pix(chave_cpf, valor):
    navegador = webdriver.Chrome(service=page, options=opt)
    navegador.get('https://app.norwaydigital.com.br/auth/signin')
    time.sleep(3)

    # inserir login
    login = navegador.find_element(By.XPATH, '//*[@id="text"]')
    login.send_keys('thiago@teraidc.com.br')
    # senha
    procurarSenha = navegador.find_element(By.XPATH, '//*[@id="teste"]')
    numerosBtn = procurarSenha.find_elements(By.TAG_NAME, 'button')
    senha = [1, 1, 2, 0, 2, 2]
    listaBtn = [button.get_attribute('textContent').replace(
        'ou', '') for button in numerosBtn]
    # print(listaBtn)
    while len(senha) != 0:
        for n in senha:
            for i, botao in enumerate(listaBtn):
                if str(senha[0]) in botao:
                    numerosBtn[i].click()
                    senha.remove(senha[0])
                    time.sleep(1)
                    break
    # click entrar
    time.sleep(1)
    acessar = navegador.find_element(
        By.XPATH, '//*[@id="single-spa-application:@infinity/auth"]/body/section/section[1]/form/button')
    acessar.click()
    time.sleep(2)
    #click MENU
    hamburguer = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="burguerButton"]')))
    hamburguer.click()
    time.sleep(1)
    #click PIX
    menu_pix = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="MenuWrapperId"]/a[3]')))
    menu_pix.click()
    time.sleep(2)
    #verifica saldo
    url = 'https://api.norwaydigital.com.br/prod/v1/balances/user/01FPDE2NKM2KANZP877E31AR2G'

    response = requests.get(url)
    if response.status_code == 200:
        saldo = response.json()
        print(saldo)
    else:
        print(response.status_code)

    #faz o pix se tiver saldo maior que 0.01
    valor_minimo = 0.01
    if saldo > valor_minimo:
        #click TRANSFERIR
        transferir = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/ul/label[4]/div')))
        transferir.click()
        #click CHAVE PIX
        chave_pix = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div[2]/button[1]')))
        chave_pix.click()
        time.sleep(1)
        #insere CHAVE
        #chave_cpf = 43996081880
        chave = navegador.find_element(By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/form/input')
        chave.send_keys(chave_cpf)
        time.sleep(1)
        #click avancar
        avancar = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/p[2]/button[2]'))
        )
        avancar.click()
        time.sleep(1)
        #digitar VALOR
        #valor = '0,01'
        inserir_valor = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/div[1]/input'))
        )
        ActionChains(navegador).move_to_element(inserir_valor).double_click().perform()
        time.sleep(1)
        inserir_valor.send_keys(valor)
        #confirmar
        confirmar = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/div[5]/button[2]'))
        )
        confirmar.click()
        time.sleep(1)
        #confirma nome destinatario
        destinatario = 'Jeferson Queiroz Lemes'
        nome_elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/div[2]/div[1]/div[2]/span[2]'))
        )
        nome = nome_elemento.text
        print(nome)
        if nome == destinatario:
            enviar = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/p[2]/button[2]'))
            )
            enviar.click()
            time.sleep(1)
            #finalizar
            finalizar = WebDriverWait(navegador, 10).until(
                EC. presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/p[2]/button'))
            )
            finalizar.click()
            return 'Pix realizado!'
        else:
            return 'Nome divergente.'
    else:
        return "Saldo insuficiente."
    pass
