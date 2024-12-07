from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(MomentImage)
admin.site.register(ServiceImage)
admin.site.register(Appointment)
admin.site.register(MomentRelatedImage)
admin.site.register(Plans)
admin.site.register(CaratPlanes)
admin.site.register(UserA)
admin.site.register(Role)
admin.site.register(Permisons)
admin.site.register(Tweet)
admin.site.register(ImgTweet)
admin.site.register(ImageServiceImg)

admin.site.register(CashRegister)
admin.site.register(Transaction)
admin.site.register(CashMovement)
admin.site.register(FinancialRecord)
admin.site.register(Sale)
admin.site.register(Opciones)
admin.site.register(PackOpciones)

admin.site.register(Company)