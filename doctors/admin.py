from django.contrib import admin

from .models import DoctorAvailability, DoctorProfile, Speciality

admin.site.register(DoctorAvailability)

admin.site.register(DoctorProfile)

admin.site.register(Speciality)
