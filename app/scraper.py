import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

def scrape_info(cufes):
    options = Options()
    options.add_argument("--incognito")
    #options.add_argument('--headless')
    #options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    result = {} 

    for cufe in cufes:
        cufe_info = {
            "events": [],
            "sellerInformation": {},
            "receiverInformation": {},
            "linkGraphicRepresentation": ""
        }
        intentos = 0

        while True:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            try:
                print(f"Procesando el cufe: {cufe}")
                driver.get("https://catalogo-vpfe.dian.gov.co/User/SearchDocument")
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DocumentKey"]')))
                
                label_dian = driver.find_element(By.XPATH, '//*[@id="DocumentKey"]')
                label_dian.click() 
                label_dian.clear() 
                label_dian.send_keys(cufe)  
                label_dian.send_keys(Keys.ENTER)  

                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/p')))
                
                error_span = driver.find_elements(By.XPATH, '//*[@id="search-document-form"]/div/span[@data-valmsg-for="DocumentKey" and contains(text(), "Recaptcha inválido")]')
                
                if error_span:
                    print("Recaptcha inválido.")
                    
                    if intentos >= 1:
                        print("Intentos excedidos. Abriendo nueva ventana de incógnito.")
                        driver.quit()
                        intentos = 0
                        continue  
                    else:
                        print("Volviendo a intentar después de 2 segundos.")
                        time.sleep(2)
                        label_dian.send_keys(Keys.ENTER)

                def find_table_rows(driver):
                    return driver.find_elements(By.XPATH, '//table[@class="documents-table table table-striped table-hover align-middle margin-bottom-0"]/tbody/tr')

                def find_element_links(driver):
                    return driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[3]/p/a')

                def extract_element_attributes(element_list, attribute):
                    return [element.get_attribute(attribute) for element in element_list]

                rows = find_table_rows(driver)
                elementos = find_element_links(driver)
                enlaces = extract_element_attributes(elementos, 'href')

                for row in rows:
                    def extract_cell_text(row, xpath):
                        return row.find_element(By.XPATH, xpath).text

                    event_code_cell = extract_cell_text(row, './td[1]')
                    nombre_event_name = extract_cell_text(row, './td[2]')
                    nit_emisor_cell = extract_cell_text(row, '//*[@id="container1"]/div[2]/table/tbody/tr[1]/td[4]')
                    nombre_emisor_cell = extract_cell_text(row, '//*[@id="container1"]/div[2]/table/tbody/tr[1]/td[5]')
                    nit_receptor_cell = extract_cell_text(row, '//*[@id="container1"]/div[2]/table/tbody/tr[1]/td[7]')
                    nombre_receptor_cell = extract_cell_text(row, '/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[6]/div[2]/table/tbody/tr[1]/td[7]')

                    if all([event_code_cell, nombre_event_name, nit_emisor_cell, nombre_emisor_cell, nit_receptor_cell, nombre_receptor_cell]):
                        cufe_info["events"].append({
                            "eventNumber": event_code_cell,
                            "eventName": nombre_event_name
                        })

                    cufe_info["sellerInformation"] = {
                        "Document": nit_emisor_cell,
                        "Name": nombre_emisor_cell
                    }

                    cufe_info["receiverInformation"] = {
                        "Document": nit_receptor_cell,
                        "Name": nombre_receptor_cell
                    }

                    cufe_info["linkGraphicRepresentation"] = enlaces[0] if enlaces else ""

                result[cufe] = cufe_info

                driver.find_element(By.XPATH, '//*[@id="content-container"]/div[2]/a').click()
                print(f"El ID {cufe} es válido: se encontró la información.")
                break  
            except TimeoutException:
                print(f"El ID {cufe} no es válido: revise si es correcto. " )
                continue

        time.sleep(2)

    driver.quit()
    return result
