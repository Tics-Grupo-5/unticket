import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def des_arch_test(driver, id, file, username):

    UAC = 2
    passed = 0

    try:

        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(10)

        shared.search(driver, 'Mis Solicitudes', id)

        time.sleep(10)

        shared.descargar_soporte(driver, 0)

        file_name_substr = f'{username}_{id}'

        time.sleep(5)

        result = shared.UAC_validate_downloaded_filename(file_name_substr, file)
        passed += shared.evaluate_UAC_result(result)
        passed += 1

        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))
    shared.select_role(driver, 'Solicitante')
    time.sleep(5)
    # 0 : soporte
    # 1 : certificado
    des_arch_test(driver, id='1508', file=0, username=username)