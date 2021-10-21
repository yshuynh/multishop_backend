from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import User, Product, Category, Brand
from app.models.rating import RatingResponse, Rating

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(RatingResponse)
admin.site.register(Brand)


class CustomUserAdmin(UserAdmin):
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('created_at', 'updated_at')}),
    )
    list_display = ('username', 'email', 'name', 'is_staff')


admin.site.register(User, CustomUserAdmin)
admin.site.site_header = 'Admin Management'
