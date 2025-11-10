from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from conversations.models import Conversation, ConversationAnalysis
from .analyzer import ConversationAnalyzer
import logging

logger = logging.getLogger(__name__)


@shared_task
def analyze_new_conversations():
    """
    Celery task that runs daily to analyze all new conversations.
    
    This task:
    1. Finds conversations that haven't been analyzed yet
    2. Runs analysis on each
    3. Stores results in database
    4. Logs the results
    
    Scheduled to run daily at midnight (configured in settings.py)
    """
    logger.info("Starting automatic conversation analysis task...")
    
    # Get conversations that haven't been analyzed
    unanalyzed = Conversation.objects.filter(is_analyzed=False)
    count = unanalyzed.count()
    
    if count == 0:
        logger.info("No new conversations to analyze.")
        return {"status": "success", "analyzed": 0}
    
    logger.info(f"Found {count} unanalyzed conversations. Starting analysis...")
    
    analyzer = ConversationAnalyzer()
    analyzed_count = 0
    failed_count = 0
    
    for conversation in unanalyzed:
        try:
            # Run analysis
            metrics = analyzer.analyze_conversation(conversation)
            
            # Store in database
            ConversationAnalysis.objects.update_or_create(
                conversation=conversation,
                defaults=metrics
            )
            
            # Mark as analyzed
            conversation.is_analyzed = True
            conversation.save()
            
            analyzed_count += 1
            logger.debug(f"✓ Analyzed conversation {conversation.id}")
            
        except Exception as e:
            failed_count += 1
            logger.error(f"✗ Failed to analyze conversation {conversation.id}: {str(e)}")
    
    logger.info(
        f"Analysis complete. Analyzed: {analyzed_count}, Failed: {failed_count}"
    )
    
    return {
        "status": "success",
        "analyzed": analyzed_count,
        "failed": failed_count,
    }


@shared_task
def analyze_conversation_async(conversation_id):
    """
    Celery task for analyzing a single conversation asynchronously.
    
    Usage: Call this when you want immediate but non-blocking analysis
    analyze_conversation_async.delay(conversation_id=1)
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        analyzer = ConversationAnalyzer()
        metrics = analyzer.analyze_conversation(conversation)
        
        ConversationAnalysis.objects.update_or_create(
            conversation=conversation,
            defaults=metrics
        )
        
        conversation.is_analyzed = True
        conversation.save()
        
        logger.info(f"Async analysis complete for conversation {conversation_id}")
        return {"status": "success", "conversation_id": conversation_id}
    
    except Conversation.DoesNotExist:
        logger.error(f"Conversation {conversation_id} not found")
        return {"status": "error", "message": "Conversation not found"}
    except Exception as e:
        logger.error(f"Error analyzing conversation {conversation_id}: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def cleanup_old_analyses():
    """
    Optional cleanup task to remove analyses older than 90 days.
    Can be scheduled separately if needed.
    """
    cutoff_date = timezone.now() - timedelta(days=90)
    deleted_count, _ = ConversationAnalysis.objects.filter(
        created_at__lt=cutoff_date
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} old analyses")
    return {"status": "success", "deleted": deleted_count}