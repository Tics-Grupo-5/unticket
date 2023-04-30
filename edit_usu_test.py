import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.roles as roles
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

USERNAMES = []
ROLES = ['Administrador']
NOMBRES = []
APELLIDOS = []
TIPOS_DOC = []
NUMS_DOC = []
CAMBIOS_ESTADO = []
ROLES_PERSONA = []

def edit_usu_test(driver, DF, caso, username, rol, nombres, apellidos, tipo_doc, num_doc, cambio_estado, roles):

    UAC = 3
    passed = 0

    FUNC_STR = 'Editar Usuario'
    PARAMS_STR = f'Nombres: {nombres}\nApellidos: {apellidos}\nTipo Doc: {tipo_doc}\nNum Doc: {num_doc}\nCambio Estado: {cambio_estado}\nRoles: {roles}'

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

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El rol seleccionado se mantiene tras enviar el formulario', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] El usuario se guarda con los datos correctos
        shared.search(driver, 'Usuarios', username)
        result = shared.UAC_validate_saved_record(driver, 'Usuarios', [username, ' '.join(roles)], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El usuario se guarda con los datos correctos', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Los datos del usuario aparecen correctamente en el modo edición
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
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los datos del usuario aparecen correctamente en el modo edición', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'EDIT USU: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":
    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 35 # suma de todos los time sleep en la función

    for i in range(nexp):

        username = USERNAMES[i]
        rol = ROLES[i]
        nombres = NOMBRES[i]
        apellidos = APELLIDOS[i]
        tipo_doc = TIPOS_DOC[i]
        num_doc = NUMS_DOC[i]
        cambio_estado = CAMBIOS_ESTADO[i]
        roles_ = ROLES_PERSONA[i]

        DF = edit_usu_test(driver, DF, caso=i+1, username=username, rol=rol, nombres=nombres, apellidos=apellidos, tipo_doc=tipo_doc, num_doc=num_doc, cambio_estado=cambio_estado, roles=roles_)

        iteration_time = time.time() - start_time - total_time
        total_time += iteration_time

        print(f"Caso {i+1} tomó: {datetime.timedelta(seconds=iteration_time)}")
        print(f"Caso {i+1} sin espera tomó aprox.: {datetime.timedelta(seconds=iteration_time - wait)}")

    avg_time_per_iteration = total_time / nexp
    total_time = time.time() - start_time

    print('\n\n\n')
    print(f"Tiempo promedio por caso: {datetime.timedelta(seconds=avg_time_per_iteration)}")
    print(f"Tiempo promedio aprox. por caso sin espera: {datetime.timedelta(seconds=avg_time_per_iteration - wait)}") 
    print(f"Tiempo total para {nexp} casos: {datetime.timedelta(seconds=total_time)}")
    print(f"Tiempo total aprox. para {nexp} casos sin espera: {datetime.timedelta(seconds=total_time - wait * nexp)}")

    DF.to_excel(r'results\edit_usu_test_results.xlsx', index=False)

    '''
    edit_usu_test(driver, username='alicia642e68b8', rol='Administrador', nombres='Alice', apellidos='Smith', tipo_doc='C.C.', num_doc='1680763064', cambio_estado=True, roles=roles.get_roles(4))
    '''