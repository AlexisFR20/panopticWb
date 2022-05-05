from csv import excel_tab
from multiprocessing import context
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from core import user_validation
from API.serializers import TrasladoSerializer
import facturama
from types import SimpleNamespace
import json
from django.contrib import messages
import requests
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from .models import *
from .forms import *


# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

new_js_list = ["js_basic","js_datepicker"]

#Credenciales facturama
facturama._credentials = ("ionyhz","fenderjp60010")
facturama.sandbox = True
facturama.api_lite = True

# Create your views here.
class PorteClienteCreateView(CreateView):
    model = PorteCliente
    template_name = "cporte/porte_clientes_form.html"
    form_class = PorteClienteForm

    def get_success_url(self, *args, **kwargs):        
        return reverse('porte_cliente_create')

    def form_valid(self, form, **kwargs):       
        form = form.save(commit=False)        
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class PorteReceiverCreateView(CreateView):
    model = PorteReceiver
    template_name = "cporte/porte_receivers_form.html"
    form_class = PorteReceiverForm
    
    def get_success_url(self, *args, **kwargs):        
        messages.add_message(self.request,  messages.SUCCESS, 'Cliente creado exitosamente!')   
        return reverse('cporte:porte_receiver_create')

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)      
        form.porteCliente_id = self.request.user.portecliente_id    #Importante para guardar el id correspondiente
        form.save()
        return super().form_valid(form)
    
    """
    def get_form_kwargs(self):
        form_kwargs = super(PorteReceiverCreateView, self).get_form_kwargs()
        form_kwargs["type"] = "create"
        return form_kwargs
    """

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        context['btnMessage'] = "Crear"      

        return context
    
class PorteReceiverUpdate(UpdateView):
    model = PorteReceiver
    template_name = "cporte/porte_receivers_form.html"
    form_class = PorteReceiverForm

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request,  messages.SUCCESS, 'Cliente actualizado exitosamente!')   
        return reverse("cporte:porte_receiver_list")
    
    """
    #Ya no se usa, dado que no se comunica con facturama.
    def get_form_kwargs(self):
        form_kwargs = super(PorteReceiverUpdate, self).get_form_kwargs()
        form_kwargs["type"] = "update"
        return form_kwargs
    """

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list 
        context['btnMessage'] = "Actualizar"      

        return context

def porteReceiverDelete(request, id): 
    r_id = id
    try:
        receiver = PorteReceiver.objects.get(id=r_id)
        rfc = receiver.rfc
        try:
            facturama.csdsMultiEmisor.delete(rfc)   
            PorteReceiver.objects.filter(id=r_id).delete()
            messages.add_message(request,  messages.SUCCESS, 'Cliente borrado exitosamente')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, "Hubo un error al borrar el cliente")
    except PorteReceiver.DoesNotExist:
        messages.add_message(request,  messages.ERROR, 'Hubo un error al borrar el cliente')
    return redirect("cporte:porte_receiver_list")

def porteReceiverList(request):
    receivers = PorteReceiver.objects.filter(porteCliente_id=request.user.portecliente_id)
    return render(request, "cporte/porte_receivers_list.html", {"css_list": css_list, "js_list": js_list, "receivers": receivers})

