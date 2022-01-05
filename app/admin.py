from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import User, Product, Category, Brand, Image, Payment, Cart, Order
from app.models.rating import RatingResponse, Rating

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Rating)
# admin.site.register(RatingResponse)
admin.site.register(Brand)
# admin.site.register(Image)
# admin.site.register(Payment)
# admin.site.register(Cart)
# admin.site.register(Order)


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

    list_display = ('username', 'email', 'name', 'is_superuser', 'is_staff', 'get_groups')

    @display(description='Groups')
    def get_groups(self, obj):
        return [e + " " for e in obj.groups.values_list('name', flat=True)]


class CustomRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'rate', 'comment', 'get_product', 'get_response', 'is_solved', 'btn_add_response')
    search_fields = (
        "id",
        "comment",
    )

    @display(description='User')
    def get_user(self, obj):
        return obj.user.name

    @display(description='Product')
    def get_product(self, obj):
        return mark_safe(f'<a href="/admin/app/product/{obj.product.id}/">{obj.product.name}</a>')

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
    list_display = ('id', 'name', 'get_thumbnail', 'brand', 'sale_price', 'category', 'short_description')
    list_filter = ['category', 'brand']
    search_fields = (
        "id",
        "name",
        "brand__name",
        "category__name",
    )

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


class CustomPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'get_logo')

    @display(description='Logo')
    def get_logo(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.logo}">')

    def get_queryset(self, request):
        return super(CustomPaymentAdmin, self).get_queryset(request).order_by('id')


class CustomImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_image', 'label')

    @display(description='Preview Image')
    def get_image(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.url}">')


class CustomCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_name', 'get_thumbnail', 'sale_price', 'count')

    @display(description='Thumbnail')
    def get_thumbnail(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.product.thumbnail}">')

    @display(description='Product Name')
    def product_name(self, obj):
        return obj.product.name

    @display(description='Sale Price')
    def sale_price(self, obj):
        return obj.product.sale_price

    def get_queryset(self, request):
        return super(CustomCartAdmin, self).get_queryset(request).order_by('user__id')


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'user', 'get_payment', 'is_paid', 'info', 'total_cost', 'items')
    search_fields = (
        "status",
        "id",
        "user__name"
    )

    @display(description='Payment')
    def get_payment(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.payment.logo}"><br><p>{obj.payment.name}</p>')

    @display(description='Info')
    def info(self, obj):
        res = f'<p>{obj.name}</p>'
        res += f'<p>{obj.phone_number}</p>'
        res += f'<p>{obj.address}</p>'
        return mark_safe(res)

    @display(description='Items')
    def items(self, obj):
        res = ''
        for e in obj.items.all():
            res += f'<img style="width:100px; height:100px;" src="{e.product.thumbnail}">'
        return mark_safe(res)

    @display(description='Thumbnail')
    def get_thumbnail(self, obj):
        return mark_safe(f'<img style="width:100px; height:100px;" src="{obj.product.thumbnail}">')

    @display(description='Product Name')
    def product_name(self, obj):
        return obj.product.name

    @display(description='Sale Price')
    def sale_price(self, obj):
        return obj.product.sale_price

    def get_queryset(self, request):
        return super(CustomOrderAdmin, self).get_queryset(request).order_by('-created_at')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Rating, CustomRatingAdmin)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(RatingResponse, CustomRatingResponseAdmin)
admin.site.register(Payment, CustomPaymentAdmin)
admin.site.register(Image, CustomImageAdmin)
admin.site.register(Cart, CustomCartAdmin)
admin.site.register(Order, CustomOrderAdmin)
admin.site.site_header = 'Admin Management'
