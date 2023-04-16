import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import lib.edit_dat_lib as edit_dat
import utils.datetime_id as id
import os
import traceback

def edit_dat_test(driver, program_action, tipo_doc, num_doc, program_data=None):

    UAC = 2
    passed = 0

    try:

        shared.select_module(driver, 'Mis datos')

        shared.click_button(driver, 'Modificar')

        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Número', num_doc)

        if program_action == 1:
            shared.click_button(driver, 'Agregar')
            shared.select_value(driver, 'Estado solicitante', program_data[1])
            shared.select_value(driver, 'Programa', program_data[0], strict=True)

            if program_data[1] != 'Estudiante Activo':
                shared.set_date_field_value(driver, 0, 'Año de grado / Año de retiro', program_data[2])

            shared.click_button(driver, 'Guardar', 1)

        elif program_action == 2:
            edit_dat.see_all_programs(driver)
            edit_dat.open_edit_program_modal(driver, program_data[0])
            shared.select_value(driver, 'Estado solicitante', program_data[1])
            # we cannot select program when editing
            # shared.select_value(driver, 'Programa', program_data[0], strict=True)

            if program_data[1] != 'Estudiante Activo':
                shared.set_date_field_value(driver, 0, 'Año de grado / Año de retiro', program_data[2])

            shared.click_button(driver, 'Guardar', 1)

        elif program_action == 3:
            edit_dat.see_all_programs(driver)
            edit_dat.open_delete_program_modal(driver, program_data[0])
            shared.click_button(driver, 'Eliminar')

        time.sleep(2)
        shared.click_button(driver, 'Guardar')

        time.sleep(10)

        results = []

        results.append(shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Tipo de documento'),
                                                shared.get_input_value(driver, 'Número')
                                                ], [tipo_doc, num_doc]))

        if program_action == 1:
            results.append(edit_dat.UAC_check_if_program_was_added(driver, program_data[0]))
        elif program_action == 2:
            results.append(edit_dat.UAC_check_if_program_was_edited(driver, program_data))
        elif program_action == 3:
            results.append(edit_dat.UAC_check_if_program_was_deleted(driver, program_data[0]))


        passed += shared.evaluate_composite_UAC_result(results)

        expected_programs = edit_dat.get_all_programs(driver)

        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(5)

        visible_programs = shared.get_select_dropdown_values(driver, 'Programa')
        shared.press_esc_key(driver)

        result = shared.UAC_check_two_lists(visible_programs, expected_programs)
        passed += shared.evaluate_UAC_result(result)

        print(f'EDIT DAT: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT DAT: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Solicitante')
    time.sleep(5)
    # 0 : nothing
    # 1 : add : cannot add already added program
    # 2 : edit
    # 3 : delete : cannot delete programs that have been used in certificates
    edit_dat_test(driver, program_action=1, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Egresado', '2023-01-03'])
    time.sleep(5)
    edit_dat_test(driver, program_action=2, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Estudiante Activo', None])
    time.sleep(5)
    edit_dat_test(driver, program_action=3, tipo_doc='C.C.', num_doc='1070000000', program_data=['Ingeniería Mecánica', 'Estudiante Activo', None])