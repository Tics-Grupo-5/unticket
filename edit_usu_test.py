import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.roles as roles

def edit_usu_test(driver, username, nombres, apellidos, tipo_doc, num_doc, cambio_estado, roles):

    UAC = 1
    passed = 0

    try:

        shared.select_module(driver, 'Administrar usuarios')
        time.sleep(10)

        shared.search(driver, 'Usuarios', username)

        shared.click_edit_button(driver, 'Usuarios', 0, pos=1)

        time.sleep(5)

        shared.enter_input_value(driver, 'Nombres', nombres)
        shared.enter_input_value(driver, 'Apellidos', apellidos)
        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Documento', num_doc)

        if cambio_estado:
            shared.click_checkbox(driver, 'Estado')

        shared.multiselect_values(driver, 'Roles', roles)
        shared.press_esc_key(driver)


        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)
        shared.search(driver, 'Usuarios', username)

        result = shared.UAC_validate_saved_record(driver, 'Usuarios', [username, ' '.join(roles)], 0)
        passed += shared.evaluate_UAC_result(result)

        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Administrador')
    time.sleep(5)
    edit_usu_test(driver, username='alicia642e68b8', nombres='Alice', apellidos='Smith', tipo_doc='C.C.', num_doc='1680763064', cambio_estado=True, roles=roles.get_roles(4))