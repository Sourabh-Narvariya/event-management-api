from django.contrib import admin
from .models import Event, RSVP, Review, UserProfile

admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Review)
admin.site.register(UserProfile)
