import json
import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BinInfo
import logging

logger = logging.getLogger(__name__)

class BinLookupView(APIView):
    def get(self, request, bin_number, format=None):
        cache_key = f'bin_{bin_number}'
        try:
            value = cache.get(cache_key)
            if value:
                value = json.loads(value)
            else:
                value = self.fetch_from_external_service(bin_number)
                cache.set(cache_key, json.dumps(value))
            return Response({'bin_number': bin_number, 'info': value}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in GET method: {e}")
            return Response({'error': 'Internal server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        card_number = request.data.get('card_number')
        if not card_number:
            return Response({'error': 'Card number is required'}, status=status.HTTP_400_BAD_REQUEST)

        bin_number = card_number[:6]
        cache_key = f'bin_{bin_number}'
        try:
            bank_info = cache.get(cache_key)
            if not bank_info:
                bank_info = self.fetch_from_external_service(bin_number)
                if bank_info:
                    BinInfo.objects.create(bin_number=bin_number, bank_name=bank_info)
                    cache.set(cache_key, json.dumps(bank_info))
                else:
                    return Response({'error': 'Bank information not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'bin_number': bin_number, 'bank_name': bank_info}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in POST method: {e}")
            return Response({'error': 'Internal server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_from_external_service(self, bin_number):
        url = f"https://api.apilayer.com/bincheck/{bin_number}"
        headers = {
            "apikey": "N2GMRcpeuuQajmuj0V6GH4DVYXSqsfbN"
        }

        logger.info(f"Sending request to API: {url}")
        logger.info(f"Headers: {headers}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"API Response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching BIN info: {e}")
            raise Exception(f'Error fetching BIN info: {e}')
