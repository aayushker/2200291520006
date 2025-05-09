from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import StockService
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class StockPriceView(View):

    def get(self, request, ticker):

        try:
            minutes = request.GET.get('minutes')
            aggregation = request.GET.get('aggregation')
            
            if aggregation and aggregation != 'average':
                return JsonResponse({'error': 'Invalid aggregation parameter'}, status=400)
            
            price_history = StockService.get_stock_prices(ticker, minutes)
            
            average_price = StockService.calculate_average_price(price_history)
            
            return JsonResponse({
                'averageStockPrice': average_price,
                'priceHistory': price_history
            })
        except Exception as e:
            logger.exception(f"Error in stock price view: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class StockCorrelationView(View):

    def get(self, request):

        try:
            minutes = request.GET.get('minutes')
            tickers = request.GET.getlist('ticker')
            
            if not minutes:
                return JsonResponse({'error': 'Minutes parameter is required'}, status=400)
            
            if not tickers or len(tickers) != 2:
                return JsonResponse({'error': 'Exactly two tickers are required'}, status=400)
            
            ticker_a, ticker_b = tickers
            prices_a = StockService.get_stock_prices(ticker_a, minutes)
            prices_b = StockService.get_stock_prices(ticker_b, minutes)
            
            correlation = StockService.calculate_correlation(prices_a, prices_b)
            
            avg_a = StockService.calculate_average_price(prices_a)
            avg_b = StockService.calculate_average_price(prices_b)
            
            response = {
                'correlation': correlation,
                'stocks': {
                    ticker_a: {
                        'averagePrice': avg_a,
                        'priceHistory': prices_a
                    },
                    ticker_b: {
                        'averagePrice': avg_b,
                        'priceHistory': prices_b
                    }
                }
            }
            
            return JsonResponse(response)
        except Exception as e:
            logger.exception(f"Error in stock correlation view: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
