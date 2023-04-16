import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import traceback

def edit_pv_test(driver, rol, pv, fecha_inicio, fecha_final, mode=0):

    UAC = 2
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Periodo académico')
        time.sleep(5)
        if mode == 0:
            shared.click_button(driver, 'Modificar')

        shared.click_button(driver, 'Limpiar campos')
        time.sleep(2)

        shared.enter_input_value(driver, 'nombre', pv)
        time.sleep(1)
        shared.set_date_field_value(driver, 1, 'Inicio', fecha_inicio)
        time.sleep(1)
        shared.set_date_field_value(driver, 1, 'Final', fecha_final)
        time.sleep(2)

        shared.click_button(driver, 'Guardar')
        
        # [UAC] Los datos del periodo académico se guardan correctamente
        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'nombre'),
                                                shared.get_input_value(driver, 'Inicio'),
                                                shared.get_input_value(driver, 'Final')
                                                ], [pv, fecha_inicio, fecha_final])
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El periodo académico aparece en el módulo GEN REP
        shared.select_module(driver, 'Generar reporte')
        time.sleep(5)
        result = shared.UAC_check_element_in_dropdown(pv, shared.get_select_dropdown_values(driver, 'Periodo Académico'))
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'EDIT PV: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT PV: {passed}/{UAC} UAC PASSED')


def test_clear_fields(driver, rol, mode=0):

    UAC = 1
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Periodo académico')
        time.sleep(5)
        if mode == 0:
            shared.click_button(driver, 'Modificar')

        shared.click_button(driver, 'Limpiar campos')
        time.sleep(2)

        # [UAC] El botón de limpiar campos funciona correctamente
        nombreValidation = shared.UAC_validate_input_field(driver, 'nombre', '')
        inicioDateValidation = shared.UAC_validate_input_field(driver, 'Inicio', '')
        finalDateValidation = shared.UAC_validate_input_field(driver, 'Final', '')

        if nombreValidation[0] and inicioDateValidation[0] and finalDateValidation[0]: 
            passed += 1
        # END UAC CHECK

        print(f'EDIT PV (CLEAR FIELDS): {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT PV (CLEAR FIELDS): {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    test_clear_fields(driver, rol='Administrador') 
    edit_pv_test(driver, rol='Administrador', pv='2023-1', fecha_inicio='2023-01-03', fecha_final='2023-06-03', mode=1) # mode 1, Modificar already clicked
