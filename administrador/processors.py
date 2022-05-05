def ctx_dict(request):
    ctx = {'test':'hola'}
    return ctx  

rolesCliente = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta', 'seguridad_interna' ]

rolesAguilas = ['administrador', 'gerente_operativo', 'supervisor', 'supervidor_junior', 'ejecutivo_cuenta', 'monitorista', 'coordinador', 'jefe_grupo', 'guardia', 'auditor', 'capacitador', 'chofer']

#Determina el acceso por módulo en base a los roles permitidos en el usuario dado
#Param  Roles(array) y Usuario (instancia)
#Zona 0 
def permisoZona0(request):    
    acceso = {'permisoZona0': False}    
    if str(request.user) != 'AnonymousUser':                
        roles = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta',  'administrador', 'gerente_operativo', 'supervisor', 'supervidor_junior', 'ejecutivo_cuenta', 'monitorista', 'coordinador', 'auditor', 'capacitador']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoZona0': True}    
    return acceso

#Análisis de Riesgo
def permisoAnalisisRiesgo(request):
    acceso = {'permisoAnalisisRiesgo': False}
    if str(request.user) != 'AnonymousUser':          
        roles = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta', 'administrador', 'supervisor', 'supervidor_junior', 'ejecutivo_cuenta', 'monitorista', 'coordinador', 'auditor']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoAnalisisRiesgo': True}    
    return acceso

#D&D Management
def permisoDD(request):
    acceso = {'permisoDD': False}
    if str(request.user) != 'AnonymousUser':          
        roles = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta', 'administrador', 'gerente_operativo', 'supervisor', 'supervidor_junior', 'monitorista', 'coordinador']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoDD': True}
    return acceso

#Carta Porte
def permisoCPorte(request):
    acceso = {'permisoCPorte': False}
    if str(request.user) != 'AnonymousUser':
        roles = ['agente_logistico']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoCPorte': True}
    return acceso

#Predictive Analytics
def permisoPredictive(request):
    acceso = {'permisoPredictive': False}
    if str(request.user) != 'AnonymousUser':          
        roles = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta', 'seguridad_interna','administrador', 'gerente_operativo', 'supervisor', 'supervidor_junior', 'ejecutivo_cuenta', 'coordinador', 'jefe_grupo',  'capacitador', 'chofer']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoPredictive': True}
    return acceso

#Backstage
def permisoBackstage(request):
    acceso = {'permisoBackstage': False}
    if str(request.user) != 'AnonymousUser':          
        roles = ['administrador']
        #roles = ['administrador', 'gerente_operativo', 'supervisor', 'supervidor_junior', 'ejecutivo_cuenta', 'monitorista', 'coordinador', 'jefe_grupo', 'auditor', 'capacitador']
        role = request.user.role.alias_rol
        if role in roles:
            acceso = {'permisoBackstage': True}
    return acceso


