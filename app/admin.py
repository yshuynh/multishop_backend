from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import User, Product, Category, Brand
from app.models.rating import RatingResponse, Rating

admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Rating)
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


class CustomRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'rate', 'comment', 'get_product', 'get_response')

    @display(description='User')
    def get_user(self, obj):
        return obj.user.name

    @display(description='Product')
    def get_product(self, obj):
        return obj.product.name

    @display(description='Response List')
    def get_response(self, obj):
        # return mark_safe(['<ul>' + e.user.name + ': ' + e.comment + '</ul>' for e in obj.responses.all()])
        # each obj will be an Order obj/instance/row
        to_return = '<ul>'
        # I'm assuming that there is a name field under the event.Product model. If not change accordingly.
        to_return += '\n'.join(
            '<li>{}</li>'.format(e.user.name + ': ' + e.comment) for e in obj.responses.all())
        to_return += '</ul>'
        return mark_safe(to_return)

    class Media:
        css = {
            'all': ('fancy.css',)
        }


admin.site.register(User, CustomUserAdmin)
admin.site.register(Rating, CustomRatingAdmin)
admin.site.site_header = 'Admin Management'
