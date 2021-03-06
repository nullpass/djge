"""
player/views.py
"""
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from inventory.models import Container

from player.models import Config, PlayerCharacter
from player import forms

MAX_TOONS = 5
CHAR_STORAGE = 16


class Index(mixin.RequireUser, generic.ListView):
    """    List of characters    """
    model = PlayerCharacter
    template_name = 'player/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['object_list'] = PlayerCharacter.objects.filter(user=self.request.user).order_by('created')
        context['cfg'], created = Config.objects.get_or_create(name=self.request.user)
        context['max_toons'] = MAX_TOONS
        return context


class Create(mixin.RequireUser, generic.CreateView):
    """    Create a character    """
    form_class = forms.CreateCharacter
    model = PlayerCharacter
    template_name = 'player/create.html'

    def get(self, request, *args, **kwargs):
        if PlayerCharacter.objects.filter(user=self.request.user).count() >= MAX_TOONS:
            messages.error(self.request, 'Already at max.', extra_tags='danger')
            return redirect('toon:index')
        return super(Create, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if PlayerCharacter.objects.filter(user=self.request.user).count() >= MAX_TOONS:
            messages.error(self.request, 'Already at max.', extra_tags='danger')
            return super(Create, self).form_invalid(form)
        self.object = form.save(commit=False)
        self.object.storage = Container.objects.create(name=self.object.name, size=CHAR_STORAGE)
        self.object.user = self.request.user
        self.object.life = self.object.category.life_max
        self.object.life_max = self.object.category.life_max
        try:
            self.object.where = self.object.category.spawn
        except ValueError:
            self.object.where = get_object_or_404(Location, id=1)
        self.success_url = reverse('player:index')
        return super(Create, self).form_valid(form)


class Detail(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    """    View details of a character    """
    model = PlayerCharacter
    template_name = 'player/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        obj = context['object']
        context['nonenone'] = 0
        context['xtradodg'] = 0
        context['dbledamg'] = 0
        context['funkregn'] = 0
        context['magiheal'] = 0
        context['hitsteal'] = 0
        context['dbleatta'] = 0
        context['dbleheal'] = 0
        for this in [obj.c01, obj.c02, obj.c03, obj.c04, obj.c05, obj.c06, obj.c07, obj.c08]:
            context[this] += 10
        return context


class Update(mixin.RequireUser, mixin.RequireOwner, generic.UpdateView):
    """    Edit a character    """
    form_class = forms.UpdateCharacter
    model = PlayerCharacter
    template_name = 'player/update.html'

    def form_valid(self, form):
        if self.object.in_combat():
            messages.warning(self.request, 'Sorry, cannot save while character is in combat.')
            return super(Update, self).form_invalid(form)
        return super(Update, self).form_valid(form)


class Select(mixin.RequireUser, generic.RedirectView):
    """    Enter game using selected character    """
    permanent = False
    query_string = False
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        account, created = Config.objects.get_or_create(name=self.request.user)
        account.playing_toon = get_object_or_404(PlayerCharacter, user=self.request.user, pk=self.kwargs.get('pk'))
        account.save()
        return super(Select, self).get_redirect_url(*args, **kwargs)


class Inventory(mixin.RequireUser, generic.TemplateView):
    """    Storage for a character    """
    template_name = 'player/inventory.html'

    def get_context_data(self, **kwargs):
        """
        Provide {{character}} variable for base.html
        This template gets storage as relation from 'character'
        """
        context = super(Inventory, self).get_context_data(**kwargs)
        context['character'] = self.request.user.playercharacter_set.get()
        return context


class Settings(mixin.RequireUser, generic.UpdateView):
    """    Edit account settings    """
    form_class = forms.Settings
    model = Config
    template_name = 'player/settings.html'

    def get_object(self, queryset=None):
        return self.request.user.config_set.get()

    def get_success_url(self):
        messages.success(self.request, 'Changes saved!')
        return reverse_lazy('player:settings')
