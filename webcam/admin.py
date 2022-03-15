from re import search
from django.contrib import admin
from .models import Student, Class, Authentication
class StudenInfo(admin.ModelAdmin):
    list_display = ['id', 'name', 'mssv','Class']
    list_filter = ['Class','mssv']
    search_fields = ['Class','mssv']

class ClassInfo(admin.ModelAdmin):
    list_editable = ['name_class', 'value']
    list_display = ['id', 'name_class','value']
    search_fields = ['name_class']
    
class AuthenticationInfo(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['id', 'student','status','date']
    search_fields = ['student','status','date']

admin.site.register(Student, StudenInfo)
admin.site.register(Class, ClassInfo)
admin.site.register(Authentication, AuthenticationInfo)
