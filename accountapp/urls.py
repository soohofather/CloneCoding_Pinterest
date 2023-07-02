from django.urls import path, include
from accountapp.views import hello_world, AccountCreateView

app_name = "accountapp"

urlpatterns = [
    path("hello_world/", hello_world, name="hello_world"),

    # CBV는 .as_view
    path('create/', AccountCreateView.as_view(), name="create"),
]
