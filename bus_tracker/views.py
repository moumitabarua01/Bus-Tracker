from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random

def home(request):
    return render(request,'home.html')

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_api(request):
    """Chatbot API endpoint that provides intelligent responses about bus tracking"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').lower().strip()
        
        # Define responses based on common queries
        responses = {
            'greeting': [
                "Hello! I'm here to help you with bus tracking information. How can I assist you?",
                "Hi there! I can help you with bus schedules, live tracking, and seat booking. What do you need?",
                "Welcome! I'm your Bus Tracker assistant. How can I help you today?"
            ],
            'schedule': [
                "You can view the complete bus schedule by clicking on the 'Schedule' menu in the navigation bar. The schedule shows all departure and arrival times for different bus types.",
                "The bus schedule is available in the Schedule section. It includes times for Minibus, Microbus, Students' Bus, and other vehicle types.",
                "To check bus schedules, go to the Schedule page where you'll find detailed timetables for all university buses."
            ],
            'tracking': [
                "For live bus tracking, click on 'Live Map' in the navigation menu. You'll see real-time bus locations on an interactive map.",
                "The live tracking feature shows you exactly where your bus is right now. Just go to the Live Map section.",
                "You can track buses in real-time using the Live Map feature. It updates every few seconds with current bus locations."
            ],
            'booking': [
                "To book a seat, click on 'Book Your Seat' in the navigation menu. You'll see available trips and can select your preferred seat.",
                "Seat booking is available for different bus trips. Go to the Book Your Seat section to see available options.",
                "You can book seats for various bus trips. The booking system shows available seats and lets you make reservations."
            ],
            'bus_names': [
                "We have several buses available: Ronobheri, Agnibina, and Bhorer Alo. You can book seats for any of these buses.",
                "Our bus fleet includes Ronobheri, Agnibina, and Bhorer Alo. Each bus has its own schedule and seat availability.",
                "The available buses are Ronobheri, Agnibina, and Bhorer Alo. You can check their schedules and book seats accordingly."
            ],
            'help': [
                "I can help you with: bus schedules, live tracking, seat booking, and general information about our bus services.",
                "Here's what I can assist you with: viewing bus schedules, tracking buses in real-time, booking seats, and answering questions about our services.",
                "I'm here to help with bus tracking, schedules, seat booking, and any other questions about our transportation services."
            ],
            'default': [
                "I'm not sure I understand. Could you ask about bus schedules, live tracking, seat booking, or bus information?",
                "I can help you with bus schedules, live tracking, seat booking, or general bus information. What would you like to know?",
                "For assistance, you can ask about: bus schedules, live tracking, seat booking, or available bus services."
            ]
        }
        
        # Determine response category based on user message
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            response = random.choice(responses['greeting'])
        elif any(word in user_message for word in ['schedule', 'time', 'departure', 'arrival', 'timetable']):
            response = random.choice(responses['schedule'])
        elif any(word in user_message for word in ['track', 'tracking', 'location', 'where', 'live', 'map']):
            response = random.choice(responses['tracking'])
        elif any(word in user_message for word in ['book', 'booking', 'seat', 'reserve', 'reservation']):
            response = random.choice(responses['booking'])
        elif any(word in user_message for word in ['bus', 'buses', 'ronobheri', 'agnibina', 'bhorer alo']):
            response = random.choice(responses['bus_names'])
        elif any(word in user_message for word in ['help', 'assist', 'support', 'what can you do']):
            response = random.choice(responses['help'])
        else:
            response = random.choice(responses['default'])
        
        return JsonResponse({'response': response})
        
    except json.JSONDecodeError:
        return JsonResponse({'response': 'Sorry, I had trouble understanding your message. Please try again.'}, status=400)
    except Exception as e:
        return JsonResponse({'response': 'Sorry, I encountered an error. Please try again later.'}, status=500)
