import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def edit_sol_test(driver, id, estado, encargado, rol, nota):

    UAC = 1
    passed = 0

    try:

        shared.select_module(driver, 'Solicitudes')
        time.sleep(10)

        shared.search(driver, 'Solicitudes', id)

        shared.click_edit_button(driver, 'Solicitudes', 0)

        time.sleep(5)

        shared.select_value(driver, 'Estado', estado)
        time.sleep(1)
        shared.select_value(driver, 'Encargado', encargado)
        time.sleep(1)
        shared.select_value(driver, 'Rol', rol)
        shared.enter_textarea_value(driver, 'Nota', nota)

        if estado == 'Elaborado':
            shared.enter_input_value(driver, 'Certificado digital', os.path.abspath(r'utils\files\certificado.pdf'), mode=1)

        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)
        shared.search(driver, 'Solicitudes', id)

        result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, estado, encargado], 0)
        passed += shared.evaluate_UAC_result(result)

        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Administrador')
    time.sleep(5)
    edit_sol_test(driver, id='1508', estado='Elaborado', encargado='Cristian Camilo', rol='Administrador', nota='nota')