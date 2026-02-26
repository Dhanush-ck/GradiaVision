from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from chatbot.chatbot_manager import generate_reply
from students.models import SemesterResult
from prediction.models import Prediction
from prediction.models import PredictionData
from prediction.predict import predict_score

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

        if reply == 'change':
            return JsonResponse({
                "reply": "Usage: /change &lt;toughness&gt; &lt;study hours&gt; &lt;planned effort&gt; <br> toughness -> 1-5 <br> planned efforts -> 1-5 <br> Eg: /change 4 3 5",
                "help": 'help',
            })

        if isinstance(reply, dict):
            if reply['type'] == 'change':
                toughness = reply['values'][0]
                study_hours = reply['values'][1]
                planned_effort = reply['values'][2]

                if PredictionData.objects.filter(student=user).exists():
                    prediction_data = PredictionData.objects.get(student=user)
                    prediction_data.avg_difficulty = toughness
                    prediction_data.avg_study_hours = study_hours
                    prediction_data.planned_effort = planned_effort
                    prediction_data.save()

                    predicted_score = predict_score(
                        prediction_data.prev_sgpa,
                        prediction_data.avg_sgpa ,
                        prediction_data.sgpa_trend,
                        prediction_data.avg_marks,
                        prediction_data.avg_difficulty,
                        prediction_data.avg_study_hours,
                        prediction_data.planned_effort,
                    )

                    prediction = Prediction.objects.get(student=user)
                    prediction.predicted_sgpa = predicted_score
                    prediction.save()

                    return JsonResponse({
                        'reply': f"Successfully Updated <br> The new predicted score is {predicted_score} ",
                        'help': 'help'
                    })

                else: 
                    return JsonResponse({
                        'reply': "Sorry you don't have any previous prediction data."
                    })

            elif reply['type'] == 'percentage':
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