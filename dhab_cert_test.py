import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

ROLES = ['Administrador']
NAMES = [] 

def dhab_cert_test(driver, DF, caso, rol, nombre):

    UAC = 3
    passed = 0

    FUNC_STR = 'Des/Habilitar Certificado'
    PARAMS_STR = f"Nombre: {nombre}"

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Ver certificados')
        time.sleep(10)

        shared.search(driver, 'Certificados', nombre)

        old_status = shared.read_cert_status(driver, 0)
        print(old_status)

        shared.click_eye_button(driver, 'Certificados', 0)

        time.sleep(5)

        shared.search(driver, 'Certificados', nombre)

        # [UAC] Al deshabilitar/habilitar el certificado, el estado cambia correctamente
        new_status = 'Habilitado' if old_status == 'Deshabilitado' else 'Deshabilitado'
        result = shared.UAC_validate_saved_record(driver, 'Certificados', [nombre, None, new_status], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'Al deshabilitar/habilitar el certificado, el estado cambia correctamente', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Certificados', 0)   

        time.sleep(5)

        nivel = shared.get_input_value(driver, 'Nivel')
        programas = shared.get_multiselect_values(driver, 'Programas')

        shared.click_button(driver, 'Cerrar', 1)

        # [UAC] Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de AGGR SOL
        shared.select_role(driver, 'Administrador')
        time.sleep(5)
        shared.select_module(driver, 'Solicitudes')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(10)
        shared.select_value(driver, 'Grupo', nivel.title()) # titlecase in this form
        shared.select_value(driver, 'Programa', programas[0])
        if new_status == 'Habilitado':
            result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        else:
            result = shared.UAC_check_element_not_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de AGGR SOL', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de NUEVO TICKET
        shared.select_role(driver, 'Solicitante')
        time.sleep(5)
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(2)
        shared.select_value(driver, 'Programa', programas[0]) # PRECONDITION: Program must be assigned to Solicitante
        if new_status == 'Habilitado':
            result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        else:
            result = shared.UAC_check_element_not_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de NUEVO TICKET', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'DHAB CERT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'DHAB CERT: {passed}/{UAC} UAC PASSED')
        return DF



if __name__ == "__main__":
    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 49

    for i in range(nexp):

        rol = random.choice(ROLES)
        name = NAMES[i]

        DF = dhab_cert_test(driver, DF, caso=i+1, rol=rol, name=name)

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

    DF.to_excel(r'results\dhab_cert_test_results.xlsx', index=False)