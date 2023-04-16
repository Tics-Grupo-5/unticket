import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import utils.filters as filters

def bus_msol_test(driver, rol, filter, keyword, expected):
    
    UAC = 1
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(10)

        shared.search(driver, 'Mis Solicitudes', keyword)

        time.sleep(5)

        result = shared.UAC_check_search_results(driver, 'Mis Solicitudes', keyword, filter['column'], filter['unique'], expected)
        passed += shared.evaluate_UAC_result(result)

        print(f'BUS MSOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'BUS MSOL: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    bus_msol_test(driver, rol='Solicitante', filter=filters.FILTERS['mis_solicitudes']['id'], keyword='1511', expected=True)