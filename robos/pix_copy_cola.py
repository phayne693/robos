 # from more_itertools import numeric_range
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import glob
import requests
import subprocess
import clipboard
from dotenv import load_dotenv
load_dotenv()

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
options.add_argument("--disk-cache-dir=/home/jeferson/Área de Trabalho/roboPix")
options.add_argument("--disk-cache-size=104857600")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable_images")
options.add_experimental_option("prefs", {
    "donwload.default.directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"
})
prefs = {"download.default_directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"}
opt = webdriver.ChromeOptions()
# opt.add_argument('--headless')
opt.add_experimental_option("prefs", prefs)


def pix_copia_cola(chave_copia_cola):
    try:   
        login_env = os.getenv("LOGIN")
        senha_env = os.getenv("SENHA")
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://app.norwaydigital.com.br/auth/signin')
        time.sleep(4)
        # inserir login
        login = navegador.find_element(By.XPATH, '//*[@id="text"]')
        login.send_keys(login_env)
        # senha
        procurarSenha = navegador.find_element(By.XPATH, '//*[@id="teste"]')
        numerosBtn = procurarSenha.find_elements(By.TAG_NAME, 'button')
        senha = [int(digito) for digito in senha_env]
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
            try:
                saldo = response.json()
                print(f'Saldo: {saldo}')
                valor_minimo = 0.01
                if saldo > valor_minimo:
                    #click pagar
                    pagar = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/ul/label[3]/div'))
                    )
                    pagar.click()
                    time.sleep(2)
                    #click copia e cola
                    copy_cola = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/div/div[2]/div'))
                    )
                    copy_cola.click()
                    #digitar copia e cola
                    input_copy_cola = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/form/div/input'))
                    )
                    input_copy_cola.click()
                    #copia a variavel
                    clipboard.copy(chave_copia_cola)
                    #simula ctrl+v e envia a chave
                    ActionChains(navegador).key_down(Keys.CONTROL).send_keys('v').perform()
                    ActionChains(navegador).key_up(Keys.CONTROL)
                    time.sleep(2)
                    #click confirmar
                    confirmar = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/button'))
                    )
                    confirmar.click()
                    time.sleep(1)
                    #confirmar 2
                    confirmar_dois = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="single-spa-application:@infinity/navigation"]/div/div[2]/div[2]/div/div/div/div/div/section/p[2]/button[2]'))
                    )
                    confirmar_dois.click()
                    time.sleep(2)
                    navegador.quit()
                    return 'Pix copia e cola realizado!'
                else:
                    navegador.quit()
                    return {'error':'Saldo insuficiente.'}
            except WebDriverException as e:
                navegador.quit()
                return {'error' : str(e)}
        else:
            navegador.quit()
            return {'code' : response.status_code, 'error': response.text.json()}
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}

    


