from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Q
from .models import Lead, Notification
from .serializers import (
    LeadSerializer, 
    LeadCreateSerializer, 
    NotificationSerializer,
    NotificationUpdateSerializer
)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing leads (public form submissions).
    Public access for creation, admin access for management.
    """
    queryset = Lead.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LeadCreateSerializer
        return LeadSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Create a new lead from landing page form and generate notification"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        
        # Create notification for admin
        lead_type_display = lead.get_lead_type_display()
        notification_title = f"New {lead_type_display}"
        notification_message = (
            f"{lead.business_name} has submitted a {lead_type_display.lower()}. "
            f"Contact: {lead.email}, {lead.phone}"
        )
        
        Notification.objects.create(
            notification_type='lead_submission',
            title=notification_title,
            message=notification_message,
            related_lead=lead
        )
        
        return Response(
            LeadSerializer(lead).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics for admin dashboard"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Unauthorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_leads = Lead.objects.count()
        new_leads = Lead.objects.filter(status='new').count()
        demo_requests = Lead.objects.filter(lead_type='demo_request').count()
        automation_requests = Lead.objects.filter(lead_type='business_automation').count()
        
        return Response({
            'total_leads': total_leads,
            'new_leads': new_leads,
            'demo_requests': demo_requests,
            'automation_requests': automation_requests,
        })


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing admin notifications.
    Admin access only.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications count"""
        unread_count = self.queryset.filter(is_read=False).count()
        return Response({'unread_count': unread_count})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.queryset.update(is_read=True)
        return Response({'message': 'All notifications marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)
