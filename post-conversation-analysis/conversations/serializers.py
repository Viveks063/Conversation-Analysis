from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for individual messages"""
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Basic conversation serializer for list view"""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_analyzed', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_analyzed']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with all messages included"""
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_analyzed', 'messages']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_analyzed']


class ConversationAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for analysis results"""
    conversation_title = serializers.CharField(source='conversation.title', read_only=True)
    
    class Meta:
        model = ConversationAnalysis
        fields = [
            'id',
            'conversation',
            'conversation_title',
            'clarity_score',
            'relevance_score',
            'accuracy_score',
            'completeness_score',
            'sentiment',
            'sentiment_score',
            'empathy_score',
            'response_time_avg',
            'resolution',
            'escalation_needed',
            'fallback_count',
            'overall_score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'conversation', 'created_at', 'updated_at'
        ]