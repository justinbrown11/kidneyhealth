from django.contrib import admin
from tracking.models import Profile, Comorbidity, Race, Lab, DailyEntry, Food, FoodHistory

admin.site.register(Comorbidity)
admin.site.register(Profile)
admin.site.register(Race)
admin.site.register(Lab)
admin.site.register(DailyEntry)
admin.site.register(Food)
admin.site.register(FoodHistory)