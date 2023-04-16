import time

from getpass import getpass
import lib.login_lib as login
import lib.shared_lib as shared
import traceback

def login_test(driver, username, password):

    UAC = 2
    passed = 0

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
        passed += shared.evaluate_composite_UAC_result(results)
        # END UAC CHECK
        
        login.login_to_unal_ldap(driver, username, password)
        time.sleep(10)
        shared.switch_to_window(driver, 0)

        # [UAC] El usuario autenticado es dirigido a su perfil correctamente
        result = shared.UAC_check_current_url(driver, 'perfil')
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'LOGIN: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'LOGIN: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login_test(driver, input('Username: '), getpass('Password: '))
