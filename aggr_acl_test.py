import time
import lib.aggr_acl_lib as aggr_acl
from login_test import login_test as login
from getpass import getpass
import lib.shared_lib as shared
import utils.filters as filters
import traceback

# Test de agregar aclaracion - solicitante
def aggr_acl_test(driver, id, respuesta):

  UAC = 2
  passed = 0

  try:
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
  
    # Check if request's state has changed 
    shared.search(driver, 'Mis Solicitudes', id)
    result = shared.UAC_validate_saved_record(driver, 'Mis Solicitudes', [id, 'En trámite'], 0)
    passed += shared.evaluate_UAC_result(result)

    results = []
    for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
        shared.select_role(driver, _rol_)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(10)

        shared.search(driver, 'Solicitudes', id)

        results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, 'En trámite'], 0))
            
    passed += shared.evaluate_composite_UAC_result(results)

    print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')
  except Exception as e:
    traceback.print_exc()
    print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')

if __name__ == '__main__':
  driver = shared.init_driver()
  login(driver, input('Username: '), getpass('Password: '))
  shared.select_role(driver, 'Solicitante')
  #aggr_acl_test(driver, id='1512', respuesta='aclaración 1512')
  aggr_acl_test(driver, id='1508', respuesta='aclaración 1508') # PRECONDICIÓN: Necesita estar en estado Aclaración



