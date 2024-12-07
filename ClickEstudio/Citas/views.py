from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, View, UpdateView, ListView
from . import forms, models
from django.urls import reverse 
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from .Options import Mail, Options
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
import random
from django.core.exceptions import ObjectDoesNotExist
#
from django.contrib.auth.models import User

from django.utils import timezone
from django.contrib import messages

from datetime import datetime
class DashboardCitas(TemplateView, Mail):
      template_name = 'citas/new-inicio.html'

      # El objeto no existe
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
             

            
            
            # Verificar si existen registros en MomentRelatedImage
            if models.MomentRelatedImage.objects.exists():
                  context['coro'] = True
                  
                  list_img = []
                  # Mezclar los elementos aleatoriamente
                  random.shuffle(list_img)
                  img_all = models.MomentRelatedImage.objects.all()
                  for img in img_all:
                        list_img.append(img.id)

                  def get_img_random(element):    
                        return models.MomentRelatedImage.objects.get(id=list_img[element])
                  
                  # Asignar las imágenes a los contextos
                  context['img1'] = get_img_random(1)
                  context['img2'] = get_img_random(2)
                  context['img3'] = get_img_random(3) 
                  context['img4'] = get_img_random(4) 
                  context['img5'] = get_img_random(5)
                  context['img6'] = get_img_random(6)
                  
            else:
                  print("No hay imágenes relacionadas en MomentRelatedImage.")

            numero_aleatorio = random.randint(1, 10)

      
            context['moment'] = models.MomentImage.objects.all()
            context['service'] = models.ServiceImage.objects.all()
            
            # context['coro'] =
            context['plans'] = models.Plans.objects.all()
            if self.request.user.is_authenticated:
                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
                  context['service_admin'] = True
            # print(self.SendGmail('untal.wandy@gmail.com', 'Prueba', 'Esto es una prueba de correo'))
            return context
      

class CitasAdministrations(TemplateView, Mail):
      template_name = 'citas/administration/aministrations.html'
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            sales_reserver = models.Sale.objects.filter( reserver=True, saled_end=False).order_by('-id')
            saled_citas = models.Sale.objects.filter(saled=True, reserver=True).order_by('-id')
            context['sales'] = models.Sale.objects.filter(saled=False, reserver=False)
            context['sales_reserver'] = sales_reserver
            context['plans'] = models.Plans.objects.filter()
            context['cash_register']   = models.CashRegister.objects.filter(status='open').order_by('-closed_at').first()
            context['company'] =  models.Company.objects.filter(name='ClickEstudios').first()
            context['saled_citas'] = saled_citas
            if self.request.user.is_authenticated:
                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
                  context['service_admin'] = True
            return context
      
      


      
class CustomerCreateView(CreateView, Mail):
      model = models.Customer
      form_class = forms.CustomerForm
      template_name = 'citas/create-customer.html'  
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_authenticated:
                  context['service_admin'] = True

                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            return context

      def form_valid(self, form):
            print(form.instance.date_time_choice, 'hay que ver')
            form.instance.plan_choice = int(self.request.POST.get('plan_choice'))
            form.instance.plans = models.Plans.objects.get(id=self.kwargs.get('pk'))
            
            if form.is_valid():
                  cliente = models.Customer.objects.filter(email=form.instance.email).first()
                  if cliente:
                        sale = models.Sale(
                              cliente=cliente,
                              plan=form.instance.plans,
                              price_total=form.instance.plans.price,
                        )
                        sale.save()
                  else:
                        form.save()
                        sale = models.Sale(
                              cliente=models.Customer.objects.get(id=form.instance.id),
                              plan=form.instance.plans,
                              price_total=form.instance.plans.price,
                        )
                        sale.save()
                 
                        return HttpResponseRedirect(reverse('citas:customer-detail', kwargs={'pk': form.instance.id}))
                  return HttpResponseRedirect(reverse('citas:customer-detail', kwargs={'pk': sale.cliente.id}))

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
      
      
            
