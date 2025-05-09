from django.shortcuts import render
import json
import time
import statistics
import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .models import NumberEntry
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class NumbersView(View):
    """
    View to handle the numbers API endpoints
    """
    NUMBER_APIS = {
        'p': 'http://20.244.56.144/evaluation-service/primes',
        'f': 'http://20.244.56.144/evaluation-service/fibo',
        'e': 'http://20.244.56.144/evaluation-service/even',
        'r': 'http://20.244.56.144/evaluation-service/rand',
    }
    
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ2Nzk3NDUyLCJpYXQiOjE3NDY3OTcxNTIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjgzNDQwZGE4LTFmNjctNGZhNy05YjYyLWE3M2NhMTg0MjkxMSIsInN1YiI6ImFheXVzaGtlci4yMjI2Y3NlYWkxQGtpZXQuZWR1In0sImVtYWlsIjoiYWF5dXNoa2VyLjIyMjZjc2VhaTFAa2lldC5lZHUiLCJuYW1lIjoiYWF5dXNoa2VyIHNpbmdoIiwicm9sbE5vIjoiMjIwMDI5MTUyMDAwNiIsImFjY2Vzc0NvZGUiOiJTeFZlamEiLCJjbGllbnRJRCI6IjgzNDQwZGE4LTFmNjctNGZhNy05YjYyLWE3M2NhMTg0MjkxMSIsImNsaWVudFNlY3JldCI6InJDQ05GZkZ5WEREdktLc3IifQ.UWCyhIrAibZCa6F8AOkWqwEzX1NLAkYU-PM2xH1BNlI"
    
    def get(self, request, number_id):
        """
        Handle GET requests for numbers/{number_id}
        """

        if number_id not in self.NUMBER_APIS:
            return JsonResponse({'error': 'Invalid number ID'}, status=400)
        

        window_prev_state = list(NumberEntry.objects.filter(
            number_type=number_id
        ).values_list('value', flat=True)[:settings.NUMBER_WINDOW_SIZE])
        

        numbers = self.fetch_numbers(number_id)
        

        self.process_numbers(numbers, number_id)
        

        window_curr_state = list(NumberEntry.objects.filter(
            number_type=number_id
        ).values_list('value', flat=True)[:settings.NUMBER_WINDOW_SIZE])
        

        avg = 0.0
        if window_curr_state:
            avg = round(statistics.mean(window_curr_state), 2)
        

        return JsonResponse({
            'windowPrevState': window_prev_state,
            'windowCurrState': window_curr_state,
            'numbers': numbers,
            'avg': avg
        })
    
    def post(self, request, number_id):
        """
        Handle POST requests for numbers/{number_id}
        """

        return self.get(request, number_id)
    
    def fetch_numbers(self, number_id):
        """
        Fetch numbers from the third-party API with timeout
        """
        try:
    
            start_time = time.time()
            
    
            headers = {
                "Authorization": f"Bearer {self.ACCESS_TOKEN}"
            }
            
            response = requests.get(
                self.NUMBER_APIS[number_id], 
                headers=headers,
                timeout=0.5
            )
            
    
            if time.time() - start_time > 0.5:
                return []
            
    
            if response.status_code == 200:
                return response.json().get('numbers', [])
        except (requests.RequestException, json.JSONDecodeError, KeyError):
            pass
        
        return []
    
    def process_numbers(self, numbers, number_id):
        """
        Process newly received numbers
        """

        existing_values = set(NumberEntry.objects.filter(
            number_type=number_id
        ).values_list('value', flat=True))
        

        added_count = 0
        
        for value in numbers:
    
            if value in existing_values:
                continue
            
    
            NumberEntry.objects.create(value=value, number_type=number_id)
            existing_values.add(value)
            added_count += 1
            
    
            if NumberEntry.objects.filter(number_type=number_id).count() > settings.NUMBER_WINDOW_SIZE:
        
                oldest = NumberEntry.objects.filter(number_type=number_id).order_by('timestamp').first()
                if oldest:
                    oldest.delete()
