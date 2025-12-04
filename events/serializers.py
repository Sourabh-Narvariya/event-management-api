from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, RSVP, Review, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'bio', 'profile_picture']


class EventSerializer(serializers.ModelSerializer):
    organizer = UserProfileSerializer(source='organizer.profile', read_only=True)
    attendee_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'organizer', 'title', 'description', 'location', 'start_datetime', 
                  'end_datetime', 'capacity', 'status', 'image_url', 'attendee_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_attendee_count(self, obj):
        return obj.get_attendee_count()


class RSVPSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'event', 'event_title', 'user', 'user_name', 'status', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'event_title', 'author', 'author_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
