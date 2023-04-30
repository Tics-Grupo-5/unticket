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
PROGRAMAS = []
CERTIFICADOS = []
OBSERVACIONES = []
DIGITALES = []
NUM_CONSIGS = []
TIPOS_PAGO = []

def nuevo_ticket_test(driver, DF, caso, rol, programa, certificado, observaciones, digital, num_consig=None, tipo_pago=None):

    UAC = 4
    passed = 0

    FUNC_STR = 'Login'
    PARAMS_STR = f'Programa: {programa}\nCertificado: {certificado}\nObservaciones: {observaciones}\nDigital: {digital}\nNum Consig: {num_consig}\nTipo Pago: {tipo_pago}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        expected_programs = edit_dat.get_all_programs(driver)

        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(5)

        ids = shared.get_all_solicitudes_ids(driver)

        # [UAC] Los programas se filtran correctamente según los datos de perfil del usuario
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(5)
        visible_programs = shared.get_select_dropdown_values(driver, 'Programa')
        shared.press_esc_key(driver)
        result = shared.UAC_check_two_lists(visible_programs, expected_programs)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                'Los programas se filtran correctamente según los datos de perfil del usuario', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

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

        # [UAC] El enlace de PAGO VIRTUAL dirige al sitio web correctamente
        shared.switch_to_window(driver, 1)
        result = shared.UAC_check_current_url(driver, 'pago-virtual')
        passed += shared.evaluate_UAC_result(result)
        driver.close()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                'El enlace de PAGO VIRTUAL dirige al sitio web correctamente', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK
        
        shared.switch_to_window(driver, 0)

        shared.enter_input_value(driver, 'Número de consignación', num_consig) # spelling error
        shared.enter_input_value(driver, 'Soporte de pago', os.path.abspath(r'utils\files\soporte.pdf'), mode=1)
        shared.select_value(driver, 'Tipo de pago', tipo_pago)

        shared.click_button(driver, 'Terminar')

        # [UAC] Al enviar la solicitud, se guarda correctamente y el estado es Radicado
        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(5)
        new_ids = shared.get_all_solicitudes_ids(driver)
        new_id = list(set(new_ids) - set(ids))[0]
        shared.search(driver, 'Mis Solicitudes', new_id)
        result = shared.UAC_validate_saved_record(driver, 'Mis Solicitudes', [new_id, 'Radicado', certificado, num_consig, observaciones], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                'Al enviar la solicitud, se guarda correctamente y el estado es Radicado', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] La solicitud es visible con los datos correctos para los diferentes roles
        results = []
        for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
            shared.select_role(driver, _rol_)
            time.sleep(5)
            shared.select_module(driver, 'Solicitudes')
            time.sleep(10)
            shared.search(driver, 'Solicitudes', new_id)
            results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [new_id, None, None, None, 'Radicado'], 0))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                 'La solicitud es visible con los datos correctos para los diferentes roles', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK

        print(f'NUEVO TICKET: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'NUEVO TICKET: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":
    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 86 # suma de todos los time sleep en la función

    for i in range(nexp):

        rol = random.choice(ROLES)
        programa = PROGRAMAS[i]
        certificado = CERTIFICADOS[i]
        observaciones = OBSERVACIONES[i]
        digital = DIGITALES[i]
        num_consig = NUM_CONSIGS[i]
        tipo_pago = TIPOS_PAGO[i]

        DF = nuevo_ticket_test(driver, DF, caso=i+1, rol=rol, programa=programa, certificado=certificado, observaciones=observaciones, digital=digital, num_consig=num_consig, tipo_pago=tipo_pago)

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

    DF.to_excel(r'results\nuevo_ticket_test_results.xlsx', index=False)

    '''
    nuevo_ticket_test(driver, rol='Solicitante', programa='Ingeniería Agrícola', certificado='Mi Certificado', 
                      observaciones='Lorem ipsum dolor sit amet, consectetur adipiscing elit', 
                      digital=True, num_consig='2023000', tipo_pago='Banco')
    '''
