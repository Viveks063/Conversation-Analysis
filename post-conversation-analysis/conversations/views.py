from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, ConversationAnalysis
from .serializers import (
    ConversationSerializer, MessageSerializer, 
    ConversationAnalysisSerializer, ConversationDetailSerializer
)
from analysis.analyzer import ConversationAnalyzer

class MessageViewSet(viewsets.ModelViewSet):
    """API endpoints for managing messages"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['conversation', 'sender']


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing conversations.
    
    Endpoints:
    - POST /api/conversations/ - Create new conversation
    - GET /api/conversations/ - List all conversations
    - GET /api/conversations/{id}/ - Get conversation details
    - POST /api/conversations/{id}/analyze/ - Trigger analysis
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    def get_serializer_class(self):
        """Use detailed serializer when retrieving single conversation"""
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer
    
    @action(detail=False, methods=['post'], url_path='batch-create')
    def batch_create(self, request):
        """
        Create a conversation with messages in one request.
        
        Expected JSON format:
        {
            "title": "Order Support",
            "messages": [
                {"sender": "user", "text": "Hi"},
                {"sender": "ai", "text": "Hello!"}
            ]
        }
        """
        title = request.data.get('title', 'Untitled')
        messages_data = request.data.get('messages', [])
        
        if not messages_data:
            return Response(
                {"error": "No messages provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create conversation
        conversation = Conversation.objects.create(title=title)
        
        # Create all messages
        for msg_data in messages_data:
            Message.objects.create(
                conversation=conversation,
                sender=msg_data.get('sender'),
                text=msg_data.get('text', '')
            )
        
        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """
        Trigger analysis on a specific conversation.
        
        Example: POST /api/conversations/1/analyze/
        """
        conversation = self.get_object()
        
        try:
            analyzer = ConversationAnalyzer()
            metrics = analyzer.analyze_conversation(conversation)
            
            # Create or update analysis record
            analysis, created = ConversationAnalysis.objects.update_or_create(
                conversation=conversation,
                defaults=metrics
            )
            
            conversation.is_analyzed = True
            conversation.save()
            
            serializer = ConversationAnalysisSerializer(analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get aggregated analytics across all conversations.
        
        Example: GET /api/conversations/analytics/
        """
        analyses = ConversationAnalysis.objects.all()
        
        if not analyses.exists():
            return Response({"message": "No analyzed conversations yet"})
        
        total = analyses.count()
        avg_overall_score = sum(a.overall_score for a in analyses) / total
        avg_sentiment_score = sum(a.sentiment_score for a in analyses) / total
        escalation_count = analyses.filter(escalation_needed=True).count()
        resolution_count = analyses.filter(resolution=True).count()
        
        stats = {
            "total_conversations": total,
            "average_overall_score": round(avg_overall_score, 2),
            "average_sentiment_score": round(avg_sentiment_score, 2),
            "conversations_needing_escalation": escalation_count,
            "conversations_resolved": resolution_count,
            "resolution_rate": round((resolution_count / total * 100), 2) if total > 0 else 0,
        }
        
        return Response(stats)


class ConversationAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints for viewing analysis results.
    
    Endpoints:
    - GET /api/analysis/ - List all analyses
    - GET /api/analysis/{id}/ - Get specific analysis
    """
    queryset = ConversationAnalysis.objects.all()
    serializer_class = ConversationAnalysisSerializer
    filterset_fields = ['conversation', 'sentiment', 'escalation_needed', 'resolution']