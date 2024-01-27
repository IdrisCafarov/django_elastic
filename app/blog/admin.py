from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Post)
admin.site.register(Reply)

class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title','email']

admin.site.register(Professor, BlogAdmin)
admin.site.register(Title)