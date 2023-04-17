import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import data.data_api as data_api
import random
import pandas as pd
import datetime

ROLES = ['Administrador', 'Gestor 1', 'Gestor 2', 'Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']
NOMBRES = [ 'Sofía Elena', 'Martín Andrés', 'Ana Isabel', 'Santiago Alejandro', 'Valentina Victoria' ]
APELLIDOS = [ 'García Pérez', 'Martínez Sánchez', 'Ramírez González', 'Gómez Rodríguez', 'Castro Ruiz' ]
TIPOSDOC = ['T.I.', 'C.C.', 'Pasaporte', 'Cédula de Extranjería']
NUMSDOC = ['67890123', 'FG789012', '1234567A', '4567890B', '8901234C', '2345678D', '5678901E', '9012345F', 'CD567890', 'EF789012', 'GH901234', 'IJ345678', 'KL901234']
EMAILS = ['johndoe@example.com', 'sarahsmith@gmail.com', 'robertjohnson@hotmail.com', 'emilycarter@yahoo.com', 'michaelbrown@outlook.com', 'amandaadams@icloud.com', 'brianlee@aol.com', 'christinegarcia@protonmail.com', 'davidjackson@live.com', 'lisawalker@rediffmail.com']
CELULARES = ["5551234567", "5559876543", "5551112233", "5557778899", "5554445566", "5552223344", "5558889999", "5556667777", "5555551212", "5551212121"]
NIVELES = ['Pregrado', 'Posgrado']
ESTADOS_SOL = ['Estudiante activo', 'Egresado']
CERTIFICADOS = ['Certificado de Servicio Comunitario Universitario - 1681714464', 'Certificado de Desarrollo Personal y Profesional - 1681714832', 'Certificado de Logro en Programa de Prácticas - 1681715084', 'Certificado de Logro en Estudio de Idiomas o Intercambio Internacional - 1681715507', 'Certificado de Investigación Estudiantil - 1681714584']
OBSERVACIONES = ['Lorem ipsum dolor sit.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris.']
MEDIOSPAGO = ['Banco']
NUMSCONSIG = ['2023000', '1234567890']
NOTAS = ['Lorem ipsum dolor sit.']
FECHAS = ['2018-05-17', '2011-10-11', '2023-07-22', '2015-03-12', '2018-11-16', '2013-02-07', '2020-01-23', '2010-09-29', '2015-11-14', '2022-05-06', '2019-08-09', '2016-12-26', '2016-05-20', '2023-04-29', '2024-03-07', '2015-04-30', '2016-06-15', '2020-12-01', '2021-08-02', '2012-07-14']

