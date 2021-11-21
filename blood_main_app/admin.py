from django.contrib import admin
from .models import User,Compliment,p2p_donation_receive,emergency_receiver
# Register your models here.
admin.site.register(User)
admin.site.register(Compliment)
admin.site.register(p2p_donation_receive)
admin.site.register(emergency_receiver)