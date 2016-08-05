from django.contrib import admin

from .models import Workshop, Instructor, Rate, Order, OrderItem


class InstructorInline(admin.TabularInline):
    model = Instructor.workshops.through
    extra = 1


class RateInline(admin.TabularInline):
    model = Rate
    extra = 1


class WorkshopAdmin(admin.ModelAdmin):
    inlines = [InstructorInline, RateInline]
    prepopulated_fields = {'slug': ('title', 'start_date')}
    list_display = ('title', 'start_date', 'end_date', 'url')


class RateAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'workshop')


class OrderItemInline(admin.TabularInline):
    can_delete = False
    model = OrderItem
    extra = 0
    readonly_fields = ('order', 'rate', 'quantity')

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('email', 'order_total', 'billed_total',
                       'billed_datetime')
    list_display = ('email', 'order_total', 'order_datetime',
                    'billed_total', 'billed_datetime')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'rate', 'quantity')
    readonly_fields = ('order', 'rate', 'quantity')

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Instructor)
admin.site.register(Rate, RateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
