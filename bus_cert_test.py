import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import traceback
import utils.filters as filters

# Test buscar certificado - admin
def bus_cert_test(driver, filter, keyword, expected):
    
    UAC = 1
    passed = 0

    try:
        # Select module 
        shared.select_module(driver, 'Ver certificados')
        time.sleep(10)
       
        # Buscar certificado
        shared.search(driver, 'Certificados', keyword)
        time.sleep(5)

        result = shared.UAC_check_search_results(driver, 'Certificados', keyword, filter['column'], filter['unique'], expected)
        passed += shared.evaluate_UAC_result(result)

        print(f'BUS SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'BUS SOL: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    # Select role
    shared.select_role(driver, 'Administrador')
    time.sleep(5)
    bus_cert_test(driver, filter=filters.FILTERS['certificados']['nombre'], keyword='Mi Certificado 642cdf22', expected=True)
    bus_cert_test(driver, filter=filters.FILTERS['certificados']['nombre'], keyword='Mi Certificado 642cdf29199219', expected=False)
    bus_cert_test(driver, filter=filters.FILTERS['certificados']['grupo'], keyword='Posgrado', expected=True)

