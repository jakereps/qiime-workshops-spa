from decimal import Decimal

import requests

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import FormMixin

from .models import Workshop, Order, OrderItem
from .forms import OrderForm


class WorkshopList(ListView):
    queryset = Workshop.objects.filter(closing_date__gte=timezone.now())
    context_object_name = 'upcoming_workshops'


class WorkshopDetail(FormMixin, DetailView):
    model = Workshop
    form_class = OrderForm
    context_object_name = 'workshop'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['workshop'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        rates = []
        for rate in self.object.rate_set.order_by('price'):
            field = context['form'][rate.name]
            rates.append({'field': field, 'name': rate.name, 'price':
                          rate.price})
        context['rates'] = rates
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        order = form.data.copy()
        order['workshop'] = self.object.slug
        order_total = 0
        for rate in form.rate_set:
            order_total += Decimal(form.data[rate.name]) * rate.price

        order['order_total'] = str(order_total)
        self.request.session['order'] = order
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payments:confirm',
                       kwargs={'workshop_slug': self.object.slug})


class ConfirmOrder(TemplateView):
    template_name = 'payments/workshop_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.session['order']
        order.pop('csrfmiddlewaretoken')
        context['order'] = order
        return context


class SubmitOrder(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_data = request.session['order']
        workshop = Workshop.objects.get(slug=order_data['workshop'])
        order = Order.objects.create(email=order_data['email'],
                                     order_total=order_data['order_total'])
        for rate in workshop.rate_set.all():
            if order_data[rate.name] != 0:
                OrderItem.objects.create(order=order, rate=rate,
                                         quantity=order_data[rate.name])
        payload = {'LMID': 'DUMMY',
                   'unique_id': '%s' % order.pk,
                   'sTotal': order_data['order_total'],
                   'webTitle': 'test',
                   'Trans_Desc': 'abc',
                   'contact_info': 'admin@google.com'}
        r = requests.post('http://example.com', data=payload,
                          verify='/Users/Develop/Desktop/Certificates.pem')
        return HttpResponse(r.text)
