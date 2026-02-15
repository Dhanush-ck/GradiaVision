from django.contrib import admin

from prediction.models import PredictionData
from prediction.models import Prediction

# Register your models here.
admin.site.register(PredictionData)
admin.site.register(Prediction)