"""
def porteProductoList(request):
    obj_productos = []
    productos = facturama.Product.all()

    for x in productos:
        object_x = json.loads(json.dumps(x), object_hook = lambda d: SimpleNamespace(**d))
        if(object_x.IdentificationNumber == str(request.user.portecliente_id)):
            obj_productos.append(object_x)

    return render(request, "cporte/porte_productos_update.html", {"css_list": css_list, "js_list": js_list, "productos": obj_productos})


def porteProductoUpdate(request, id):
    userdict = user_validation.validate(request)
    idproduct = "id=" + id
    product = facturama.Product.query(idproduct)
    unitCodes = (("H87","Pieza"),("EA","Elemento"),("E48","Unidad de Servicio"),("ACT","Actividad"),
                 ("KGM","Kilogramo"),("E51","Trabajo"),("A9","Tarifa"),("MTR","Metro"),("AB","Paquete a Granel"),
                 ("BB","Caja base"),("KT","Kit"),("SET","Conjunto"),("LTR","Litro"),("XBX","Caja"),("MON","Mes"),
                 ("HUR","Hora"),("MTK","Metro cuadrado"),("11","Equipos"),("MGM","Miligramo"),("XPK","Paquete"),
                 ("XKI","Kit (Conjunto de piezas)"),("AS","Variedad"),("GRM","Gramo"),("PR","Par"),("DPC","Docenas de piezas"),
                 ("xun","Unidad"),("DAY","Día"),("XLT","Lote"),("10","Grupos"),("MLT","Mililitro"),("E54","Viaje"))
    #object to update
    obj_product = json.loads(json.dumps(product), object_hook = lambda d: SimpleNamespace(**d))
    
    if request.method == "POST":
        nombre = request.POST["nombreInt"]
        descripcion = request.POST['descripcion']
        claveProducto = request.POST['claveProducto']
        unidad = request.POST['unidad']
        
        product["Unit"] = dict(unitCodes).get(unidad)
        product["UnitCode"] = unidad
        product["Name"] = nombre
        product["Description"] = descripcion
        product["CodeProdServ"] = claveProducto

        try:
            facturama.Product.update(product,product["Id"])
            messages.add_message(request,  messages.SUCCESS, 'Producto actualizado exitosamente')   
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Hubo un error al actualizar el producto')
        return redirect("porte_producto_list")
    else:   
        return render(request, "cporte/porte_producto_update.html", {"css_list": css_list, "js_list": js_list, "userdict": userdict, "product": product, "unitCodes": unitCodes})

def porteProductoDelete(request, id):   
    try:
        facturama.Product.delete(id)
        messages.add_message(request,  messages.SUCCESS, 'Producto borrado exitosamente')
    except Exception as e:
        messages.add_message(request,  messages.ERROR, 'Hubo un error al borrar el product')
    return redirect("porte_producto_list")
    
def porteProducto(request):
    userdict = user_validation.validate(request)
    portecliente = request.user.portecliente_id
    unitCodes = (("H87","Pieza"),("EA","Elemento"),("E48","Unidad de Servicio"),("ACT","Actividad"),
                 ("KGM","Kilogramo"),("E51","Trabajo"),("A9","Tarifa"),("MTR","Metro"),("AB","Paquete a Granel"),
                 ("BB","Caja base"),("KT","Kit"),("SET","Conjunto"),("LTR","Litro"),("XBX","Caja"),("MON","Mes"),
                 ("HUR","Hora"),("MTK","Metro cuadrado"),("11","Equipos"),("MGM","Miligramo"),("XPK","Paquete"),
                 ("XKI","Kit (Conjunto de piezas)"),("AS","Variedad"),("GRM","Gramo"),("PR","Par"),("DPC","Docenas de piezas"),
                 ("xun","Unidad"),("DAY","Día"),("XLT","Lote"),("10","Grupos"),("MLT","Mililitro"),("E54","Viaje"))

    if request.method == "POST":
        nombre = request.POST["nombreInt"]
        descripcion = request.POST['descripcion']
        claveProducto = request.POST['claveProducto']
        unidad = request.POST['unidad']

        product_object = {
            "Unit": dict(unitCodes).get(unidad),
            "UnitCode": unidad,
            "IdentificationNumber": str(portecliente),
            "Name": nombre,
            "Description": descripcion,
            "Price": 0,
            "CodeProdServ": claveProducto,
            "CuentaPredial": "0",
            "Taxes": [
                {
                    "Name": "IVA Exento",
                    "Rate": 0,
                    "IsRetention": False,
                    "IsFederalTax": False
                }
            ]
        }

        try:
            facturama.Product.create(product_object)     
            messages.add_message(request,  messages.SUCCESS, 'Producto creado exitosamente')       
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Hubo un error al registrar el producto')
        return redirect("porte_producto_create")
    else:
        return render(request, "cporte/porte_productos_form.html", {"css_list": css_list, "js_list": js_list, "userdict": userdict, "unitCodes": unitCodes})
"""

def porteFacturaList(request):
    cfdis = PorteCarta.objects.filter(PorteReceiver__porteCliente_id = request.user.portecliente_id)
    return render(request, "cporte/porte_carta_list.html", {"css_list": css_list, "js_list": js_list, "cfdis": cfdis})

def porteFacturaDelete(request, id):
    PorteCarta.objects.get(id=id).delete()
    messages.add_message(request,  messages.SUCCESS, "Se ha eliminado su CFDI con éxito")       
    return redirect("cporte:porte_factura_list")

