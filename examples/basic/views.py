from django.views.generic import FormView

from .forms import (
    SimpleBootstrapForm, SimpleFoundationForm, SimpleMultiWidgetForm,
    SimpleForm, SimpleWithOverridesForm)


class SimpleView(FormView):
    form_class = SimpleForm
    template_name = 'basic/simple_view.html'


class SimpleWithOverridesView(FormView):
    form_class = SimpleWithOverridesForm
    template_name = 'basic/simple_view.html'


class SimpleBootstrapView(FormView):
    form_class = SimpleBootstrapForm
    template_name = 'basic/bootstrap_view.html'


class SimpleFoundationView(FormView):
    form_class = SimpleFoundationForm
    template_name = 'basic/foundation_view.html'


class SimpleMultiWidgetView(FormView):
    form_class = SimpleMultiWidgetForm
    template_name = 'basic/simple_view.html'
