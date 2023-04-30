import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

ROLES = ['Administrador']
FECHAS_INICIO = []
FECHAS_FINAL = []
MODES = []

def edit_pv_test(driver, DF, caso, rol, pv, fecha_inicio, fecha_final, mode=0):

    UAC = 2
    passed = 0

    FUNC_STR = 'Editar Periodo'
    PARAMS_STR = f'PV: {pv}\nFecha Inicio: {fecha_inicio}\nFecha Final: {fecha_final}\nMode: {mode}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Periodo académico')
        time.sleep(5)
        if mode == 0:
            shared.click_button(driver, 'Modificar')

        shared.click_button(driver, 'Limpiar campos')
        time.sleep(2)

        shared.enter_input_value(driver, 'nombre', pv)
        time.sleep(1)
        shared.set_date_field_value(driver, 1, 'Inicio', fecha_inicio)
        time.sleep(1)
        shared.set_date_field_value(driver, 1, 'Final', fecha_final)
        time.sleep(2)

        shared.click_button(driver, 'Guardar')
        
        # [UAC] Los datos del periodo académico se guardan correctamente
        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'nombre'),
                                                shared.get_input_value(driver, 'Inicio'),
                                                shared.get_input_value(driver, 'Final')
                                                ], [pv, fecha_inicio, fecha_final])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los datos del periodo académico se guardan correctamente', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] El periodo académico aparece en el módulo GEN REP
        shared.select_module(driver, 'Generar reporte')
        time.sleep(5)
        result = shared.UAC_check_element_in_dropdown(pv, shared.get_select_dropdown_values(driver, 'Periodo Académico'))
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El periodo académico aparece en el módulo GEN REP', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'EDIT PV: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'EDIT PV: {passed}/{UAC} UAC PASSED')
        return DF


def test_clear_fields(driver, rol, mode=0):

    UAC = 1
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Periodo académico')
        time.sleep(5)
        if mode == 0:
            shared.click_button(driver, 'Modificar')

        shared.click_button(driver, 'Limpiar campos')
        time.sleep(2)

        # [UAC] El botón de limpiar campos funciona correctamente
        nombreValidation = shared.UAC_validate_input_field(driver, 'nombre', '')
        inicioDateValidation = shared.UAC_validate_input_field(driver, 'Inicio', '')
        finalDateValidation = shared.UAC_validate_input_field(driver, 'Final', '')

        if nombreValidation[0] and inicioDateValidation[0] and finalDateValidation[0]: 
            passed += 1
        # END UAC CHECK

        print(f'EDIT PV (CLEAR FIELDS): {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT PV (CLEAR FIELDS): {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 20 # suma de todos los time sleep en la función : o una aproximación

    for i in range(nexp):

        rol = random.choice(ROLES)
        fecha_inicio = FECHAS_INICIO[i]
        fecha_final = FECHAS_FINAL[i]
        mode = MODES[i]

        DF = edit_pv_test(driver, DF, caso=i+1, rol=rol, fecha_inicio=fecha_inicio, fecha_final=fecha_final, mode=mode)

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

    DF.to_excel(r'results\edit_pv_test_results.xlsx', index=False)

    '''
    test_clear_fields(driver, rol='Administrador') 
    edit_pv_test(driver, rol='Administrador', pv='2023-1', fecha_inicio='2023-01-03', fecha_final='2023-06-03', mode=1) # mode 1, Modificar already clicked
    '''