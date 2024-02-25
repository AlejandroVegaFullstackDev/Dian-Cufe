from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json
import time

options = Options()

options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://catalogo-vpfe.dian.gov.co/User/SearchDocument")

with open('cufes.json') as f:
    data = json.load(f)
    cufes = data['cufes']

for cufe in cufes:
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DocumentKey"]')))
        label_dian = driver.find_element(By.XPATH, '//*[@id="DocumentKey"]')
        label_dian.click() 
        label_dian.clear() 
        label_dian.send_keys(cufe)  
        label_dian.send_keys(Keys.ENTER)  

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/p')))
        rows = driver.find_elements(By.XPATH, '//table[@class="documents-table table table-striped table-hover align-middle margin-bottom-0"]/tbody/tr')
        elementos = driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[3]/p/a')
        enlaces = [elemento.get_attribute('href') for elemento in elementos]
        print(enlaces)

        for row in rows:
            event_code_cell = row.find_element(By.XPATH, './td[1]')
            nombre_event_name = row.find_element(By.XPATH, './td[2]')
            nit_emisor_cell = row.find_element(By.XPATH, './td[4]')
            nombre_emisor_cell = row.find_element(By.XPATH, './td[5]')
            nit_receptor_cell = row.find_element(By.XPATH, './td[6]')
            nombre_receptor_cell = row.find_element(By.XPATH, './td[7]')
            
            if event_code_cell.text and nombre_event_name.text and nit_emisor_cell.text and nombre_emisor_cell.text and nit_receptor_cell.text and nombre_receptor_cell.text:
                print("Código del Evento:", event_code_cell.text)
                print("Nombre del Evento:", nombre_event_name.text)
                print("NIT Emisor:", nit_emisor_cell.text)
                print("Nombre Emisor:", nombre_emisor_cell.text)
                print("NIT Receptor:", nit_receptor_cell.text)
                print("Nombre Receptor:", nombre_receptor_cell.text)

    except TimeoutException:
        print(f"El ID {cufe} no es válido: no se pudo interactuar con el elemento en el tiempo esperado.")
        continue

    time.sleep(2)

driver.close()
