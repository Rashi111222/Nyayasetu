from django.contrib import admin
from .models import Judgment, ActionPlan, OfficerReview

admin.site.register(Judgment)
admin.site.register(ActionPlan)
admin.site.register(OfficerReview)