import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import traceback
import utils.filters as filters
import random
import pandas as pd
import datetime
import data.data_api as data_api

ROLES = ['Administrador']
FILTERS = ([filters.FILTERS['certificados']['nombre'] ] * 6) + ([filters.FILTERS['certificados']['grupo']] * 4)
KEYWORDS = ['Certificado - 1682570149', 'Certificado - 1682638508', 'UN Certificado 2023', 'Certificado 20190000', 'Certificado - 1682638641', 'Certificado - 1682638776', 'Pregrado', 'Secundaria', 'Posgrado', 'PHD']
EXPECTED = [True, True, False, False, True, True, True, False, True, False]

# Test buscar certificado - admin
def bus_cert_test(driver, DF, caso, rol, filter, keyword, expected):
    
    UAC = 1
    passed = 0

    FUNC_STR = 'Buscar Certificdo'
    PARAMS_STR = f'Filtro: {filter}\nKeyword: {keyword}\nExpected: {expected}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        # Select module 
        shared.select_module(driver, 'Ver certificados')
        time.sleep(10)
       
        # Buscar certificado
        shared.search(driver, 'Certificados', keyword)
        time.sleep(5)

        # [UAC] Al buscar por nombre completo o grupo, aparecen los resultados correctos
        result = shared.UAC_check_search_results(driver, 'Certificados', keyword, filter['column'], filter['unique'], expected)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'Al buscar por nombre completo o grupo, aparecen los resultados correctos', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'BUS CERT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'BUS CERT: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 20

    for i in range(nexp):

        rol = random.choice(ROLES)
        filter = FILTERS[i]
        keyword = KEYWORDS[i]
        expected = EXPECTED[i]

        DF = bus_cert_test(driver, DF, caso=i+1, rol=rol, filter=filter, keyword=keyword, expected=expected)

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

    DF.to_excel(r'results\bus_cert_test_results.xlsx', index=False)
