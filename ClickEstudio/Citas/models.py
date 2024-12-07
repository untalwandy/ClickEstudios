from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
import os





# Create your models here.

class Customer(models.Model):
      name = models.CharField(max_length=255)
      choice_time = models.CharField(max_length=255, default='10:00', blank=True)
      last_name = models.CharField(max_length=255, default='', blank=True, null=True)
      dni = models.CharField(max_length=20, unique=True, blank=True, null=True)
      email = models.EmailField(default='', blank= True, null=True)  
      number = models.CharField(max_length=20, blank=True, null=True, default='809-000-0000')
      date_created = models.DateTimeField(auto_now_add=True)
      date_choice = models.DateTimeField(default=datetime.now, blank=True, null=True)

      date_only_choice = models.DateField(default=datetime.now, blank=True, null=True)

      date_time_choice = models.TimeField(default='10:00') 
      plan_choice = models.IntegerField(default=2, blank=True, null=True)
      finished = models.BooleanField(default=False)
      reserve = models.BooleanField(default=False)
      reserver_mount = models.IntegerField(default=500, blank=True, null=True)
      plans = models.ForeignKey('Plans', related_name='plans_customer', on_delete=models.CASCADE, 
                                blank=True, null=True)
      plans_more = models.ManyToManyField('Plans', related_name='plans_more', blank=True)
      saled = models.BooleanField(default=False, blank=True, null=True)
      saled_mount = models.IntegerField(default=0, blank=True, null=True)
      price_reserved = models.IntegerField(default=500, blank=True, null=True)

      
      def __str__(self):
            return f"{self.name} {self.last_name}"
  
  
class Appointment(models.Model):
      customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
      date_created = models.DateTimeField(auto_now_add=True)
      date_remember = models.DateTimeField()  # Assuming date_remember is a reminder date
      date_remember_time = models.TimeField(default='10:00')  # Time part of the reminder 

      def __str__(self):
            return f"Cita para {self.customer.name} {self.date_remember} "
      
      
      
class ServiceImage(models.Model):
      name = models.CharField(max_length=255, default='Servicio')
      image = models.ImageField(upload_to='media/')
      date_created = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.name
      
      