def porteFacturaUpdate(request, id):
    userdict = user_validation.validate(request)
    clientes = PorteReceiver.objects.filter(porteCliente_id=request.user.portecliente_id)
    figuras = PorteFigura.objects.filter(porteCliente_id=request.user.portecliente_id)
    factura = PorteCarta.objects.get(id=id)
    factura.json = json.dumps(factura.json)
    
    #FACTURAMA
    paises = facturama.CountriesCatalog.query()
    metodosPago = facturama.PaymentMethodsCatalog.query()
    monedas = facturama.CurrenciesCatalog.query()
    formasPago = facturama.PaymentFormsCatalog.query()

    #CARGAR CONFIG AUTO
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    configAuto = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/ConfigAutotransporte',headers=info)
    tipoVehiculo = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/CatalogTransportKey',headers=info)
    unidades = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/ClaveUnidadPeso',headers=info)

    return render(request, "cporte/porte_carta_form.html", {"css_list": css_list, "js_list": new_js_list, "factura": factura, "paises": paises, "metodosPago": metodosPago, "monedas":monedas, "formasPago":formasPago, "configAuto":configAuto.json(), "tipoVehiculo":tipoVehiculo.json(),"clientes":clientes,"figuras": figuras,"userdict":userdict,"unidades":unidades.json()})

def porteFactura(request):
    userdict = user_validation.validate(request)
    clientes = PorteReceiver.objects.filter(porteCliente_id=request.user.portecliente_id)
    figuras = PorteFigura.objects.filter(porteCliente_id=request.user.portecliente_id)
    
    #FACTURAMA
    paises = facturama.CountriesCatalog.query()
    metodosPago = facturama.PaymentMethodsCatalog.query()
    monedas = facturama.CurrenciesCatalog.query()
    formasPago = facturama.PaymentFormsCatalog.query()
  
    #CARGAR CONFIG AUTO
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    configAuto = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/ConfigAutotransporte',headers=info)
    #permisos = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/TipoPermiso',headers=info)
    tipoVehiculo = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/CatalogTransportKey',headers=info)
    unidades = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/ClaveUnidadPeso',headers=info)

    if request.is_ajax and request.method == "POST":
        storeOk = True
        data = json.loads(request.body.decode("utf-8"))
        
        #Agregando campos a issuer
        issuer = PorteCliente.objects.get(id=request.user.portecliente_id)
        
        try:
            folio = PorteCarta.objects.latest("id").pk + 1
        except:
            folio = 1

        #data["data"]["LogoUrl"] = "http://192.168.1.118:8001/media/" + str(issuer.path_img) 
        data["data"]["LogoUrl"] = "https://panoptic.com.mx/static/core/assets/images/AGUILASCORP.png"
        data["data"]["Folio"] = folio
        jsonreceiver = data["data"]["Issuer"]
        jsonreceiver["FiscalRegime"] = issuer.regimen_fiscal
        jsonreceiver["Name"] = issuer.razon_social
        jsonreceiver["Rfc"] = issuer.rfc
        jsonreceiver = jsonreceiver["Address"]
        jsonreceiver["Street"] = issuer.calle
        jsonreceiver["ExteriorNumber"] = issuer.exterior
        jsonreceiver["InteriorNumber"] = issuer.interior
        jsonreceiver["Neighborhood"] = issuer.colonia
        jsonreceiver["ZipCode"] = issuer.cp
        jsonreceiver["Locality"] = issuer.localidad
        jsonreceiver["Municipality"] = issuer.municipio
        jsonreceiver["State"] = issuer.estado
        jsonreceiver["Country"] = issuer.pais

        #Agregando campos a receiver
        receiver = PorteReceiver.objects.get(id = data["idreceiver"])
        jsonreceiver = data["data"]["Receiver"]
        jsonreceiver["Name"] = receiver.razon_social
        jsonreceiver["CfdiUse"] = "P01"
        jsonreceiver["Rfc"] = receiver.rfc
        jsonreceiver = jsonreceiver["Address"]
        jsonreceiver["Street"] = receiver.calle
        jsonreceiver["ExteriorNumber"] = receiver.exterior
        jsonreceiver["InteriorNumber"] = receiver.interior
        jsonreceiver["Neighborhood"] = receiver.colonia
        jsonreceiver["ZipCode"] = receiver.cp
        jsonreceiver["Locality"] = receiver.localidad
        jsonreceiver["Municipality"] = receiver.municipio
        jsonreceiver["State"] = receiver.estado
        jsonreceiver["Country"] = receiver.pais

        #Calculando Taxes
        if data["data"]["CfdiType"] == "I":

            for tax in data["data"]["Items"][0]["Taxes"]:
                if tax["Rate"] == "-":
                    print("delete")
                else:
                    tax["Total"] = float(tax["Base"]) * float(tax["Rate"])
                    if tax["Name"] == "IVA RET":
                        data["data"]["Items"][0]["Total"] = float(data["data"]["Items"][0]["Total"]) - float(tax["Total"])
                    else:
                        data["data"]["Items"][0]["Total"] = float(data["data"]["Items"][0]["Total"]) + float(tax["Total"])

            """
            if data["data"]["Items"][0]["Taxes"][1]:
                jsonIvaRet = data["data"]["Items"][0]["Taxes"][1]
                jsonIvaRet["Total"] = float(jsonIvaRet["Base"]) * float(jsonIvaRet["Rate"])
                data["data"]["Items"][0]["Total"] = float(data["data"]["Items"][0]["Total"]) + float(jsonIvaRet["Total"])

            jsonreceiver = data["data"]["Items"][0]["Taxes"][0]
            if jsonreceiver["Rate"] == "-":
                print("delete taxes")
            else:
                jsonreceiver["Total"] = float(jsonreceiver["Base"]) * float(jsonreceiver["Rate"])
                data["data"]["Items"][0]["Total"] += float(jsonreceiver["Total"])
            """

        # If json have ID in update, make a query. If is false, create a new object
        if not data["update"]: 
            factura = PorteCarta()
            msg = "Factura almacenada exitosamente"
        else:
            msg = "Factura actualizada exitosamente"
            factura = PorteCarta.objects.get(id=data["update"])   
        
        factura.json = data["data"]
        factura.PorteReceiver_id = data["idreceiver"]
        factura.figura = data["figura"]
        factura.origen = data["origen"]
        factura.destino = data["destino"]
        factura.status = data["status"]

        if data["status"] == "1":
            print("entre")
            try:
                res = facturama.CfdiMultiEmisor.create(data["data"])
                messages.add_message(request,  messages.SUCCESS, 'Factura creada exitosamente') 
                factura.pdf = facturama.CfdiMultiEmisor.get_by_file("pdf","issuedLite",res["Id"])["Content"]
                st = 200
            except Exception as e:
                storeOk = False
                st = 400
                if data["update"]:
                    factura.status = 0
                messages.add_message(request, messages.ERROR, e)
        else:
            st = 200
            messages.add_message(request, messages.SUCCESS, msg)       
        
        if storeOk or data["update"]:
            factura.save() 

        return JsonResponse({"message": "factura ok"}, status=st)

    else:
        return render(request, "cporte/porte_carta_form.html", {"css_list": css_list, "js_list": new_js_list, "paises": paises, "metodosPago": metodosPago, "monedas":monedas, "formasPago":formasPago, "configAuto":configAuto.json(), "tipoVehiculo":tipoVehiculo.json(),"clientes":clientes,"figuras": figuras,"userdict":userdict,"unidades":unidades.json()})

