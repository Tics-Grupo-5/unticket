import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.filters as filters

def bus_sol_test(driver, rol, filter, keyword, expected):
    
    UAC = 1
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(10)

        shared.search(driver, 'Solicitudes', keyword)

        time.sleep(5)

        # [UAC] Al buscar por id, estado, solicitante, certificado o encargado, aparecen los resultados correctos
        result = shared.UAC_check_search_results(driver, 'Solicitudes', keyword, filter['column'], filter['unique'], expected)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'BUS SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'BUS SOL: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    bus_sol_test(driver, rol='Administrador', filter=filters.FILTERS['solicitudes']['id'], keyword='1511', expected=True)
    bus_sol_test(driver, rol='Administrador', filter=filters.FILTERS['solicitudes']['id'], keyword='3000', expected=False)
    bus_sol_test(driver, rol='Administrador', filter=filters.FILTERS['solicitudes']['nombre_solicitante'], keyword='Zamir', expected=True)