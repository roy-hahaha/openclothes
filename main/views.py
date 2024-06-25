from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Assuming you have a Clothes model
from .models import Store

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
@require_http_methods(["POST"])
def store(request):
    # Load the JSON data from the request
    data = json.loads(request.body)
    times_fetch = data.get('timesFetch', 1)

    # Calculate the range of clothes to fetch based on times_fetch
    # Assuming each fetch returns 10 items
    start_index = (times_fetch - 1) * 9
    end_index = start_index + 9

    # Fetch clothes from the database
    # Adjust the query according to your model and requirements
    store_queryset = Store.objects.all()[start_index:end_index]

    # Serialize the clothes data
    # Adjust the fields according to your Clothes model
    store_data = list(store_queryset.values('id', 'name', 'description', 'image'))

    # Return the serialized data as JSON
    return JsonResponse({'stores': store_data})