class ServiceRelatedImage(models.Model):
    service = models.ForeignKey(ServiceImage, related_name='service_img', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    img_url = models.URLField(default='', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.moment.name} - {"Related Image"}'



class MomentImage(models.Model):
      name = models.CharField(max_length=255, default='Momento')
      image = models.ImageField(upload_to='media/')
      date_created = models.DateTimeField(auto_now_add=True)
      service = models.ForeignKey(ServiceImage, related_name='svc_img_g',
                  on_delete=models.CASCADE,     blank=True,     null=True)

      def __str__(self):
            return self.name


class MomentRelatedImage(models.Model):
      moment = models.ForeignKey(MomentImage, related_name='moment_img', 
                                 on_delete=models.CASCADE, blank=True, null=True)
      service = models.ForeignKey(ServiceImage, related_name='svc_img',
                                  on_delete=models.CASCADE, blank=True, null=True)
      image = models.ImageField(upload_to='media/', blank=True, null=True)
      img_url = models.URLField(default='', blank=True, null=True)
      date_created = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f'{self.moment.name} - {"Related Image"}'
      
  
      
# Nuestros planes
class Plans(models.Model):
      name = models.CharField(max_length=255, default='Plan')
      description = models.TextField(default='Descripción del plan', blank=True, null=True)
      service = models.ForeignKey(ServiceImage, related_name='services', on_delete=models.CASCADE, blank=True, null=True)
      img = models.ImageField(upload_to='media/')
      price = models.IntegerField(default=0)
      final_price = models.IntegerField(default=0)
      date_created = models.DateTimeField(auto_now_add=True)
      is_activate = models.BooleanField(default=True)
      
      def __str__(self):
            return self.name
      
# Carateristicas de los planes
class CaratPlanes(models.Model):
      plans = models.ForeignKey(Plans, related_name='plans', on_delete=models.CASCADE, blank=True, null=True)
      name = models.CharField(max_length=255, default='Plan o Servicio')
      date_created = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.name
      
      
class Adicionales(models.Model):
      plans = models.ForeignKey(Plans, related_name='adicionales', on_delete=models.CASCADE, blank=True, null=True)
      description = models.TextField(default='...')
      date_created = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.description
      
      
class Role(models.Model):
      name = models.CharField(max_length=255, default='Indefinido')
      user = models.ForeignKey(User, related_name='user_role',  on_delete=models.CASCADE, blank=True, null=True)
      description = models.TextField(default="Un rol indefinodo podría tener la capacidad de ver ciertos contenidos que no requieran permisos especiales, como páginas informativas o recursos de ayuda y mas")
      date_created = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.name
      
      
class UserA(models.Model):
      user = models.ForeignKey(User, related_name='userA',  on_delete=models.CASCADE, blank=True, null=True)
      role = models.ForeignKey(Role, related_name='role', on_delete=models.CASCADE, blank=True, null=True)
      img = models.ImageField(upload_to='media/', blank=True, null=True)

      name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      number = models.CharField(max_length=20,  blank=True, null=True)
      birthday = models.DateField(default=timezone.now)
      date_created = models.DateTimeField(auto_now_add=True,  blank=True, null=True)
      active = models.BooleanField(default=True)
      email = models.EmailField()

      def __str__(self):
            return self.name
      

class Permisons(models.Model):
      role = models.ForeignKey(Role, related_name='role_permisons', blank=True, null=True,
                               on_delete=models.CASCADE)
      user = models.ForeignKey(User, related_name='permisons', blank=True, null=True,
                               on_delete=models.CASCADE)
      priori = models.IntegerField(blank=True, null=True, default=0)
      active = models.BooleanField(default=True)
      date_created = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.role.name
      
      
class ImageServiceImg(models.Model):
      img_service = models.ForeignKey(ServiceImage,
                  related_name='img_service', on_delete=models.CASCADE, blank=True,  null=True)
      name = models.CharField(default='...', max_length=100, blank=True,  null=True)
      moment = models.ForeignKey(MomentImage, related_name='moment_img_service',
                  on_delete=models.CASCADE,  blank=True,  null=True)
      date = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.name
      
      
      

class Tweet(models.Model):
      img = models.ImageField(upload_to='media/', blank=True, null=True)
      title = models.CharField(max_length=280)  # Límite de caracteres similar a Twitter
      sub = models.CharField(max_length=280, default='')  # Límite de caracteres similar a Twitter
      p = models.CharField(max_length=280, default='')  # Límite de caracteres similar a Twitter
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      is_activate = models.BooleanField(default=True)

      def __str__(self):
            return self.sub
      


class ImgTweet(models.Model):
      img = models.ForeignKey(Tweet, related_name='img_tweet', blank=True, null=True,
                               on_delete=models.CASCADE)
      img_tweet = models.ImageField(upload_to='media/', blank=True, null=True)
      is_activate = models.BooleanField(default=True)
      
      
class Gastos(models.Model):
      plans = models.ForeignKey(Plans, related_name='gastos_plan', 
                                on_delete=models.CASCADE,  blank=True, null=True)
      service = models.ForeignKey(ServiceImage, related_name='gastos_service', 
                                on_delete=models.CASCADE,  blank=True, null=True)
      adicionales = models.ForeignKey(Plans, related_name='gastos_adicionales', 
                                on_delete=models.CASCADE,  blank=True, null=True)
      name = models.CharField(max_length=100, default='...')
      description = models.TextField(default='...')
      price = models.IntegerField(default=0)
      date = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.name
      
      
      

class CashRegister(models.Model):
    # Estado de la caja (abierta o cerrada)
    STATUS_CHOICES = [
        ('open', 'Abierta'),
        ('closed', 'Cerrada'),
    ]


    
    # Apertura y cierre de caja
    opened_by = models.ForeignKey(User, related_name='cash_opened', on_delete=models.SET_NULL, null=True)
    closed_by = models.ForeignKey(User, related_name='cash_closed', on_delete=models.SET_NULL, null=True, blank=True)


    number_caja = models.PositiveIntegerField(null=True, blank=True)  # Agregar el campo number_caja

    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)  # Monto inicial en la caja
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Monto final en la caja

    opened_at = models.DateTimeField(default=timezone.now)  # Fecha y hora de apertura
    closed_at = models.DateTimeField(null=True, blank=True)  # Fecha y hora de cierre

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # Estado actual de la caja
      
    date = models.DateTimeField(default=timezone.now) # Crear fecha atuacal


    def save(self, *args, **kwargs):
      if not self.number_caja:  # Si no tiene un número asignado, asignar uno.
            self.number_caja = CashRegister.objects.count() + 1  # Contar y sumar 1
      super().save(*args, **kwargs)
    

    def __str__(self):
        return f'Caja {self.id} - {self.status}'

