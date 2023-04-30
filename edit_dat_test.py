import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import lib.edit_dat_lib as edit_dat
import utils.datetime_id as id
import os
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

ROLES = ['Solicitante']
PROGRAM_ACTIONS = []
TIPOS_DOC = []
NUMS_DOC = []
PROGRAMS_DATA = []

def edit_dat_test(driver, DF, caso, rol, program_action, tipo_doc, num_doc, program_data=None):

    UAC = 2
    passed = 0

    FUNC_STR = 'Editar Datos'
    PARAMS_STR = f'Program Action: {program_action}\nTipo Doc: {tipo_doc}\nNum Doc: {num_doc}\nProgram Data: {program_data}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Mis datos')

        shared.click_button(driver, 'Modificar')

        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Número', num_doc)

        if program_action == 1:
            shared.click_button(driver, 'Agregar')
            shared.select_value(driver, 'Estado solicitante', program_data[1])
            shared.select_value(driver, 'Programa', program_data[0], strict=True)

            if program_data[1] != 'Estudiante Activo':
                shared.set_date_field_value(driver, 0, 'Año de grado / Año de retiro', program_data[2])

            shared.click_button(driver, 'Guardar', 1)

        elif program_action == 2:
            edit_dat.see_all_programs(driver)
            edit_dat.open_edit_program_modal(driver, program_data[0])
            shared.select_value(driver, 'Estado solicitante', program_data[1])
            # we cannot select program when editing
            # shared.select_value(driver, 'Programa', program_data[0], strict=True)

            if program_data[1] != 'Estudiante Activo':
                shared.set_date_field_value(driver, 0, 'Año de grado / Año de retiro', program_data[2])

            shared.click_button(driver, 'Guardar', 1)

        elif program_action == 3:
            edit_dat.see_all_programs(driver)
            edit_dat.open_delete_program_modal(driver, program_data[0])
            shared.click_button(driver, 'Eliminar')

        time.sleep(2)
        shared.click_button(driver, 'Guardar')

        time.sleep(10)

        # [UAC] Los datos se guardan correctamente
        results = []
        results.append(shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Tipo de documento'),
                                                shared.get_input_value(driver, 'Número')
                                                ], [tipo_doc, num_doc]))
        if program_action == 1:
            results.append(edit_dat.UAC_check_if_program_was_added(driver, program_data[0]))
        elif program_action == 2:
            results.append(edit_dat.UAC_check_if_program_was_edited(driver, program_data))
        elif program_action == 3:
            results.append(edit_dat.UAC_check_if_program_was_deleted(driver, program_data[0]))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los datos se guardan correctamente', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK

        # [UAC] Los programas seleccionados están disponibles en el formulario de NUEVO TICKET
        expected_programs = edit_dat.get_all_programs(driver)
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(5)
        visible_programs = shared.get_select_dropdown_values(driver, 'Programa')
        shared.press_esc_key(driver)
        result = shared.UAC_check_two_lists(visible_programs, expected_programs)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los programas seleccionados están disponibles en el formulario de NUEVO TICKET', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'EDIT DAT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'EDIT DAT: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 22 # suma de todos los time sleep en la función

    for i in range(nexp):

        rol = random.choice(ROLES)
        program_action = PROGRAM_ACTIONS[i]
        tipo_doc = random.choice(TIPOS_DOC)
        num_doc = random.choice(NUMS_DOC)
        program_data = PROGRAMS_DATA[i]

        DF = edit_dat_test(driver, DF, caso=i+1, rol=rol, program_action=program_action, tipo_doc=tipo_doc, num_doc=num_doc, program_data=program_action)

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

    DF.to_excel(r'results\edit_dat_test_results.xlsx', index=False)

    '''
    # 0 : nothing
    # 1 : add : cannot add already added program
    # 2 : edit
    # 3 : delete : cannot delete programs that have been used in certificates
    edit_dat_test(driver, DF, caso=1, rol='Solicitante', program_action=1, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Egresado', '2023-01-03'])
    time.sleep(5)
    edit_dat_test(driver, DF, caso=2, rol='Solicitante', program_action=2, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Estudiante Activo', None])
    time.sleep(5)
    edit_dat_test(driver, DF, caso=3, rol='Solicitante', program_action=3, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Estudiante Activo', None])
    '''