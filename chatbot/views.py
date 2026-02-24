from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from chatbot.chatbot_manager import generate_reply
from students.models import SemesterResult

# Create your views here.

@login_required(login_url='signin')
def chatbot(request):

    if request.user.userprofile.role != 'student':
        return redirect('tutor_dashboard')

    return render(request, "chatbot/chatbot.html")

@csrf_exempt
def reply(request):
    if request.method == "POST":
        user = request.user.userprofile.student
        data = json.loads(request.body.decode("utf-8"))

        user_message = data.get("message")

        reply =generate_reply(user_message)

        if reply == "sgpa":
            sem_results = SemesterResult.objects.filter(student=user)
            all_sgpa = []
            for sem in sem_results:
                all_sgpa.append(sem.sgpa)
            sgpa = round(sum(all_sgpa)/len(all_sgpa), 2)
            reply = f"Your current SGPA is {sgpa}"

        if isinstance(reply, dict):
            sem_results = SemesterResult.objects.filter(student=user)
            all_sgpa = []
            for sem in sem_results:
                all_sgpa.append(sem.sgpa)
            target_cgpa = reply['percentage'] / 10

            required = round((target_cgpa * (len(all_sgpa)+1)) - sum(all_sgpa), 2)

            print(all_sgpa)
            print("CGPA", sum(all_sgpa)/len(all_sgpa))
            print("CGPA", (sum(all_sgpa)+required)/(len(all_sgpa)+1))
            print(required)
        
            if required < 10:
                reply = f"You need {required} SGPA in next semester for achieving {target_cgpa} CGPA"
            else:
                reply = f"You can't achieve {target_cgpa} CGPA only through next semester"

        return JsonResponse({
            "reply": reply
        })
    return JsonResponse({"error": "Invalid request"})