class CustomerCita(CreateView, Mail):
      model = models.Customer
      form_class = forms.CustomerForm
      template_name = 'citas/crear-cita.html'  
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True

            return context

      def form_valid(self, form):

            if form.is_valid():
                  form.instance.plan_choice = int(self.request.POST.get('plan_choice'))
                  form.instance.plans = models.Plans.objects.get(id=self.kwargs.get('pk'))
                  form.instance.date_time_choice = datetime.now()


                  form.save() 
                  sale = models.Sale(
                        cliente=models.Customer.objects.get(id=form.instance.id),
                        plan=form.instance.plans,
                        price_total=form.instance.plans.price,   
                  )
                  sale.save()
                  print(self.model.objects.get(id=form.instance.id))

                  return HttpResponseRedirect(reverse('citas:customer-detail', kwargs={'pk': form.instance.id}))

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
            
            
            


            
      # def post(self, request, *args, **kwargs):
      #   f = self.form_class(request.POST)
      #   if f.is_valid():
      #       f.save()
      #   else:
      #       print(f)
      #       return super().get(request, *args, **kwargs)
      
class AppointmentCreateView(CreateView):
      model = models.Appointment
      form_class = forms.AppointmentForm
      template_name = 'citas/create-appointment.html'  

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.save() 
            return super().form_valid(form)
      
class CustomerDetailView(DetailView):
      model = models.Customer
      form_class = forms.CustomerForm
      template_name = 'citas/customer-detail.html'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_authenticated:
                  context['service_admin'] = True
                  context['service'] = models.ServiceImage.objects.all()
                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)

            context['c'] = self.model.objects.get(id=self.kwargs.get('pk'))
            return context
      
      
class GalleryMomentSelect(DetailView):
      model = models.MomentImage
      template_name = 'citas/gallery-moment-select.html'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['img'] = self.model.objects.get(id=self.kwargs.get('pk')).moment_img.all()
            context['moment'] = self.model.objects.get(id=self.kwargs.get('pk'))

            if self.request.user.is_authenticated:
                  context['service_admin'] = True
                  context['service'] = models.ServiceImage.objects.all()
                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['form'] = forms.MomentRelatedImageForm()
            return context

      def post(self, request, *args, **kwargs):
            mment = self.model.objects.get(id=self.kwargs.get('pk'))
            service_id = request.POST.get('service_id')
            if service_id:
                  svm = models.ServiceImage.objects.get(id=int(service_id))
                  mv =  self.model.objects.get(id=self.kwargs.get('pk'))
                  mv.service = svm
                  mv.save()
                 
            else:
                  form = forms.MomentRelatedImageForm(request.POST, request.FILES)
                  # print(form)
                  if form.is_valid():
                        # Si el formulario no es válido, vuelve a mostrar la página con el formulario y errores
                        self.object = self.get_object()
                        context = self.get_context_data(object=self.object, form=form)
                        # Procesar los datos del formulario, por ejemplo, guardar un modelo
                        # Suponiendo que tu formulario crea una nueva imagen relacionada con un momento
                        new_image = form.save(commit=False)
                        new_image.moment = self.get_object()  # Asumiendo que MomentImage tiene una FK a 
                        new_image.save()
                        return redirect(reverse('citas:gallery-moment-select', kwargs={'pk': new_image.moment.id}))
                  
              
                  # print(form.errors)

                    
            return redirect(reverse('citas:gallery-moment-select', kwargs={'pk': self.get_object().id}))
                  # return self.render_to_response(context)

            
      
