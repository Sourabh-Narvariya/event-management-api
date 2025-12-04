from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsEventOrganizer, IsReviewAuthor


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'organizer']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_datetime', 'created_at']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsEventOrganizer]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def attend(self, request, pk=None):
        event = self.get_object()
        rsvp, created = RSVP.objects.update_or_create(
            event=event, user=request.user,
            defaults={'status': 'attending'}
        )
        return Response({'status': 'attending event'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unattend(self, request, pk=None):
        event = self.get_object()
        rsvp = RSVP.objects.filter(event=event, user=request.user).first()
        if rsvp:
            rsvp.delete()
        return Response({'status': 'not attending'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def attendees(self, request, pk=None):
        event = self.get_object()
        rsvps = RSVP.objects.filter(event=event, status='attending')
        serializer = RSVPSerializer(rsvps, many=True)
        return Response(serializer.data)


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all().order_by('-created_at')
    serializer_class = RSVPSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'status']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return RSVP.objects.filter(user=user).order_by('-created_at')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['event', 'rating']
    ordering_fields = ['rating', 'created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsReviewAuthor]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
