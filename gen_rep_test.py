import time
from selenium.webdriver.common.by import By
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

ROLES = ['Administrador']
REPORTS = []
PERIODOS_ACADEMICOS = []
F_INICIOS = []
F_FINALES = []

def gen_rep_test(driver, DF, caso, rol, report, periodo_academico=None, f_inicio=None, f_final=None):

    UAC = 1
    passed = 0

    FUNC_STR = 'Generar Reporte'
    PARAMS_STR = f'Report: {report}\nPeriodo Académico: {periodo_academico}\nFecha Inicio: {f_inicio}\nFecha Final: {f_final}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Generar reporte')
        time.sleep(5)

        if report == 1:
            shared.select_value(driver, 'Periodo Académico', periodo_academico)
            time.sleep(5)
            shared.click_button(driver, 'Generar')
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente y con el nombre correcto
            file_name_substr = f'ReportePeriodo{periodo_academico}'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=2)
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'El archivo se descarga correctamente y con el nombre correcto', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
            # END UAC CHECK

        elif report == 2:
            shared.click_button(driver, 'reporte histórico')
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente y con el nombre correcto
            file_name_substr = f'ReporteHistorico'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=3)
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'El archivo se descarga correctamente y con el nombre correcto', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
            # END UAC CHECK

        elif report == 3:
            shared.click_button(driver, 'reporte periodo actual')
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente y con el nombre correcto
            file_name_substr = f'ReportePeriodo'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=4)
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'El archivo se descarga correctamente y con el nombre correcto', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
            # END UAC CHECK

        elif report == 4:
            shared.set_date_field_value(driver, 1, 'Inicio', f_inicio)
            time.sleep(5)
            shared.set_date_field_value(driver, 1, 'Final', f_final)
            time.sleep(5)
            shared.click_button(driver, 'Generar', idx=1)
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente y con el nombre correcto
            file_name_substr = f'ReporteFechas'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=5)
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El archivo se descarga correctamente y con el nombre correcto', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
            # END UAC CHECK


        print(f'GEN REP: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'GEN REP: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == "__main__":
    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 10 # suma de todos los time sleep en la función : o una aproximación

    for i in range(nexp):

        rol = random.choice(ROLES)
        report = REPORTS[i]
        periodo_academico = PERIODOS_ACADEMICOS[i]
        f_inicio = F_INICIOS[i]
        f_final = F_FINALES[i]


        DF = gen_rep_test(driver, DF, caso=i+1, rol=rol, report=report, periodo_academico=periodo_academico, f_inicio=f_inicio, f_final=f_final)

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

    DF.to_excel(r'results\gen_rep_test_results.xlsx', index=False)

    '''
    # 1 : Reporte periodo academico
    # 2 : Reporte Historico
    # 3 : Reporte Periodo Actual
    # 4 : Reporte por fechas
    
    gen_rep_test(driver, rol='Administrador', report=1, periodo_academico='2023-1')
    gen_rep_test(driver, rol='Administrador', report=2)
    gen_rep_test(driver, rol='Administrador', report=3)
    gen_rep_test(driver, rol='Administrador', report=4, f_inicio='2023/04/04', f_final='2023/04/08')
    '''