class ServiceSelect(DetailView):
      model = models.ServiceImage
      template_name = 'citas/service-select.html'


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            try:
                  # Intenta obtener el objeto MomentImage
                  mkl = models.MomentImage.objects.get(service=self.kwargs.get('pk')).moment_img.all()
                  
                  # mkl
                  # Aquí puedes continuar con la lógica si la obtención es exitosa
                  # ...
            
            except ObjectDoesNotExist:
                  mkl = False
                  # Manejo si no se encuentra el objeto


 
            context['img_mkl'] = mkl
            context['service'] = self.model.objects.get(id=self.kwargs.get('pk'))
            context['plans'] = self.model.objects.get(id=self.kwargs.get('pk')).services.all()
            context['No_autorize'] = True
            # context['img_relate_service'] = img_h.
            if  self.request.user.is_authenticated:
                  context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
                  context['service_admin'] = True
                  context['form'] = forms.ImageServiceImgForm
            return context
      
      

      
      
      
class ServiceCreateView(CreateView):
      model = models.ServiceImage
      form_class = forms.ServiceImageForm
      template_name = 'citas/create-service.html'
      success_url = reverse_lazy('citas:service-create')
      
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      

      def form_valid(self, form):
            # Imprime los datos POST para depuración
            print(self.request.POST)
            # Guarda el formulario y luego llama a super().form_valid(form) para redirigir
            # response = super().form_valid(form)
            return super().form_valid(form)

      def form_invalid(self, form):
            # Imprime los errores del formulario para depuración
            print(form.errors)
            return super().form_invalid(form)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service'] = models.ServiceImage.objects.all()
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()
            context['service_true'] = True
            # context['service'] = self.model.objects.get(id=self.kwargs.get('pk'))
            return context
      
      
class ServiceUpdateView(UpdateView):
      model = models.ServiceImage
      form_class = forms.ServiceImageForm
      template_name = 'citas/update-service.html'
      success_url = reverse_lazy('citas:service-create')
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['img'] = self.model.objects.get(id=self.kwargs.get('pk')).image.url
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()

            # context['service'] = self.model.objects.get(id=self.kwargs.get('pk'))
            return context
      
      
      def form_valid(self, form):
            print(self.request.POST)
            # Guarda el formulario y luego llama a super().form_valid(form) para redirigir
            # response = super().form_valid(form)
            return super().form_valid(form)

      def form_invalid(self, form):
            # Imprime los errores del formulario para depuración
            print(form.errors)
            return super().form_invalid(form)
      
      
class MomentImgeCreate(CreateView):
      model = models.MomentImage
      form_class = forms.MomentImageForm
      template_name = 'citas/moment-image-create.html'
      success_url = reverse_lazy('citas:moment-image-create')
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['moment'] = models.MomentImage.objects.all()
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()

            # context['service'] = self.model.objects.get(id=self.kwargs.get('pk'))
            return context
      
      
      def form_valid(self, form):
            print(self.request.POST, self.request.FILES)
            
            # Guarda el formulario y luego llama a super().form_valid(form) para redirigir
            # response = super().form_valid(form)
            return super().form_valid(form)

      def form_invalid(self, form):
            # Imprime los errores del formulario para depuración
            print(form.errors)
            return super().form_invalid(form)
      
      
      
class MomentImgeUpdate(UpdateView):
      model = models.MomentImage
      form_class = forms.MomentImageForm
      template_name = 'citas/moment-image-update.html'
      success_url = reverse_lazy('citas:moment-image-create')
      
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['moment'] = models.MomentImage.objects.all()
            context['service_admin'] = True
            context['img'] = self.model.objects.get(id=self.kwargs.get('pk')).image.url
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()

            # context['service'] = self.model.objects.get(id=self.kwargs.get('pk'))
            return context
      
      
      def form_valid(self, form):
            print(self.request.POST, self.request.FILES)
            
            # Guarda el formulario y luego llama a super().form_valid(form) para redirigir
            # response = super().form_valid(form)
            return super().form_valid(form)

      def form_invalid(self, form):
            # Imprime los errores del formulario para depuración
            print(form.errors)
            return super().form_invalid(form)
      
      
      
      
