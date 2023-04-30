import time

from getpass import getpass
import lib.login_lib as login
import lib.shared_lib as shared
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

def login_test(driver, DF, caso, username, password):

    UAC = 2
    passed = 0

    FUNC_STR = 'Login'
    PARAMS_STR = f'Username: {username}'

    try:

        shared.go_to_url(driver, 'bienvenida')
        
        login.click_ingresar_button(driver)
        
        time.sleep(1)

        shared.switch_to_window(driver, 1)
        
        time.sleep(2)

        # [UAC] El sistema evita el ingreso de cuentas con dominio diferente de unal.edu.co
        results = []
        results.append(login.UAC_check_unal_domain(driver))
        login.login_to_unal_ldap(driver, username, password)
        time.sleep(5)
        login.confirm_google_account(driver)
        time.sleep(3)
        login.click_use_another_account(driver)
        time.sleep(3)
        results.append(login.UAC_check_google_unal_domain(driver))
        login.login_to_google(driver, username)
        time.sleep(2)
        results.append(login.UAC_check_unal_domain(driver))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                 'El sistema evita el ingreso de cuentas con dominio diferente de unal.edu.co', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK
        
        login.login_to_unal_ldap(driver, username, password)
        time.sleep(10)
        shared.switch_to_window(driver, 0)

        # [UAC] El usuario autenticado es dirigido a su perfil correctamente
        result = shared.UAC_check_current_url(driver, 'perfil')
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                'El usuario autenticado es dirigido a su perfil correctamente', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'LOGIN: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'LOGIN: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == "__main__":

    # Ejecución por lotes no implementada
    driver = shared.init_driver()
    login_test(driver, input('Username: '), getpass('Password: '))
