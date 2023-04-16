import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import traceback

def aggr_usu_test(driver, rol, username, nombres, apellidos, tipo_doc, num_doc, roles):

    UAC = 4
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Administrar usuarios')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(2)
        shared.enter_input_value(driver, 'Username', username)
        shared.enter_input_value(driver, 'Nombres', nombres)
        shared.enter_input_value(driver, 'Apellidos', apellidos)
        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Documento', num_doc)
        shared.multiselect_values(driver, 'Roles', roles)
        shared.press_esc_key(driver)
        shared.click_button(driver, 'Guardar')
        time.sleep(5)

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El sistema no permite guardar dos usuarios con el mismo username o documento
        shared.search(driver, 'Usuarios', username)
        result = shared.UAC_check_unique_record(driver, 'Usuarios', username)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El usuario se guarda con los datos correctos
        result = shared.UAC_validate_saved_record(driver, 'Usuarios', [username, ' '.join(roles)], 0)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] Los datos del usuario aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Usuarios', 0, pos=0)   
        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Username'),
                                                shared.get_input_value(driver, 'Nombres'),
                                                shared.get_input_value(driver, 'Apellidos'),
                                                shared.get_input_value(driver, 'Tipo de documento'),
                                                shared.get_input_value(driver, 'Documento'),
                                                shared.get_checkbox_value(driver, 'Estado'),
                                                sorted(shared.get_multiselect_values(driver, 'Roles'))
                                                ], [username, nombres, apellidos, tipo_doc, num_doc, True, sorted(roles)])
        passed += shared.evaluate_UAC_result(result)
        shared.click_button(driver, 'Cerrar', 1)
        # END UAC CHECK

        print(f'AGGR USU: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'AGGR USU: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    aggr_usu_test(driver, rol='Administrador', username=f'alicia{id.get_id()}', nombres='Alicia', apellidos='Smith', tipo_doc='C.C.', num_doc=f'{id.get_id_()}', roles=['Solicitante', 'Recepción'])
    