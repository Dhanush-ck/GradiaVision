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

        if reply == "cgpa":
            sem_results = SemesterResult.objects.filter(student=user)
            all_sgpa = []
            for sem in sem_results:
                all_sgpa.append(sem.sgpa)
            cgpa = round(sum(all_sgpa)/len(all_sgpa), 2)
            reply = f"Your current CGPA is {cgpa}"

        if reply == 'predict':
            return JsonResponse({
                "reply": """<b>/predict</b> – Estimate your next semester performance 🔮 <br><br>

                            <b>How to use:</b> <br>
                            /predict &lt;semester_toughness&gt; &lt;avg_study_hours&gt; &lt;planned_effort&gt; <br><br>

                            <b>Value Ranges:</b> <br>
                            • Semester Toughness → 1 (Very Easy) to 5 (Very Tough) <br>
                            • Average Study Hours → 0 to 12 hours per day <br>
                            • Planned Effort → 1 (Low) to 5 (Maximum) <br><br>

                            <b>Example:</b> <br>
                            /predict 4 3 5 <br><br>

                            This means: <br>
                            Tough semester, 3 study hours per day, and strong effort planned. """,
                "help": 'help',
            })

        if isinstance(reply, dict):
            if reply['type'] == 'predict':
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
                current_cgpa = round(sum(all_sgpa)/len(all_sgpa), 2)
                target_cgpa = reply['percentage'] / 10
                if target_cgpa < current_cgpa:
                    return JsonResponse({
                        "reply": f"You already have {current_cgpa} CGPA"
                    })

                required = round((target_cgpa * (len(all_sgpa)+1)) - sum(all_sgpa), 2)


                # print(all_sgpa)
                # print("CGPA", current_cgpa)
                # print("CGPA", (sum(all_sgpa)+required)/(len(all_sgpa)+1))
                # print(required)
            
                if required < 10:
                    reply = f"You need {required} SGPA in next semester for achieving {target_cgpa} CGPA"
                else:
                    reply = f"You can't achieve {target_cgpa} CGPA only through next semester"

        return JsonResponse({
            "reply": reply
        })
    return JsonResponse({"error": "Invalid request"})