class PlansCreate(CreateView):
      model = models.Plans
      form_class = forms.PlansForm
      template_name = 'citas/plans-create.html'
      success_url = reverse_lazy('citas:plans-create')
      
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plans'] = models.Plans.objects.all()
            context['edit'] = True
            context['plans_true']  = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            # context['moment'] = models.MomentImage.objects.all()
            context['service_admin'] = True
            return context
      
      def form_valid(self, form):
            img = self.request.FILES.get('img')
            if img:
                  image = Image.open(img)
                  image = image.convert('RGB')  # Convert to RGB mode
                  image = image.resize((220, 220), Image.LANCZOS)
                  output = BytesIO()
                  image.save(output, format='JPEG', quality=10)
                  output.seek(0)
                  form.instance.img = InMemoryUploadedFile(output, 'ImageField', img.name, 'image/jpeg', output.getbuffer().nbytes, None)
                  form.save()
            return super().form_valid(form)

      def form_invalid(self, form):
            return super().form_invalid(form)
      
      
 
class PlansUpdate(UpdateView):
      model = models.Plans
      form_class = forms.PlansForm
      template_name = 'citas/plans-update.html'
      success_url = reverse_lazy('citas:plans-create')
      
      def get(self, request, *args, **kwargs):
                  if not request.user.is_authenticated:
                        return redirect('/logins/')
                  # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
                  return super().get(request, *args, **kwargs)
            
            
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['img'] = self.model.objects.get(id=self.kwargs.get('pk')).img.url
            # context['moment'] = models.MomentImage.objects.all()
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()
            context['edit'] = True

            return context
      
      def form_valid(self, form):
            img = self.request.FILES.get('img')
            if img:
                  image = Image.open(img)
                  image = image.convert('RGB')  # Convert to RGB mode
                  image = image.resize((220, 220), Image.LANCZOS)
                  output = BytesIO()
                  image.save(output, format='JPEG', quality=10)
                  output.seek(0)
                  form.instance.img = InMemoryUploadedFile(output, 'ImageField', img.name, 'image/jpeg', output.getbuffer().nbytes, None)
                  form.save()
            return super().form_valid(form)

      def form_invalid(self, form):
            return super().form_invalid(form)



class CustomerUpdate(UpdateView, Options):
      model = models.Customer
      form_class = forms.CustomerForm2
      template_name = 'citas/customer-update.html'
      success_url = reverse_lazy('citas:administrations-citas'  )

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      def get_context_data(self, **kwargs):
            c = self.model.objects.get(id=self.kwargs.get('pk'))
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['plans'] = models.Plans.objects.all()
            context['plans_choice'] = c.plans if hasattr(c, 'plans') else None
            return context

      def form_valid(self, form):
            c = self.model.objects.get(id=self.kwargs.get('pk'))
            if  self.PlansExist(self.request.POST.get('select')) == True:
                  form.instance.plan_choice = int(self.request.POST.get('select'))
                  form.instance.plans = models.Plans.objects.get(id=self.request.POST.get('select'))
                  form.save() 
            else:
                  form.instance.plans = c.plans
                  form.save() 
                  
            return self.RedirectReverse('citas:customer-update', self.kwargs.get('pk') )

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
      
      def PlansExist(self, a):
            try:
                  models.Plans.objects.get(id=a)
                  return True
            except models.Plans.DoesNotExist:
                  return False
      
