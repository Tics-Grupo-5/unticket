# Test: Edicion de Periodo Vigente (Rol: Admin)

# | -- Accion --                   | -- program_action --

# | Edicion sin Limpiar Campos     |          0
# | Test de Limpiar Campos         |          1

import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import traceback

def edit_pv_test(driver, program_action=0):
    UAC = 1
    passed = 0

    try:
        shared.select_module(driver, 'Periodo académico')
        time.sleep(5)
        shared.click_button(driver, 'Modificar')
        time.sleep(3)

        if program_action == 0:
            passed = edit_pv_by_clearing_fields(driver, passed)
        elif program_action == 1:
            passed = test_clearing_fields(driver, passed)
        else:
            raise ValueError('The given value for program_action is invalid!')

        time.sleep(5)
        print(f'EDIT PV (PERIODO VIGENTE): {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT PV (PERIODO VIGENTE): {passed}/{UAC} UAC PASSED')

def edit_pv_by_clearing_fields(driver, passed):
    shared.click_button(driver, 'Limpiar campos')
    time.sleep(2)

    shared.enter_input_value(driver, 'nombre', '2023-1')
    time.sleep(1)
    shared.set_date_field_value(driver, 1, 'Inicio', '2023-01-03')
    time.sleep(1)
    shared.set_date_field_value(driver, 1, 'Final', '2023-06-03')
    time.sleep(2)

    shared.click_button(driver, 'Guardar')
    time.sleep(2)
    passed+=1
    return passed

def test_clearing_fields(driver, passed):
    shared.click_button(driver, 'Limpiar campos')
    time.sleep(2)
    nombreValidation = shared.UAC_validate_input_field(driver, 'nombre', 'jkfdsjakfl')
    inicioDateValidation = shared.UAC_validate_input_field(driver, 'Inicio', '')
    finalDateValidation = shared.UAC_validate_input_field(driver, 'Final', '')
    if nombreValidation[0] and inicioDateValidation[0] and finalDateValidation[0]: passed += 1
    return passed

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Administrador')
    time.sleep(5)

    edit_pv_test(driver, program_action=0)
    # edit_pv_test(driver, program_action=1)