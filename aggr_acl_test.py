import time
import lib.aggr_acl_lib as aggr_acl
from login_test import login_test as login
from getpass import getpass
import lib.shared_lib as shared
import utils.filters as filters
import traceback

# Test de agregar aclaracion - solicitante
def aggr_acl_test(driver, rol, id, respuesta):

    UAC = 2
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)
        
        # Add clarification
        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(5)
        
        shared.search(driver, 'Mis Solicitudes', id)
        time.sleep(5)
        
        aggr_acl.click_solicitud(driver, 0)
        time.sleep(5)

        shared.enter_textarea_value(driver, 'Respuesta', respuesta)

        shared.click_button(driver, 'Guardar')
        time.sleep(5)
      
        # [UAC] La solicitud se guarda con los datos correctos y el estado es En trámite
        shared.search(driver, 'Mis Solicitudes', id)
        result = shared.UAC_validate_saved_record(driver, 'Mis Solicitudes', [id, 'En trámite'], 0)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] La solicitud es visible con los datos correctos para los diferentes roles
        results = []
        for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
            shared.select_role(driver, _rol_)
            time.sleep(5)
            shared.select_module(driver, 'Solicitudes')
            time.sleep(10)
            shared.search(driver, 'Solicitudes', id)
            results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, 'En trámite'], 0))
        passed += shared.evaluate_composite_UAC_result(results)
        # END UAC CHECK

        print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')
    except Exception as e:
        traceback.print_exc()
        print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')

if __name__ == '__main__':
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    aggr_acl_test(driver, rol='Solicitante', id='1508', respuesta='aclaración 1508') # PRECONDICIÓN: Necesita estar en estado Aclaración



