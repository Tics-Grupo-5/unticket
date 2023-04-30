import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import data.data_api as data_api
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api


estado_to_roles = {
    'Radicado': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'En trámite': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'Aclaración': ['Administrador', 'Gestor 1', 'Gestor 2'],
    'Elaborado': ['Recepción'],
    'Cerrado': ['']
}

ROLES = ['Administrador']
USERNAMES = []
IDS = []
ESTADOS = []
ENCARGADOS = []
ROLES_ENCARGADO = []
NOTAS = []

def edit_sol_test(driver, DF, caso, username, rol, id, estado, encargado, rol_encargado, nota):

    UAC = 8
    passed = 0

    FUNC_STR = 'Editar Solicitud'
    PARAMS_STR = f'ID: {id}\nEstado: {estado}\nEncargado: {encargado}\nRol Encargado: {rol_encargado}\nNota: {nota}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(10)

        shared.search(driver, 'Solicitudes', id)

        shared.click_edit_button(driver, 'Solicitudes', 0, 0)

        time.sleep(5)

        # [UAC] El soporte de pago se descarga correctamente y con el nombre correcto
        shared.descargar_soporte_from_edit_form(driver)
        username = shared.get_input_value(driver, 'Usuario')
        file_name_substr = f'{username}_{id}'
        time.sleep(5)
        result = shared.UAC_validate_downloaded_filename(file_name_substr, file=0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El soporte de pago se descarga correctamente y con el nombre correcto', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Los estados disponibles son acorde al rol
        estados = shared.get_select_dropdown_values(driver, 'Estado')
        result = shared.UAC_check_estados_for_role(estados, rol)
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los estados disponibles son acorde al rol', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.select_value(driver, 'Estado', estado)
        time.sleep(1)

        # [UAC] Los encargados se filtran correctamente de acuerdo al estado seleccionado
        df = data_api.read_file(r'data\usuarios.txt', col_names=['usuario', 'nombre', 'rol'])
        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Encargado'),
                                             df[df['rol'].isin(estado_to_roles[estado])]['nombre'].unique().tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los encargados se filtran correctamente de acuerdo al estado seleccionado', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.select_value(driver, 'Encargado', encargado)
        time.sleep(1)

        # [UAC] Los roles se filtran correctamente de acuerdo al encargado seleccionado
        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Rol'),
                                            list(set(df.loc[df['nombre'] == encargado, 'rol'].unique().tolist()) & set(estado_to_roles[estado])))
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los roles se filtran correctamente de acuerdo al encargado seleccionado', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.select_value(driver, 'Rol', rol_encargado)
        shared.enter_textarea_value(driver, 'Nota', nota)

        if estado == 'Elaborado':
            shared.enter_input_value(driver, 'Certificado digital', os.path.abspath(r'utils\files\certificado.pdf'), mode=1)

        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El rol seleccionado se mantiene tras enviar el formulario', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Los datos de la solicitud se guardan correctamente
        shared.search(driver, 'Solicitudes', id)
        result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, estado, encargado], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los datos de la solicitud se guardan correctamente', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] La acción se agrega correctamente al registro de actividad
        shared.click_edit_button(driver, 'Solicitudes', 0, 0)   
        time.sleep(2)
        nombre = df.loc[df['usuario'] == username, 'nombre'].unique()[0]
        result = shared.UAC_check_registro_de_actividad(driver, [nombre, estado, encargado, rol_encargado, nota])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'La acción se agrega correctamente al registro de actividad', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] La solicitud es visible con los datos correctos para los diferentes roles
        results = []
        for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
            if _rol_ != rol:
                shared.select_role(driver, _rol_)
                time.sleep(5)
                shared.select_module(driver, 'Solicitudes')
                time.sleep(10)
                shared.search(driver, 'Solicitudes', id)
                results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, estado, encargado], 0))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'La solicitud es visible con los datos correctos para los diferentes roles', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK

        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'EDIT SOL: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 104 # suma de todos los time sleep en la función

    for i in range(nexp):

        rol = random.choice(ROLES)
        id_ = IDS[i]
        estado = ESTADOS[i]
        encargado = ENCARGADOS[i]
        rol_encargado = ROLES_ENCARGADO[i]
        nota = NOTAS[i]

        DF = edit_sol_test(driver, DF, caso=i+1, rol=rol, id=id_, estado=estado, encargado=encargado, rol_encargado=rol_encargado, nota=nota)

        iteration_time = time.time() - start_time - total_time
        total_time += iteration_time

        print(f"Caso {i+1} tomó: {datetime.timedelta(seconds=iteration_time)}")
        print(f"Caso {i+1} sin espera tomó aprox.: {datetime.timedelta(seconds=iteration_time - wait)}")

    avg_time_per_iteration = total_time / nexp
    total_time = time.time() - start_time

    print('\n\n\n')
    print(f"Tiempo promedio por caso: {datetime.timedelta(seconds=avg_time_per_iteration)}")
    print(f"Tiempo promedio aprox. por caso sin espera: {datetime.timedelta(seconds=avg_time_per_iteration - wait)}") 
    print(f"Tiempo total para {nexp} casos: {datetime.timedelta(seconds=total_time)}")
    print(f"Tiempo total aprox. para {nexp} casos sin espera: {datetime.timedelta(seconds=total_time - wait * nexp)}")

    DF.to_excel(r'results\edit_sol_test_results.xlsx', index=False)

    '''
    edit_sol_test(driver, username, rol='Administrador', id='1508', estado='Elaborado', encargado='Cristian Camilo', rol_encargado='Administrador', nota='nota')
    '''