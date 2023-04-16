import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import data.data_api as data_api


estado_to_roles = {
    'Radicado': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'En trámite': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'Aclaración': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'Elaborado': ['Recepción'],
    'Cerrado': ['']
}


def edit_sol_test(driver, username, rol, id, estado, encargado, rol_encargado, nota):

    UAC = 8
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(10)

        shared.search(driver, 'Solicitudes', id)

        shared.click_edit_button(driver, 'Solicitudes', 0, 0)

        time.sleep(5)

        shared.descargar_soporte_from_edit_form(driver)
        username = shared.get_input_value(driver, 'Usuario')
        file_name_substr = f'{username}_{id}'
        time.sleep(5)
        result = shared.UAC_validate_downloaded_filename(file_name_substr, file=0)
        passed += shared.evaluate_UAC_result(result)
        passed += 1

        estados = shared.get_select_dropdown_values(driver, 'Estado')
        result = shared.UAC_check_estados_for_role(estados, rol)
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)

        shared.select_value(driver, 'Estado', estado)
        time.sleep(1)

        df = data_api.read_file(r'data\usuarios.txt', col_names=['usuario', 'nombre', 'rol'])
        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Encargado'),
                                             df[df['rol'].isin(estado_to_roles[estado])]['nombre'].unique().tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)

        shared.select_value(driver, 'Encargado', encargado)
        time.sleep(1)

        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Rol'),
                                            list(set(df.loc[df['nombre'] == encargado, 'rol'].unique().tolist()) & set(estado_to_roles[estado])))
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)

        shared.select_value(driver, 'Rol', rol_encargado)
        shared.enter_textarea_value(driver, 'Nota', nota)

        if estado == 'Elaborado':
            shared.enter_input_value(driver, 'Certificado digital', os.path.abspath(r'utils\files\certificado.pdf'), mode=1)

        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)
        shared.search(driver, 'Solicitudes', id)

        result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, estado, encargado], 0)
        passed += shared.evaluate_UAC_result(result)

        # Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Solicitudes', 0, 0)   

        time.sleep(2)

        nombre = df.loc[df['usuario'] == username, 'nombre'].unique()[0]

        result = shared.UAC_check_registro_de_actividad(driver, [nombre, estado, encargado, rol_encargado, nota])
        passed += shared.evaluate_UAC_result(result)

        results = []
        for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
            if _rol_ != rol:
                shared.select_role(driver, _rol_)
                time.sleep(5)

                shared.select_module(driver, 'Solicitudes')
                time.sleep(10)

                shared.search(driver, 'Solicitudes', id)

                results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, estado, encargado], 0))
                
        passed += shared.evaluate_composite_UAC_result(results)


        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))
    edit_sol_test(driver, username, rol='Administrador', id='1508', estado='Elaborado', encargado='Cristian Camilo', rol_encargado='Administrador', nota='nota')