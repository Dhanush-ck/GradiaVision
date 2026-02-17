from django.shortcuts import render
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

from chatbot.chatbot_manager import generate_reply

# Create your views here.

def chatbot(request):
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