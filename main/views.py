from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# Assuming you have a Clothes model
from .models import Store, Selfie, Clothes
from .forms import SelfieForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)  # Correct usage of login()
            return redirect('login')  # Redirect to a desired page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Display selfie ideas
def ideas(request):
    # Load all selfies from the database
    selfies = Selfie.objects.all()
    return render(request, 'ideas.html', {'selfies': selfies})


def profile(request, id):
    if id is None:
        selfies = Selfie.objects.filter(user=request.user)
    else:
        user = get_object_or_404(User, id=id)
        selfies = Selfie.objects.filter(user=user)
    return render(request, 'profile.html', {'selfies': selfies})

@login_required
def selfie(request):
    if request.method == 'POST':
        form = SelfieForm(request.POST, request.FILES)
        if form.is_valid():
            selfie_instance = form.save(commit=False)  # Save the form temporarily without committing to the database
            selfie_instance.user = request.user  # Set the user to the current logged-in user
            selfie_instance.save()  # Now save the form with the user set
            return redirect('/') 
        else:
            # Form is not valid, render the page with form errors
            print(form.errors)
            return render(request, 'selfie.html', {'form': form})
        
    else:
        form = SelfieForm()
    return render(request, 'selfie.html', {'form': form})

@login_required
def dashboard(request):
    try:
        store = Store.objects.get(user=request.user)
        stores = [store]
    except Store.DoesNotExist:
        store = None
    return render(request, 'dashboard.html', {'stores': stores})

@login_required
def create_store(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        # Create a new store object
        store = Store(user=request.user, store_name=store_name, description=description, location=location, image=image)
        store.save()

        return redirect('dashboard')  
    return render(request, 'create_store.html')

def store_detail(request, store_id):
    store = Store.objects.get(id=store_id)
    products = Clothes.objects.filter(store=store)
    return render(request, 'store_detail.html', {'store': store, 'products': products})


@login_required
def create_product(request, store_id):
    store = Store.objects.get(id=store_id)

    # Check if the current user is the owner of the store
    if store.user != request.user:
        # If not, return a forbidden response or redirect
        return HttpResponseForbidden("You are not allowed to create products for this store.")

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        # Create a new clothes object
        clothes = Clothes(store=store, name=name, description=description, price=price, image=image)
        clothes.save()

        return redirect('store_detail', store_id=store_id)  
    return render(request, 'create_product.html')

def search_stores(request):
    query = request.GET.get('query', '')
    if query:
        stores = Store.objects.filter(store_name__icontains=query)[:5]
        results = [{'store_name': store.store_name, 'store_id': store.id} for store in stores]
        print(results)
        return JsonResponse(results, safe=False)
    return JsonResponse([])


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
    store_data = list(store_queryset.values('id', 'store_name', 'description', 'image'))

    # Return the serialized data as JSON
    return JsonResponse({'stores': store_data})