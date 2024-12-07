from . import models 
from django.http import JsonResponse
from .Options import Options
from datetime import datetime

def Sale_Delete(request):
      sale_delete = models.Sale.objects.get(id=request.GET.get('sale_id'))
      sale_delete.delete()
      return JsonResponse(list(),  safe=False)



def DeleteService(request):
      s = models.ServiceImage.objects.get(id=request.GET.get('s_id'))
      s.delete()
      return JsonResponse(list(),  safe=False)

def DeleteMomentImage(request):
      m = models.MomentImage.objects.get(id=request.GET.get('m_id'))
      m.delete()
      return JsonResponse(list(),  safe=False)


def DeledeteImgMoment(request):
      m = models.MomentRelatedImage.objects.get(id=request.GET.get('delete_img_moment_id'))
      print(m.id)
      m.delete()
      return JsonResponse(list(),  safe=False)



def DeletePlans(request):
      p = models.Plans.objects.get(id=request.GET.get('p_id'))
      p.delete()
      return JsonResponse(list(),  safe=False)


def CreateCaract(request):
      try:
            p = models.Plans.objects.get(id=request.GET.get('id'))
            cr = models.CaratPlanes.objects.create(plans=p, name=request.GET.get('input'))
            caract_list = []
            dick  =  {
                        'id': p.id,
                        'name': p.name
            }
                  
            return JsonResponse(dick,  safe=False)
      except models.Plans.DoesNotExist:
            pass
      return JsonResponse(caract_list,  safe=False)


def DeleteCaract(request):
      cr = models.CaratPlanes.objects.get(id=int(request.GET.get('id')),)
      cr.delete()
      return JsonResponse(list(),  safe=False)

def Reserver(request):
      sale = models.Sale.objects.get(id=request.GET.get('id'))

      if sale.reserver == False:
            sale.reserver = True
            sale.reserver_mount = int(request.GET.get('input'))
            sale.abonado =  sale.plan.price -  sale.reserver_mount 
            sale.save()
            Options.Guardar_Ingreso(sale,int(request.GET.get('input')), ' - Abono'  )     

      else:

            Options.Guardar_Ingreso(sale,int(request.GET.get('input')), ' - Abono' )  
            print('depuración')
            abonado =   sale.reserver_mount  + int(request.GET.get('input'))
            sale.reserver_mount = abonado
            sale.abonado =   sale.plan.price -  sale.reserver_mount
            sale.save()
      if sale.reserver_mount >=  sale.plan.price:
            
            sale.saled = True
            sale.save() 
      return JsonResponse(list(),  safe=False)

def SaleService(request):
      c = models.Customer.objects.get(id=request.GET.get('id'))
      print(c.id)

      if c.saled == False:
            c.saled = True
            c.saled_mount = c.plans.price
            c.save()
            print(c.id)
      return JsonResponse(list(),  safe=False)


def SaleCancel(request):
      c = models.Customer.objects.get(id=request.GET.get('id'))

      if c.reserve == True:
            c.reserve = False
            c.save()
      return JsonResponse(list(),  safe=False)



def Search(request):
      lista = []
      # sale =''
      for s in models.Customer.objects.all():
            dict_customer = { 
                        'id': s.id,
                        'name': s.name,
                     'name_search': (s.name or "") + (s.email or "") + (s.date_only_choice.strftime('%d/%m/%Y') if s.date_only_choice else "")
      
            }

            # models.Sale.objects.get(cliente=s),
            # sale = 

            lista.append(dict_customer)
      return JsonResponse(lista,  safe=False)

def SearchingClient(request):
      sale = models.Customer.objects.get(id=int(request.GET.get('id')))
      # Obtener todos los planes asociados a ese cliente específico
      # Obtener todos los planes asociados a ese cliente específico

      dict_client = { 
            'id': cliente.id,
            'name': cliente.name, 
            'email': cliente.email,
            'number': cliente.number,
            'sale': id,
      }
      return JsonResponse(dict_client,  safe=False)         

def Adicionales(request):
      # Obtener el plan
      plan = models.Plans.objects.get(id=int(request.GET.get('id')))


