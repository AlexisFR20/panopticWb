from django.test import TestCase
from rest_framework.test import APIRequestFactory

# Create your tests here.
factory = APIRequestFactory()
request = factory.get('http://192.168.1.118:8001/api/analytics', {'planta_id': 5})

print(request)
