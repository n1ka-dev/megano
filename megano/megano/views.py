from django.db.models import Prefetch
from django.views.generic import TemplateView

from app_shop.models import Product


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_offers'] = Product.objects.filter(hot_offers=True)[:3]
        context['limited'] = Product.objects.filter(limited_edition=True)[:16]
        context['popular'] = Product.objects.all().order_by('-views_count')[:8]

        return context
