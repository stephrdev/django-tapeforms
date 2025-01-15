from django.views.generic import FormView

from .forms import (
    SimpleBootstrap4Form,
    SimpleBootstrap5Form,
    SimpleForm,
    SimpleFoundationForm,
    SimpleMultiWidgetForm,
    SimpleWithOverridesForm,
)


class SimpleView(FormView):
    form_class = SimpleForm
    template_name = "basic/simple_view.html"


class SimpleWithOverridesView(FormView):
    form_class = SimpleWithOverridesForm
    template_name = "basic/simple_view.html"


class SimpleBootstrap4View(FormView):
    form_class = SimpleBootstrap4Form
    template_name = "basic/bootstrap4_view.html"


class SimpleBootstrap5View(FormView):
    form_class = SimpleBootstrap5Form
    template_name = "basic/bootstrap5_view.html"


class SimpleFoundationView(FormView):
    form_class = SimpleFoundationForm
    template_name = "basic/foundation_view.html"


class SimpleMultiWidgetView(FormView):
    form_class = SimpleMultiWidgetForm
    template_name = "basic/simple_view.html"
