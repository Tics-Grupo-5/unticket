import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.roles as roles

def edit_usu_test(driver, username, rol, nombres, apellidos, tipo_doc, num_doc, cambio_estado, roles):

    UAC = 3
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Administrar usuarios')
        time.sleep(10)

        shared.search(driver, 'Usuarios', username)

        shared.click_edit_button(driver, 'Usuarios', 0, pos=0)

        time.sleep(5)

        shared.enter_input_value(driver, 'Nombres', nombres)
        shared.enter_input_value(driver, 'Apellidos', apellidos)
        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Documento', num_doc)

        estado = shared.get_checkbox_value(driver, 'Estado') 
        if cambio_estado:
            shared.click_checkbox(driver, 'Estado')
            estado = not estado

        shared.multiselect_values(driver, 'Roles', roles)
        shared.press_esc_key(driver)


        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)

        # El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)

        shared.search(driver, 'Usuarios', username)

        result = shared.UAC_validate_saved_record(driver, 'Usuarios', [username, ' '.join(roles)], 0)
        passed += shared.evaluate_UAC_result(result)

            # Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Usuarios', 0, pos=0) 

        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Nombres'),
                                                shared.get_input_value(driver, 'Apellidos'),
                                                shared.get_input_value(driver, 'Tipo de documento'),
                                                shared.get_input_value(driver, 'Documento'),
                                                shared.get_checkbox_value(driver, 'Estado'),
                                                sorted(shared.get_multiselect_values(driver, 'Roles')),
                                                ], [nombres, apellidos, tipo_doc, num_doc, estado, sorted(roles)])
        passed += shared.evaluate_UAC_result(result)
        shared.click_button(driver, 'Cerrar', 1)

        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    edit_usu_test(driver, username='alicia642e68b8', rol='Administrador', nombres='Alice', apellidos='Smith', tipo_doc='C.C.', num_doc='1680763064', cambio_estado=True, roles=roles.get_roles(4))