# Get all additional features associated with the plan

      # Verificar si el plan tiene adicionales
      lista = []
      if plan.adicionales.exists():
            adicionales = models.Adicionales.objects.filter(plans=plan)
            for a in adicionales:
                  dict_client = { 
                        'description': a.description ,

                  }
                  lista.append(dict_client)

      # pln = models.Plans.objects.filter(id=int(request.GET.get('id')))

      return JsonResponse(lista,  safe=False)         

def CreateAdicionales(request):
      print(request.GET.get('id'))

      p = models.Plans.objects.get(id=request.GET.get('id'))
      adicional = models.Adicionales(plans=p, 
                  description=request.GET.get('input'))
      adicional.save()
      adicionales_list = []

      return JsonResponse(adicionales_list,  safe=False)    


def Create_P_Adicionales(request):

      p = models.Plans.objects.get(id=request.GET.get('id'))
      p.final_price = int(request.GET.get('input'))
      
      p.save()
      adicionales_list = []
      return JsonResponse(adicionales_list,  safe=False)    


def Terminar_Cita(request):
      sale = models.Sale.objects.get(id=request.GET.get('id'))
      sale.saled_confirm = True
      sale.save()


      Options.Guardar_Ingreso(sale,sale.price_total, ' - Saldado' )       
   
      
      return JsonResponse(list(),  safe=False)          

def AgregarOpcion(request):
      pack_options = models.PackOpciones.objects.get(id=int(request.GET.get('pack_options_id')))
      sale = models.Sale.objects.get(id=int(request.GET.get('saled_id')))
      options = models.Opciones(
            sale=sale,
            name = pack_options.name,
            preci = pack_options.preci,
            description = pack_options.description,
            )
      options.save()
      return JsonResponse(list(),  safe=False)

def DeleteOption(request):
      option = models.Opciones.objects.get(id=request.GET.get('option_id'))
      option.delete()
      return JsonResponse(list(), safe=False)


def DeletePaquetOption(request):
      option = models.PackOpciones.objects.get(id=request.GET.get('option_id'))
      option.delete()
      return JsonResponse(list(), safe=False)


def CreateOption(request):
      sale = models.Sale.objects.get(id=int(request.GET.get('saled_id')))
      
      if request.GET.get('price'):
            price = int(request.GET.get('price').replace(',', '')) 
      options = models.Opciones(
            sale=sale,
            name = request.GET.get('name'),
            preci = price,
            description = request.GET.get('description'),
            )
      options.save()
      return JsonResponse(list(),  safe=False)

import pytz
def CheckCitasToDay(request):
      date_to_day =  request.GET.get('date')
      if date_to_day:


                  # Convierte la fecha recibida a un objeto datetime
            print(date_to_day)
            date_obj = datetime.strptime(date_to_day, "%Y-%m-%d").date()
            print("Fecha procesada correctamente:", date_obj)
            date_only = date_obj
                  # Asegúrate de obtener solo la fecha de `date_obj`
            hours_list = [
                  '08:00', '09:00', '10:00', '11:00', '12:00',
                  '1:00', '2:00', '3:00', '4:00', '5:00'
                  ]
            list_to_day_sale = []
            # Realiza la consulta usando el filtro adecuado
            sale_to_day = models.Sale.objects.filter(cliente__date_only_choice=date_only)
            print(sale_to_day)
            if sale_to_day:
                  for to_day in sale_to_day:
                        # Verifica si la hora ya está en la lista
                        time_choice = to_day.cliente.date_time_choice.strftime('%H:%M')  # Formato de la hora, si es necesario


                        # Si la hora no está en la lista, la agrega
                        if not any(item['hors'] == time_choice for item in list_to_day_sale):
                              dict_to_day = {
                              'hors': time_choice,
                              }
                              list_to_day_sale.append(dict_to_day)

            for sale in list_to_day_sale:
                  if sale['hors'] in hours_list:
                        hours_list.remove(sale['hors'])
      return JsonResponse(hours_list,  safe=False)