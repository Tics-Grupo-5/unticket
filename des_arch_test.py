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

ROLES = ['Solicitante']
IDS = []
FILES = [] 

def des_arch_test(driver, DF, caso, rol, id, file, username):

    UAC = 1
    passed = 0

    FUNC_STR = 'Descargar Archivo'
    PARAMS_STR = f"ID: {id}\nFile: {'Soporte' if file == 0 else 'Certificado'}\nUsername: {username}"

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(10)

        shared.search(driver, 'Mis Solicitudes', id)

        time.sleep(10)

        shared.descargar_soporte(driver, 0)
        time.sleep(5)

        # [UAC] El archivo se descarga correctamente y con el nombre correcto
        file_name_substr = f'{username}_{id}'
        result = shared.UAC_validate_downloaded_filename(file_name_substr, file)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'El archivo se descarga correctamente y con el nombre correcto', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":
    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 30

    for i in range(nexp):

        rol = random.choice(ROLES)
        id_ = IDS[i]
        file = FILES[i]

        DF = des_arch_test(driver, DF, caso=i+1, rol=rol, id=id_, file=file, username=username)

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

    DF.to_excel(r'results\des_arch_test_results.xlsx', index=False)