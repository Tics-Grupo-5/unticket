import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.filters as filters

def bus_usu_test(driver, rol, filter, keyword, expected):
    UAC=1
    passed=0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver,'Administrar usuarios')
        time.sleep(10)

        shared.search(driver,'Usuarios', keyword)
        time.sleep(5)

        # [UAC] Al buscar por nombre de usuario, aparecen los resultados correctos
        result = shared.UAC_check_search_results(driver, 'Usuarios', keyword, filter['column'], filter['unique'], expected)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'BUS USU: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'BUS USU: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    bus_usu_test(driver, rol='Administrador', filter=filters.FILTERS['usuarios']['username'], keyword='miguel', expected=False)
    bus_usu_test(driver, rol='Administrador', filter=filters.FILTERS['usuarios']['username'], keyword='mvilladas', expected=True)