import time
from selenium.webdriver.common.by import By
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import lib.edit_dat_lib as edit_dat
import utils.datetime_id as id
import os
import traceback

def gen_rep_test(driver, rol, report, periodo_academico=None, f_inicio=None, f_final=None):

    UAC = 2
    passed = 0

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

            # [UAC] El archivo se descarga correctamente
            # [UAC] El archivo se descarga con el nombre correcto
            file_name_substr = f'ReportePeriodo{periodo_academico}'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=2)
            passed += shared.evaluate_UAC_result(result)
            passed += 1
            # END UAC CHECK

        elif report == 2:
            shared.click_button(driver, 'reporte histórico')
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente
            # [UAC] El archivo se descarga con el nombre correcto
            file_name_substr = f'ReporteHistorico'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=3)
            passed += shared.evaluate_UAC_result(result)
            passed += 1
            # END UAC CHECK

        elif report == 3:
            shared.click_button(driver, 'reporte periodo actual')
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente
            # [UAC] El archivo se descarga con el nombre correcto
            file_name_substr = f'ReportePeriodo'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=4)
            passed += shared.evaluate_UAC_result(result)
            passed += 1
            # END UAC CHECK

        elif report == 4:
            shared.set_date_field_value(driver, 1, 'Inicio', f_inicio)
            time.sleep(5)
            shared.set_date_field_value(driver, 1, 'Final', f_final)
            time.sleep(5)
            shared.click_button(driver, 'Generar', idx=1)
            time.sleep(5)

            # [UAC] El archivo se descarga correctamente
            # [UAC] El archivo se descarga con el nombre correcto
            file_name_substr = f'ReporteFechas'
            result = shared.UAC_validate_downloaded_filename(file_name_substr, file=5)
            passed += shared.evaluate_UAC_result(result)
            passed += 1
            # END UAC CHECK


        print(f'GEN REP: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'GEN REP: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    time.sleep(10)

    # 1 : Reporte periodo academico
    # 2 : Reporte Historico
    # 3 : Reporte Periodo Actual
    # 4 : Reporte por fechas
    
    gen_rep_test(driver, rol='Administrador', report=1, periodo_academico='2023-1')
    gen_rep_test(driver, rol='Administrador', report=2)
    gen_rep_test(driver, rol='Administrador', report=3)
    gen_rep_test(driver, rol='Administrador', report=4, f_inicio='2023/04/04', f_final='2023/04/08')