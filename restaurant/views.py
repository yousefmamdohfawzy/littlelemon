# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse ,JsonResponse
import json

# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')




def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})




def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 



def reservations(request):
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})






def bookings(request):
    date = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
    try:
        bookings = Booking.objects.filter(reservation_date=date)
        booking_json = serializers.serialize('json', bookings)
        return JsonResponse({'data': booking_json}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    
@csrf_exempt
def book(request):
    form = BookingForm()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = BookingForm(data)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Booking successful'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid form data', 'details': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    context = {'form':form}
    return render(request, 'book.html', context)


