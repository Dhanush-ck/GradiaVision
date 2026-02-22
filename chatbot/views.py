from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from chatbot.chatbot_manager import generate_reply

# Create your views here.

@login_required(login_url='signin')
def chatbot(request):

    if request.user.userprofile.role != 'student':
        return redirect('tutor_dashboard')

    return render(request, "chatbot/chatbot.html")

@csrf_exempt
def reply(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        user_message = data.get("message")

        reply =generate_reply(user_message)

        return JsonResponse({
            "reply": reply
        })
    return JsonResponse({"error": "Invalid request"})