def getTipoRemolques(request):
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    trailerType = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/SubTipoRemolque', headers=info)
    context = {
        "tipoRemolque":trailerType.json()
    }
    return render(request, 'cporte/remolques_form.html', context)

def getPostalCode(request):
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    
    try:
        codigoPostal = facturama.PostalCodesCatalog.query("keyword="+request.GET["cp"])
        #colonia = requests.get('https://apisandbox.facturama.mx/api/catalogs/neighborhoods?postalCode='+request.GET['cp'],headers=info)
        #estado = requests.get('https://apisandbox.facturama.mx/api/catalogs/municipalities?stateCode='+codigoPostal[0]["StateCode"], headers=info)
        return JsonResponse({
            "codigo":codigoPostal,
            #"colonias": colonia.json(),
            #"estados": estado.json()
        }, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": "Hubo un error"}, status=400)

def getProductoServicioCode(request):
    try:
        units = facturama.UnitsCatalog.query("keyword="+request.GET['keyword'])
        return JsonResponse({
            "units": units
        }, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error":"Hubo un error"}, status=400)

def getClaveProducto(request):
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    try:
        clave = requests.get('https://apisandbox.facturama.mx/api/catalogs/ProductsOrServices?keyword='+request.GET['keyword'], headers=info)
        print(clave.status_code)
        if(clave.status_code == 400):
            raise Exception()

        return JsonResponse({
            "claves": clave.json()
        }, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error":"Hubo un error"},status=400)

def getUbicacion(request):
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    try:
        colonia = requests.get('https://apisandbox.facturama.mx/api/catalogs/neighborhoods?postalCode='+request.GET['cp'],headers=info)
        municipios = requests.get('https://apisandbox.facturama.mx/api/catalogs/municipalities?stateCode='+request.GET["state_code"], headers=info)
        estados = requests.get('https://apisandbox.facturama.mx/api/catalogs/states?countryCode=MEX',headers=info)
        return JsonResponse({
            "colonias": colonia.json(),
            "municipios": municipios.json(),
            "estados": estados.json()
        },status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error":"Hubo un error"},status=400)

def porteFiguraList(request):
    figuras = PorteFigura.objects.filter(porteCliente_id = request.user.portecliente_id)
    return render(request, "cporte/porte_figura_list.html", {"css_list": css_list, "js_list": js_list, "figuras": figuras})

def porteFiguraCreate(request):
    userdict = user_validation.validate(request)
    paises = facturama.CountriesCatalog.query()

    if request.is_ajax and request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        cliente = PorteCliente.objects.get(id = request.user.portecliente_id)
        figura = PorteFigura()
        figura.porteCliente = cliente
        figura.tipo = data["tipo"]
        figura.nombre = data["nombre"]
        figura.rfc = data["rfc"]
        figura.licencia = data["licencia"]
        figura.pais = data["pais"]
        figura.cp = data["cp"]
        figura.municipio = data["municipio"]
        figura.estado = data["estado"]
        figura.colonia = data["colonia"]
        figura.calle = data["calle"]
        figura.ext = data["numExterior"]
        figura.int = data["numInterior"]
        figura.referencia = data["referencias"]

        try:
            figura.save()
            messages.add_message(request, messages.SUCCESS, 'Registro Existoso!')
            return JsonResponse({"message": "Figura creada"}, status=200)
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Hubo un error al registrar al chofer')
            return redirect("porte_producto_create")
    else:
        return render(request, "cporte/porte_figura_form.html", {"css_list": css_list, "js_list": js_list,"userdict":userdict, "paises":paises})

def ajax_get_figura(request):
    figura = PorteFigura.objects.get(id=request.GET.get("figura_id"))
    jsonFigura = {
        "TipoFigura": figura.tipo,
        "RFCFigura": figura.rfc,
        "NombreFigura": figura.nombre,
        "NumLicencia": figura.licencia,
        "Domicilio": {
            "Pais": figura.pais,
            "CodigoPostal": figura.cp,
            "Estado": figura.estado,
            "Municipio": figura.municipio,
            "Colonia": figura.colonia,
            "Calle": figura.calle,
            "NumeroExterior": figura.ext,
            "NumeroInterior": figura.int,
            "Referencia": figura.referencia
        }
    }

    return JsonResponse(jsonFigura, status=200, safe=False)

def updateFigura(request, id):
    userdict = user_validation.validate(request)
    paises = facturama.CountriesCatalog.query()
    idx = id
    figura = PorteFigura.objects.get(id=idx)
    
    if request.is_ajax and request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        figura.tipo = data["tipo"]
        figura.nombre = data["nombre"]
        figura.rfc = data["rfc"]
        figura.licencia = data["licencia"]
        figura.pais = data["pais"]
        figura.cp = data["cp"]
        figura.municipio = data["municipio"]
        figura.estado = data["estado"]
        figura.colonia = data["colonia"]
        figura.calle = data["calle"]
        figura.ext = data["numExterior"]
        figura.int = data["numInterior"]
        figura.referencia = data["referencias"]
        try:
            figura.save()
            messages.add_message(request, messages.SUCCESS, 'Actulizacion exitosa!')
            return JsonResponse({"message": "Figura creada"}, status=200)
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Hubo un error al registrar al chofer')
            return redirect("porte_producto_create")
    else:
        return render(request,"cporte/porte_figura_update.html", {"css_list": css_list, "js_list": js_list,"userdict":userdict, "figura":figura,"paises":paises})

def updatePermiso(request):
    userdict = user_validation.validate(request)
    info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
    permisos = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/TipoPermiso',headers=info)

    cliente = PorteCliente.objects.get(id = request.user.portecliente_id)
    tipoPermiso = cliente.tipoPermiso
    numPermiso = cliente.numPermiso

    if request.is_ajax and request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        cliente.tipoPermiso = data["tipoPermiso"]
        cliente.numPermiso = data["numPermiso"]
        try:
            cliente.save()
            messages.add_message(request, messages.SUCCESS, 'Actulizacion exitosa!')
            return JsonResponse({"message": "Figura creada"}, status=200)
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Hubo un error al actualizar el permiso')
            return redirect("porte_permiso_update")
    else:
        return render(request,"cporte/porte_permiso_form.html", {"css_list": css_list, "js_list": js_list,"userdict":userdict,"permisos":permisos.json(),"tipoPermiso":tipoPermiso,"numPermiso":numPermiso})
