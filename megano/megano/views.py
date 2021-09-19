from django.db.models import Prefetch
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = "index.html"

