from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import User, Product, Category, Brand
from app.models.rating import RatingResponse, Rating

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Rating)
# admin.site.register(RatingResponse)
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
    list_display = ('id', 'get_user', 'rate', 'comment', 'get_product', 'get_response', 'btn_add_response')

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

    @display(description='Action')
    def btn_add_response(self, obj):
        return mark_safe(f'<a href="/admin/app/ratingresponse/add/?rating={obj.id}&next=/admin/app/rating/"><input type="button" value="Add response"/></a>')

    class Media:
        css = {
            'all': ('fancy.css',)
        }


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_brands')

    @display(description='Brand List')
    def get_brands(self, obj):
        return [str(e) + ', ' for e in obj.brands.all()]


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'get_thumbnail', 'brand', 'sale_price', 'category')

    @display(description='Thumbnail')
    def get_thumbnail(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.thumbnail}">')


class CustomRatingResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_rating', 'get_response_rating')

    @display(description='Rating')
    def get_rating(self, obj):
        return f'<{obj.rating.user.name}> <{obj.rating.comment}>'

    @display(description='Response')
    def get_response_rating(self, obj):
        return f'<{obj.user.name}> <{obj.comment}>'

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomRatingResponseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['user'].disabled = True
        # form.base_fields['rating'].disabled = True
        # form.fields['user'].disabled = True
        return form


admin.site.register(User, CustomUserAdmin)
admin.site.register(Rating, CustomRatingAdmin)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(RatingResponse, CustomRatingResponseAdmin)
admin.site.site_header = 'Admin Management'
