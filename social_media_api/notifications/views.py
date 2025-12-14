from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark all unread notifications as read"""
        notifications = self.get_queryset().filter(read=False)
        notifications.update(read=True)
        return Response({'detail': f'Marked {notifications.count()} notifications as read.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)

# Notification list view (for backward compatibility)
class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
