import time
from getpass import getpass
from login_test import login_test as login
from utils.urls import URLs
import lib.logout_lib as logout
import lib.shared_lib as shared
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

def logout_test(driver, DF, caso, rol):

    UAC = 2
    passed = 0

    FUNC_STR = 'Logout'
    PARAMS_STR = ''

    try:
    
        shared.select_role(driver, rol)
        time.sleep(5)

        logout.click_cerrar_sesion_button(driver)

        time.sleep(2)

        # [UAC] El usuario es dirigido a la página externa correctamente
        result = shared.UAC_check_current_url(driver, 'bienvenida')
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                'El usuario es dirigido a la página externa correctamente', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Se evita el acceso a cualquier URL interna tras completar el cierre de sesión
        results = []
        for urlkey in URLs.keys():
            if urlkey == 'bienvenida':
                continue
            shared.go_to_url(driver, urlkey)
            time.sleep(1)
            results.append(shared.UAC_check_redirection(driver, urlkey, 'bienvenida'))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, '', PARAMS_STR,
                                 'Se evita el acceso a cualquier URL interna tras completar el cierre de sesión', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK

        print(f'LOGOUT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'LOGOUT: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == "__main__":

    # Ejecución por lotes no implementada
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    logout_test(driver, rol='Solicitante')