from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from profileapp.forms import ProfileCreationForm
from profileapp.models import Profile


# Create your views here.
class ProfileCreateView(CreateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'profileapp/create.html'

    def form_valid(self, form):
        # 날라온 Form 을 임시로 저장
        temp_profile = form.save(commit=False)
        # 저장한 것에 유저에 self 유저를 넣고 저장
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)