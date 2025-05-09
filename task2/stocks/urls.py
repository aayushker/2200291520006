from django.urls import path
from .views import StockPriceView, StockCorrelationView

urlpatterns = [
    path('stocks/<str:ticker>', StockPriceView.as_view(), name='stock_price'),
    path('stockcorrelation', StockCorrelationView.as_view(), name='stock_correlation'),
] 