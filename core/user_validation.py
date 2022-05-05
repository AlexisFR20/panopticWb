

def validate(request):
    if request.user.ceo == 1:
        tipousuario = 'CEO'
        tuser = 'ceo'
    elif request.user.vicepresidente == 1:
        tipousuario = 'VICEPRESIDENTE'
        tuser = 'vice'
    elif request.user.vicepresidente_la == 1:
        tipousuario = 'VICEPRESIDENTE LA'
        tuser = 'vicela'
    elif request.user.gerente_regional == 1:
        tipousuario = 'GERENTE REGIONAL'
        tuser = 'gtereg'
    elif request.user.gerente_planta == 1:
        tipousuario = 'GERENTE DE PLANTA'
        tuser = 'gteplanta'    
    elif request.user.planta_plus == 1:
        tipousuario = 'GERENTE DE PLANTAS PLUS'
        tuser = 'gteplus'
    else:
        if request.user.is_staff == 1:           
            tipousuario = 'Administrador'
            tuser = 'admin'
        else:
            tipousuario = 'Invitado'
            tuser = 'inv'

    if 'tipousuario' in request.GET:
        tipousuario = request.GET['tipousuario']
        print("validatio "+tipousuario)
    
        
    page_name = "Inicio"
    
    fullname = request.user.first_name + " " + request.user.last_name        
    
    if fullname == '':
        fullname = request.user.username

    return {
        'tipousuario': tipousuario,
        'tuser': tuser,
        "page_name": page_name,
        "fullname": fullname, 
        "user_id": request.user.id,        
        "cliente_id": request.user.cliente_id
        }
    