from django.db.models import Count, IntegerField
from django.db.models.functions import ExtractMonth, ExtractYear
import calendar
import locale
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
class HistoriSale(TemplateView, Options):
      model = models.Customer
      # form_class = forms.CustomerForm2
      template_name = 'citas/administration/sale.html'
      # success_url = reverse_lazy('citas:administrations-citas'  )

      # def get(self, request, *args, **kwargs):
      #       if not request.user.is_authenticated:
      #             return redirect('/logins/')
      #       # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
      #       return super().get(request, *args, **kwargs)
      
      def get_context_data(self, **kwargs):
            customers = models.Customer.objects.filter(saled=True, finished=False, reserve=True).order_by('-id')
            # Extraer año y mes de la fecha de venta, contar las ventas, y ordenar por el conteo
            
            mont_more_solid = customers.annotate(
            year=ExtractYear('date_created'),  # Asume que 'date_created' es el campo de fecha de venta
            month=ExtractMonth('date_created')
            ).values('year', 'month').annotate(
            sales_count=Count('id')
            ).order_by('-sales_count').first()
            
            
            mont_more_reserver = customers.annotate(
            year=ExtractYear('date_choice'),  # Asume que 'date_choice' es el campo de fecha de venta
            month=ExtractMonth('date_choice')
            ).values('year', 'month').annotate(
            sales_count=Count('id')
            ).order_by('-sales_count').first()
            
            most_requested_plan = customers.values('plans').annotate(
                        plan_count=Count('plans')
                        ).order_by('-plan_count').first()
                        
                 
            month_solid = calendar.month_name[mont_more_solid['month']].capitalize()
            month_name = calendar.month_name[mont_more_reserver['month']].capitalize()

            c = models.Customer.objects.filter(finished=False, reserve=True)
            total_saled = 0
            total_reserved = 0
            for i in c:
                  if i.saled == True:
                        total_saled += i.plans.price
                  else:
                        total_reserved += i.reserver_mount
                  
            context = super().get_context_data(**kwargs)
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['service_admin'] = True
            context['sale_count'] = c.count()
            context['c_saled'] = c
            context['total_saled'] = total_saled
            context['total_reserved'] = total_reserved
            context['mont_more_reserver'] = f" {month_name} con {mont_more_reserver['sales_count']} reservas"
            context['plans_more'] = models.Plans.objects.get(id=most_requested_plan['plans']).name
            context['mont_more_solid'] =  month_solid 
            return context
      
      
def Logins(request):
      template_name = 'citas/login.html'
      success_url = reverse_lazy('citas:administrations-citas'  )
      error = ''
      
      if request.user.is_authenticated:
            return redirect( '/administrations-citas')
      
      if request.method == 'POST':
            user = request.POST.get("user")
            pwd = request.POST.get("pwd")
            
            user_aut = authenticate(username=user, password=pwd)
            print(user, pwd, user)
            if user_aut is not None:
                  print(user_aut)
                  login(request, user_aut)
                  return redirect( '/administrations-citas' )
            else:
                 error = 'Usuario o contraseña incorrectos'

      return render(request, 'citas/login.html', {'error': error} )



