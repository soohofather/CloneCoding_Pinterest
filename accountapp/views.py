from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.form import AccountUpdateForm
from accountapp.models import HelloWorld


# Create your views here.

# 함수형 view
@login_required
def hello_world(request):

    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        hello_world_list = HelloWorld.objects.all()
        return HttpResponseRedirect(reverse('accountapp:hello_world'))

    else:
        hello_world_list = HelloWorld.objects.all()
        return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})



has_ownership = [account_ownership_required, login_required]
# Class형 View
class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    def get(self, *arg, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*arg, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, *arg, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*arg, **kwargs)
        else:
            return HttpResponseForbidden()

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
@method_decorator(account_ownership_required, 'get')
@method_decorator(account_ownership_required, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

    def get(self, *arg, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*arg, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, *arg, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*arg, **kwargs)
        else:
            return HttpResponseForbidden()

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'