class Transaction(models.Model):
    # Tipos de transacción: venta, salida, entrada, devolución
    TRANSACTION_TYPE_CHOICES = [
        ('sale', 'Venta'),
        ('withdrawal', 'Salida'),
        ('deposit', 'Entrada'),
        ('refund', 'Devolución'),
    ]
    
    register = models.ForeignKey(CashRegister, related_name='transactions', on_delete=models.CASCADE)
    cashier = models.ForeignKey(User, related_name='cashier_transactions', on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto de la transacción
    description = models.TextField(blank=True)  # Descripción opcional de la transacción
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount}'

class CashMovement(models.Model):   
    # Movimientos de efectivo como entradas o retiros de caja
    MOVEMENT_TYPE_CHOICES = [
        ('deposit', 'Depósito'),
        ('withdrawal', 'Retiro'),
    ]
    
    register = models.ForeignKey(CashRegister, related_name='movements', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.movement_type} - {self.amount}'
      
      
      


class Ingreso(models.Model):
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad}"



class FinancialRecord(models.Model):
      date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
      name = models.CharField(max_length=255, blank=True, null=True)
      description = models.TextField(blank=True, null=True)
      ingreso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
      gasto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
      is_ingreso_or_gasto = models.BooleanField(default=True, blank=True, null=True)
      is_activate = models.BooleanField(default=True, blank=True, null=True)
      created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

      gasto_recurrente = models.BooleanField(default=False, blank=True, null=True)
      renovacion_mensual_gasto_recurrente = models.IntegerField(default=15, blank=True, null=True)
      # Renovacion_mensual_gasto_recurrente en la que se renobara el gasto automaticamente
      # Un gasto recurrente es un gasto recurrente que se mantiene constante durante un período de tiempo, como el alquiler o los servicios públicos.

      def __str__(self):
            return f"{self.name} - {self.description}"


class Sale(models.Model):
      cliente = models.ForeignKey(Customer, related_name='cliente', 
            on_delete=models.CASCADE, blank=True, null=True)
      plan = models.ForeignKey(Plans, related_name='plan', on_delete=models.CASCADE, blank=True, null=True)
      price_total = models.IntegerField(default=0, blank=True, null=True)
      date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
      is_activate = models.BooleanField(default=True, blank=True, null=True)
      saled = models.BooleanField(default=False, blank=True, null=True)

      date_only_choice = models.DateField(default=datetime.now, blank=True, null=True)

      saled_confirm = models.BooleanField(default=False, blank=True, null=True)

      reserver = models.BooleanField(default=False, blank=True, null=True)
      reserver_mount = models.IntegerField(default=0, blank=True, null=True)
      abonado = models.IntegerField(default=0, blank=True, null=True)

      saled_end = models.BooleanField(default=False, blank=True, null=True)

      def __str__(self):
            return f"Venta #vn00{self.id} {self.cliente} - {self.plan} - {self.cliente.date_only_choice} - {'Vendido' if self.saled == True else 'No pagado'}" 


class Opciones(models.Model):
      sale = models.ForeignKey(Sale, related_name='opciones', on_delete=models.CASCADE)
      name = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      preci = models.IntegerField(default=0)
      date = models.DateTimeField(auto_now_add=True)


      def __str__(self):
            return f"{self.name} - {self.description}"


class PackOpciones(models.Model):
      img = models.ImageField(upload_to='media/', blank=True, null=True)
      name = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      preci = models.IntegerField(default=0)
      date = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f"{self.name} - {self.description}"


class Company(models.Model):
      # company =  models.ForeignKey(User, related_name='user_company', on_delete=models.CASCADE)
      name = models.CharField(max_length=255 , blank=True, null=True)
      description = models.TextField(blank=True, null=True )
      logo = models.ImageField(upload_to='media/', blank=True, null=True)
      logo2 = models.ImageField(upload_to='media/', blank=True, null=True)
      date = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.name



