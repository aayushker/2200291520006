import requests
import json
import numpy as np
import datetime
from dateutil import parser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import StockPrice
import logging

logger = logging.getLogger(__name__)

class StockService:
    
    @staticmethod
    def get_auth_headers():
    
        return {
            "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
        }

    @staticmethod
    def get_all_stocks():

        try:
            url = f"{settings.STOCK_API_BASE_URL}/stocks"
            response = requests.get(url, headers=StockService.get_auth_headers())
            
            if response.status_code == 200:
                return response.json().get('stocks', {})
            else:
                logger.error(f"Failed to fetch stocks: {response.status_code}")
                return {}
        except Exception as e:
            logger.exception(f"Error fetching stocks: {str(e)}")
            return {}

    @staticmethod
    def get_stock_prices(ticker, minutes=None):

        now = timezone.now()
        
        if minutes:
            time_threshold = now - timedelta(minutes=int(minutes))
            cached_prices = StockPrice.objects.filter(
                ticker=ticker,
                last_updated_at__gte=time_threshold
            ).order_by('-last_updated_at')
        else:
            cached_prices = StockPrice.objects.filter(ticker=ticker).order_by('-last_updated_at')
        
        if cached_prices.exists() and (now - cached_prices.first().retrieved_at).total_seconds() < settings.API_CACHE_TTL:
            return [
                {
                    'price': p.price,
                    'lastUpdatedAt': p.last_updated_at.isoformat() + 'Z'
                } for p in cached_prices
            ]
        
        try:
            if minutes:
                url = f"{settings.STOCK_API_BASE_URL}/stocks/{ticker}?minutes={minutes}"
            else:
                url = f"{settings.STOCK_API_BASE_URL}/stocks/{ticker}"
            
            response = requests.get(url, headers=StockService.get_auth_headers())
            
            if response.status_code == 200:
    
                data = response.json()
                
    
                if minutes:
                    time_threshold = now - timedelta(minutes=int(minutes))
                    StockPrice.objects.filter(
                        ticker=ticker,
                        last_updated_at__gte=time_threshold
                    ).delete()
                
    
                if isinstance(data, list):
                    for price_data in data:
                        StockService.store_price(ticker, price_data)
                    return data
                elif 'stock' in data:
                    price_data = data['stock']
                    StockService.store_price(ticker, price_data)
                    return [price_data]
                
                return []
            else:
                logger.error(f"Failed to fetch stock prices: {response.status_code}")
                return []
        except Exception as e:
            logger.exception(f"Error fetching stock prices: {str(e)}")
            return []

    @staticmethod
    def store_price(ticker, price_data):

        try:
            last_updated_at = parser.parse(price_data['lastUpdatedAt'])
            StockPrice.objects.create(
                ticker=ticker,
                price=price_data['price'],
                last_updated_at=last_updated_at
            )
        except Exception as e:
            logger.exception(f"Error storing price: {str(e)}")

    @staticmethod
    def calculate_average_price(price_history):

        if not price_history:
            return 0.0
        
        return sum(item['price'] for item in price_history) / len(price_history)

    @staticmethod
    def calculate_correlation(prices_a, prices_b):

        if not prices_a or not prices_b or len(prices_a) < 2 or len(prices_b) < 2:
            return 0.0
        
        prices_a_values = [item['price'] for item in prices_a]
        prices_b_values = [item['price'] for item in prices_b]
        
        try:
            correlation = np.corrcoef(prices_a_values, prices_b_values)[0, 1]

            return round(correlation, 4)
        except Exception as e:
            logger.exception(f"Error calculating correlation: {str(e)}")
            return 0.0 