def aggr_sol_test(driver, DF, caso, rol, nombres, apellidos, tipo_doc, num_doc, email, celular, grupo, programa, estado_usu, cert, observaciones, medio_pago, num_consig, nota_interna, fecha_grado_retiro=None):

    UAC = 5
    passed = 0

    FUNC_STR = 'Agregar Solicitud'
    PARAMS_STR = f'Nombres: {nombres}\nApellidos: {apellidos}\nTipo Doc: {tipo_doc}\nNum Doc: {num_doc}\nEmail: {email}\nCelular: {celular}\nGrupo: {grupo}\nPrograma: {programa}\nEstado Sol: {estado_usu}\nCertificado: {cert}\nObservaciones: {observaciones}\nMedio Pago: {medio_pago}\nNum Consig: {num_consig}\nNota: {nota_interna}\nFecha Grado/Retiro: {fecha_grado_retiro}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(5)
        shared.click_button(driver, 'Agregar')
        time.sleep(5)

        shared.enter_input_value(driver, 'Nombres', nombres)
        shared.enter_input_value(driver, 'Apellidos', apellidos)
        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Número de documento', num_doc)
        shared.enter_input_value(driver, 'Correo', email)
        shared.enter_input_value(driver, 'Celular', celular)
        shared.click_checkbox(driver, 'Acepto las políticas')
        shared.select_value(driver, 'Grupo', grupo)
        
        # [UAC] Los programas se filtran de acuerdo al grupo seleccionado
        df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])
        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Programa'),
                                             df.loc[df['nivel'] == grupo.lower(), 'programa'].tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los programas se filtran de acuerdo al grupo seleccionado', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.select_value(driver, 'Programa', programa)
        shared.select_value(driver, 'Estado', estado_usu)
        time.sleep(1)
        if estado_usu != 'Estudiante Activo':
            shared.set_date_field_value(driver, 2, 'Fecha de grado/retiro', fecha_grado_retiro)
        shared.select_value(driver, 'Certificado', cert)
        shared.enter_textarea_value(driver, 'Observaciones', observaciones)
        shared.select_value(driver, 'Medio de pago', medio_pago)
        shared.press_esc_key(driver)
        shared.enter_input_value(driver, 'Numero de consignación', num_consig) # spelling error
        shared.enter_input_value(driver, 'Soporte de pago', os.path.abspath(r'utils\files\soporte.pdf'), mode=1)
        shared.enter_textarea_value(driver, 'Nota interna', nota_interna)
        shared.click_button(driver, 'Crear')
        time.sleep(2)
      
        # [UAC] El sistema redirige a la tabla de solicitudes tras enviar el formulario
        try:
            # [UAC] La solicitud se guarda con los datos correctos
            result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [None, f'{nombres} {apellidos}', None, 'Radicado'], 0) # idx 0 because oredered by update time desc
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'La solicitud se guarda con los datos correctos', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')
            # END UAC CHECK

            passed += 1 # El sistema redirige a la tabla de solicitudes tras enviar el formulario 
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                    'El sistema redirige a la tabla de solicitudes tras enviar el formulario ', 
                                    'SI',
                                    'PASSED')        
            # END UAC CHECK
        except:
            shared.select_module(driver, 'Solicitudes')
            time.sleep(10)
            # La solicitud se guarda con los datos correctos
            result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [None, f'{nombres} {apellidos}', None, 'Radicado'], 0) # idx 0 because oredered by update time desc
            passed += shared.evaluate_UAC_result(result)
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 
                                    'La solicitud se guarda con los datos correctos', 
                                    f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                    'PASSED' if result[0] else 'FAILED')

            passed += 0 # El sistema NO redirige a la tabla de solicitudes tras enviar el formulario  
            DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                        'El sistema redirige a la tabla de solicitudes tras enviar el formulario ', 
                        'NO',
                        'FAILED')       

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                'El rol seleccionado se mantiene tras enviar el formulario', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] Los datos de la solicitud aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Solicitudes', 0, 0)   
        time.sleep(2)
        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Nombres'),
                                                shared.get_input_value(driver, 'Apellidos'),
                                                shared.get_input_value(driver, 'Documento'),
                                                shared.get_input_value(driver, 'Tipo de pago'),
                                                shared.get_input_value(driver, 'Numero consignación'),
                                                shared.get_input_value(driver, 'Certificado'),
                                                shared.get_textarea_value(driver, 'Observaciones')
                                                ], [nombres, apellidos, num_doc, medio_pago, num_consig, cert, observaciones])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                'Los datos de la solicitud aparecen correctamente en el modo edición', 
                                f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')
        return DF
        

if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 30

    for i in range(nexp):

        rol = random.choice(ROLES)
        nombres = random.choice(NOMBRES)
        apellidos = random.choice(APELLIDOS)
        tipo_doc = random.choice(TIPOSDOC)
        num_doc = f'{NUMSDOC[i]} - {id.get_id_()}'
        email = random.choice(EMAILS)
        celular = random.choice(CELULARES)
        nivel = random.choice(NIVELES)
        estado_sol = random.choice(ESTADOS_SOL)
        certificado = random.choice(CERTIFICADOS)
        observaciones = random.choice(OBSERVACIONES)
        medio_pago = random.choice(MEDIOSPAGO)
        numconsig = random.choice(NUMSCONSIG)
        nota = random.choice(NOTAS)

        programs = sorted(df.loc[df['nivel'] == nivel.lower(), 'programa'].tolist())
        idx = random.randint(0, len(programs) - 1)
        program = programs[idx]

        fgr = None if estado_sol == 'Estudiante activo' else random.choice(FECHAS)

        DF = aggr_sol_test(driver, 
                            rol=rol,
                            nombres=nombres, 
                            apellidos=apellidos, 
                            tipo_doc=tipo_doc, 
                            num_doc=num_doc, 
                            email=email, 
                            celular=celular, 
                            grupo=nivel, 
                            programa=program, 
                            estado_usu=estado_sol, 
                            cert=certificado, 
                            observaciones=observaciones, 
                            medio_pago=medio_pago, 
                            num_consig=numconsig, 
                            nota_interna=nota,
                            fecha_grado_retiro=fgr)
        
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
    print(f"Tiempo total aprox. para {nexp} casos sin espera: {datetime.timedelta(seconds=total_time + wait * nexp)}")

    DF.to_excel(r'results\aggr_sol_test_results.xlsx', index=False)