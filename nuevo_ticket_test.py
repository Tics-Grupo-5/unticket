import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def nuevo_ticket_test(driver, programa, certificado, observaciones, digital, num_consig=None, tipo_pago=None):

    UAC = 1
    passed = 0

    try:

        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(2)
        shared.select_value(driver, 'Programa', programa)
        shared.select_value(driver, 'Certificado', certificado)
        shared.enter_textarea_value(driver, 'Observaciones', observaciones)
        if digital:
            shared.click_checkbox(driver, '¡Quiero que mi certificado sea digital!')
        shared.click_button(driver, 'Continuar')
        time.sleep(2)
        shared.click_button(driver, 'Continuar', 1)
        time.sleep(2)
        shared.click_link(driver, 'Pagar')
        time.sleep(2)
        shared.switch_to_window(driver, 1)

        result = shared.UAC_check_current_url(driver, 'pago-virtual')
        passed += shared.evaluate_UAC_result(result)

        driver.close()

        shared.switch_to_window(driver, 0)

        shared.enter_input_value(driver, 'Número de consignación', num_consig) # spelling error
        shared.enter_input_value(driver, 'Soporte de pago', os.path.abspath(r'utils\files\soporte.pdf'), mode=1)
        shared.select_value(driver, 'Tipo de pago', tipo_pago)

        shared.click_button(driver, 'Terminar')

        # CHECK TICKET CREADO: LA TABLA NO ESTÁ ORDENADA, CÓMO VERIFICAR (?)

        print(f'NUEVO TICKET: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'NUEVO TICKET: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Solicitante')
    time.sleep(5)
    nuevo_ticket_test(driver, programa='Ingeniería Agrícola', certificado='Mi Certificado', 
                      observaciones='Lorem ipsum dolor sit amet, consectetur adipiscing elit', 
                      digital=True, num_consig='2023000', tipo_pago='Banco')
