from django.views.generic import FormView

from .forms import ManualFieldsetsForm, PropertyFieldsetsForm


class ManualFieldsetsView(FormView):
    form_class = ManualFieldsetsForm
    template_name = "fieldsets/manual.html"


class PropertyFieldsetsView(FormView):
    form_class = PropertyFieldsetsForm
    template_name = "fieldsets/property.html"
