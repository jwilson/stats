from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Weapon


class ToolsHomeView(TemplateView):
    template_name = 'tools/tools_base.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        return ctx


class ItemPrefabsCodeGenerator(TemplateView):
    template_name = 'tools/csharp_prefabclass.cshtml'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_list'] = Weapon.objects.all()
        return ctx