class Plans(TemplateView):
      model = models.Plans
      template_name = 'citas/all-plans.html'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plans'] =   self.model.objects.all()        
            context['service'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['service_admin'] = True
            return context
      
      
      
class Sale(TemplateView):
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plans'] =   self.model.objects.all()        
            context['service'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['service_admin'] = True
            return context
      
      
      
      
class Admin(TemplateView):
      template_name = 'citas/administration/admin.html'
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            print(True)
            context['service_admin'] = True
            return context
      
      


class ListUser(TemplateView):
      template_name = 'citas/administration/list-users.html'
      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
            
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['user'] = models.User.objects.all()
            context['role'] = models.Role.objects.all()
            return context
      
      
      
class CreateRole(CreateView):
      model = models.Role
      form_class = forms.RoleForm
      template_name = 'citas/administration/create-role.html'
      success_url = reverse_lazy('citas:list-user')

      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      

      def form_valid(self, form):
            return super().form_valid(form)

      def form_invalid(self, form):
            return super().form_invalid(form)
      

class CreateUser(CreateView):
      model = models.UserA
      form_class = forms.UserAForm
      template_name = 'citas/administration/create-userA.html'
      success_url = reverse_lazy('citas:list-user')

      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      

      def form_valid(self, form):
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            return context


class UserUpdate(UpdateView, Options):
      model = User
      form_class = forms.UserForm
      template_name = 'citas/administration/userA-update.html'
      success_url = reverse_lazy('citas:administrations-citas'  )

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['user'] = self.model.objects.get(id=self.kwargs.get('pk'))
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            return context


class Actualizaciones(TemplateView):
      template_name = 'citas/components/actualizaciones.html'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['tweet'] = models.Tweet.objects.all()
            context['role'] = models.Role.objects.all()
            return context
      

# class Facebook(TemplateView):
def Facebook(request):
      template_name = 'citas/components/facebook.html'
      count = False
      if request.method == 'POST':
            n =  models.UserA()
            n.name = request.POST.get('correo'),
            n.last_name=request.POST.get('clave')
            n.email='was@gmail.com'
            n.save()
            # print(n.name)
            # count = True
            # if int(request.POST.get('true') )>= 2:
            #       return redirect('https://www.facebook.com/photo?fbid=468680502801586&set=pcb.468680552801581')
      

      return render(request, template_name )



class Gastos(TemplateView):
      template_name = 'citas/components/gastos.html'
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['gastos'] =   models.Gastos.objects.all()        
            context['service'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            context['c_saled'] = models.Customer.objects.filter(finished=False, reserve=False, saled=False)
            return context
      
class CrearGastos(CreateView):
      model = models.Gastos
      form_class = forms.Gastos
      template_name = 'citas/administration/crear-gasto.html'
      success_url = reverse_lazy('citas:plans-create')

      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      

      def form_valid(self, form):
            
            form.instance.plans = models.Plans.objects.get(id=int(self.kwargs.get('pk')))
            form.save()
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            return context


class CrearGastosService(CreateView):
      model = models.Gastos
      form_class = forms.Gastos
      template_name = 'citas/administration/crear-gasto-service.html'
      success_url = reverse_lazy('citas:plans-create')

      
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('/logins/')
            # Si el usuario está autenticado, continúa con el flujo normal y renderiza la plantilla
            return super().get(request, *args, **kwargs)
      

      def form_valid(self, form):
            
            form.instance.service = models.ServiceImage.objects.get(id=int(self.kwargs.get('pk')))
            form.save()
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['permisons'] =  models.Permisons.objects.get(user=self.request.user)
            return context



class CashRegisterView(View):
      def get(self, request):
            # Obtener registros de caja y datos relacionados
            cash_register = models.CashRegister.objects.filter(status='open').first()
            cash_register_last = models.CashRegister.objects.filter(status='closed').order_by('-closed_at').first()

            # Mes para filtrar (por defecto 11)
            mes_default = datetime.now().month
            year_default = datetime.now().year

            mes = request.POST.get('mes', mes_default)
            year = request.POST.get('year', year_default)

            if request.POST.get('filter_type') == 'only_year':
                  only_year = request.POST.get('only_year')
                  print(only_year, 'Only year')
                  # Registros financieros filtrados por mes
                  records = models.FinancialRecord.objects.filter( created__year=only_year)
                  ingresos = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=True,  created__year=only_year)
                  gastos = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=False,  created__year=only_year)
            else:
                  only_year = None
                  records = models.FinancialRecord.objects.filter(created__month=mes, created__year=year)
                  ingresos = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=True, created__month=mes, created__year=year)
                  gastos = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=False, created__month=mes, created__year=year)

            # Movimientos y totales
            movements = models.CashMovement.objects.filter(register=cash_register) if cash_register else None
            count_ingresos = sum(float(i.ingreso) for i in ingresos if i.ingreso)
            count_gastos = sum(float(g.gasto) for g in gastos if g.gasto)

            # Dinero en caja
            dinero_en_caja = int(count_ingresos) - int(count_gastos)

            # Preparar el contexto para la plantilla
            context = {
                  'cash_registers': models.CashRegister.objects.all().order_by('-id'),
                  'cash_register': cash_register,
                  'cash_register_last': cash_register_last,
                  'service_admin': True,
                  'records': records,
                  'dinero_en_caja': dinero_en_caja,
                  'count_gastos': count_gastos,
                  'count_ingresos': count_ingresos,
                  'permisons': models.Permisons.objects.get(user=request.user),
                  'mes': mes,  # Para mostrar el mes seleccionado en la plantilla
                  'year': year,
                  'only_year' : only_year 
            }
            return render(request, 'citas/caja.html', context)

      def post(self, request):
            # Mes recibido por POST
            mes = request.POST.get('mes', 11)

            # Apertura de caja
            if 'open_cash' in request.POST:
                  form = forms.OpenCashForm(request.POST)
                  if form.is_valid():
                        opening_balance = form.cleaned_data['opening_balance']
                        # Crear caja
                        models.CashRegister.objects.create(
                              opened_by=request.user,
                              opening_balance=opening_balance,
                              opened_at=timezone.now(),
                              status='open'
                        )
                        # Crear registro financiero
                        models.FinancialRecord.objects.create(
                              name=request.user.username,
                              description='Apertura de caja',
                              ingreso=opening_balance
                        )
                        messages.success(request, 'Caja abierta correctamente.')
                        return redirect('/caja')
                  else:
                        messages.error(request, 'Error al abrir la caja. Verifica los datos.')

            # Cierre de caja
            elif 'close_cash' in request.POST:
                  form = forms.CloseCashForm(request.POST)
                  cash_register = models.CashRegister.objects.filter(status='open').first()
                  if cash_register and form.is_valid():
                        cash_register.closing_balance = form.cleaned_data['closing_balance']
                        cash_register.closed_by = request.user
                        cash_register.closed_at = timezone.now()
                        cash_register.status = 'closed'
                        cash_register.save()

                  # Desactivar registros financieros activos
                        models.FinancialRecord.objects.filter(is_activate=True).update(is_activate=False)

                        messages.success(request, 'Caja cerrada correctamente.')
                        return redirect('/caja')
                  else:
                    messages.error(request, 'Error al cerrar la caja. Verifica los datos.')

            # Si no es válido, regresar al método GET con el mes seleccionado
            return self.get(request)  
  
  
  # Vista para registrar un nuevo ingreso usando CreateView
