from django.urls import path
from .views import NumbersView

urlpatterns = [
    path('numbers/<str:number_id>', NumbersView.as_view(), name='numbers'),
] 