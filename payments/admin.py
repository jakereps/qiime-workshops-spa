# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

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
    list_display = ('title', 'start_date', 'end_date', 'url', 'live',
                    'capacity', 'total_tickets_sold', 'sales_open',
                    'seats_available')

    # Show 'draft' in the admin is a bit confusing with the default django
    # widgets, so inverting makes sense here
    def live(self, obj):
        return not obj.draft
    live.boolean = True
    live.short_description = 'Visible'

    def seats_available(self, obj):
        return not obj.is_at_capacity
    seats_available.boolean = True
    seats_available.short_description = 'Seats available'


class RateAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'workshop')


class OrderItemInline(admin.TabularInline):
    can_delete = False
    model = OrderItem
    extra = 0
    readonly_fields = ('rate', 'name')
    fields = ('rate', 'name')

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('contact_email', 'order_total', 'billed_total',
                       'billed_datetime', 'transaction_id')
    list_display = ('contact_name', 'contact_email', 'order_total',
                    'order_datetime', 'billed_total', 'billed_datetime',
                    'transaction_id')
    list_filter = ('order_datetime', 'contact_email', 'billed_datetime',
                   'billed_total')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'rate', 'email')
    readonly_fields = ('order', 'rate', 'email')

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Instructor)
admin.site.register(Rate, RateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