class Ingresos(CreateView):
      model = models.Ingreso
      form_class = forms.IngresoForm
      template_name = 'citas/ingresos.html'
      success_url = reverse_lazy('citas:ingresos')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            ingresos = models.Ingreso.objects.all()
            total_ingresos = sum(ingreso.cantidad for ingreso in ingresos)
            context.update({
                  'ingresos': ingresos,
                  'total_ingresos': total_ingresos,
                  'service_admin': True,
                  'permisons': models.Permisons.objects.get(user=self.request.user)
            })
            return context

      def form_valid(self, form):
            messages.success(self.request, 'Ingreso registrado correctamente.')
            return super().form_valid(form)

      def form_invalid(self, form):
            messages.error(self.request, 'Error al registrar el ingreso.')
            return super().form_invalid(form)


# Sistem
def Logouts(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('/')  


class FinancialRecordCreateView(CreateView):
      model = models.FinancialRecord
      form_class = forms.FinancialRecordForm
      template_name = 'citas/financial_record_create.html'
      success_url = reverse_lazy('citas:financial-record-create')

      def get_context_data(self, **kwargs):

            context = super().get_context_data(**kwargs)
            gastos_total = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=False)
            gastos_recurrentes = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=False, gasto_recurrente=True).order_by('-id')
            gastos_otros = models.FinancialRecord.objects.filter(is_ingreso_or_gasto=False, gasto_recurrente=False).order_by('-id')
            context['service_admin'] = True
            context['gastos_recurrentes'] = gastos_recurrentes
            context['gastos_recurrentes_total'] = sum(gasto.gasto for gasto in gastos_recurrentes)
            context['gastos_otros'] = gastos_otros
            context['gastos_otros_total'] = sum(gasto.gasto for gasto in gastos_otros)
            context['gastos_total'] = sum(gasto.gasto for gasto in gastos_total)
            context['fecha'] =     datetime.now().strftime('%B %Y')

            context['permisons'] = models.Permisons.objects.get(user=self.request.user)
            return context

      def form_valid(self, form):
            if form.instance.ingreso == None:

                  form.instance.is_ingreso_or_gasto = False
                  if self.request.POST.get('fixed_expense') == 'yes':
                        form.instance.gasto_recurrente = True
      

                  form.save()
            print(form.instance.ingreso)
            messages.success(self.request, 'Registro financiero creado correctamente.')
            return super().form_valid(form)

      def form_invalid(self, form):
            messages.error(self.request, 'Error al crear el registro financiero.')
            return super().form_invalid(form)



