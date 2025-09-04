import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusLocation
from django.shortcuts import render


@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8')
            print("Received JSON:", raw_data)  # Debugging
            data = json.loads(raw_data)

            lat = data.get('lat')
            lng = data.get('lng')

            if lat is not None and lng is not None:
                if lat == 0.0 and lng == 0.0:  # Ignore invalid data
                    return JsonResponse({'status': 'error', 'message': 'Invalid GPS data'}, status=400)

                BusLocation.objects.create(lat=lat, lng=lng)
                return JsonResponse({'status': 'success'})

            return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# Function to return the latest bus location
# def get_latest_location(request):
#     location = BusLocation.objects.last()
#     if location:
#         return JsonResponse({'lat': location.lat, 'lng': location.lng})
#     return JsonResponse({'lat': None, 'lng': None})  # Use None instead of 0


# Render the map page
def live_map(request):
    return render(request, 'tracker/map.html')



def get_latest_location(request):
    latest_location = BusLocation.objects.order_by('-id').first()
    
    if latest_location:
        return JsonResponse({"lat": latest_location.lat, "lng": latest_location.lng})
    
    return JsonResponse({"lat": None, "lng": None})  # Return None if no data exists

