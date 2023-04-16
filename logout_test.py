import time
from getpass import getpass
from login_test import login_test as login
from utils.urls import URLs
import lib.logout_lib as logout
import lib.shared_lib as shared
import traceback

def logout_test(driver, rol):

    UAC = 2
    passed = 0

    try:
    
        shared.select_role(driver, rol)
        time.sleep(5)

        logout.click_cerrar_sesion_button(driver)

        time.sleep(2)

        # [UAC] El usuario es dirigido a la página externa correctamente
        result = shared.UAC_check_current_url(driver, 'bienvenida')
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] Se evita el acceso a cualquier URL interna tras completar el cierre de sesión
        results = []
        for urlkey in URLs.keys():
            if urlkey == 'bienvenida':
                continue
            shared.go_to_url(driver, urlkey)
            time.sleep(1)
            results.append(shared.UAC_check_redirection(driver, urlkey, 'bienvenida'))
        passed += shared.evaluate_composite_UAC_result(results)
        # END UAC CHECK

        print(f'LOGOUT: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'LOGOUT: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    logout_test(driver, rol='Solicitante')