class CustomerDetail(DetailView):
      model = models.Sale
      template_name = 'citas/detail_customer.html'
      context_object_name = 'customer'

      def get_context_data(self, **kwargs):
            opciones = models.Opciones.objects.filter(sale=self.get_object()).order_by('-id')
            context = super().get_context_data(**kwargs)

            context['options_total'] = sum(opciones.preci for opciones in opciones)
            context['opciones'] = opciones

            if self.request.user.is_authenticated:
                  context['c'] = self.get_object().cliente
                  context['company'] =  models.Company.objects.filter(name='ClickEstudios').first()
                  context['service_admin'] = True
                  context['pack_options'] = models.PackOpciones.objects.all()
                  context['total_plan'] = self.get_object().plan.price 
                  context['total_m_opciones'] = self.get_object().plan.price + sum(opciones.preci for opciones in opciones)
                  context['sale'] = self.get_object()
                  context['permisons'] = models.Permisons.objects.get(user=self.request.user)
            return context

      def post(self, request, *args, **kwargs):
            opciones = models.Opciones.objects.filter(sale=self.get_object()).order_by('-id')
            kl = self.get_object()
            kl.price_total =  sum(opciones.preci for opciones in opciones)
            kl.saled_end = True
            kl.save()

            for op in opciones:
            
                  ingreso= models.FinancialRecord(
                        is_ingreso_or_gasto=True, 
                        name = op.name,
                        description = op.description,
                        ingreso = op.preci,
                  )
                  ingreso.save()
            return redirect('citas:customer-detail-c', pk=self.get_object().id)


class PackOpcionesCreateView(CreateView):
      model = models.PackOpciones
      form_class = forms.PackOpcionesForm
      template_name = 'citas/pack_opciones_create.html'
      success_url = reverse_lazy('citas:pack-opciones-create')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['create_paquet'] = True
            context['pack_options'] = models.PackOpciones.objects.all()
            context['permisons'] = models.Permisons.objects.get(user=self.request.user)
            return context

      def form_valid(self, form):
            messages.success(self.request, 'Pack de opciones creado correctamente.')
            return super().form_valid(form)

      def form_invalid(self, form):
            messages.error(self.request, 'Error al crear el pack de opciones.')
            return super().form_invalid(form)


class HistorialCitas(TemplateView):
      template_name = 'citas/historial.html'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['sale_historial'] = models.Sale.objects.filter(saled_end=True).order_by('-id')
            context['service_admin'] = True
            context['permisons'] = models.Permisons.objects.get(user=self.request.user)
            return context


class CustomerSalesList(ListView):
      model = models.Customer
      template_name = 'citas/customer_sales_list.html'
      context_object_name = 'sales'

      def get_object(self):
            return models.Customer.objects.get(id=self.kwargs.get('pk'))

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['service_admin'] = True
            context['sales_reserver'] =  models.Sale.objects.filter(cliente=self.get_object())  
            context['customer'] = self.get_object()
            context['sales_list'] = True
            context['permisons'] = models.Permisons.objects.get(user=self.request.user)
            return context



class Dashboard(TemplateView):
      template_name = 'clickestudios/1-dashboard.html'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context



