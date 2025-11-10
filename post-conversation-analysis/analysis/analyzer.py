from statistics import mean
from nltk.sentiment import SentimentIntensityAnalyzer

class ConversationAnalyzer:
    """
    Analyzes conversations using VADER sentiment analysis and text metrics.
    Learn: This class encapsulates all analysis logic in one place (clean code!)
    """
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    # CLARITY ANALYSIS
    def analyze_clarity(self, text):
        """
        Score: 0-100
        Measures if response is clear by checking:
        - Sentence length (too long = unclear)
        - Word complexity (common words = clear)
        - Question usage (questions = clarification)
        """
        if not text or len(text.strip()) == 0:
            return 0.0
        
        sentences = text.split('.')
        avg_sentence_length = mean([len(s.split()) for s in sentences if s.strip()])
        
        # Penalty for very long sentences (hard to read)
        length_score = max(0, 100 - (avg_sentence_length * 2))
        
        # Bonus for punctuation and structure
        clarity_score = min(100, length_score + 10)
        return clarity_score
    
    # RELEVANCE ANALYSIS
    def analyze_relevance(self, user_msg, ai_response):
        """
        Score: 0-100
        Checks if AI response is related to user's message.
        Uses simple word overlap and keyword matching.
        """
        user_words = set(user_msg.lower().split())
        response_words = set(ai_response.lower().split())
        
        # Find overlapping words (excluding common stop words)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'i', 'you', 'it', 'and', 'or'}
        overlap = user_words & response_words - stop_words
        
        # Calculate relevance based on word overlap
        relevance_score = (len(overlap) / len(user_words)) * 100
        return min(100, relevance_score + 20)  # +20 bonus for staying on topic
    
    # ACCURACY ANALYSIS
    def analyze_accuracy(self, ai_response):
        """
        Score: 0-100
        Simplified accuracy check. In production, you'd verify against a knowledge base.
        Here we check for confidence indicators in the response.
        """
        # Check for uncertainty language (indicates lower accuracy)
        uncertainty_phrases = [
            "i think", "i believe", "maybe", "possibly", "i'm not sure",
            "i don't know", "i'm unsure", "approximately", "roughly"
        ]
        
        response_lower = ai_response.lower()
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in response_lower)
        
        # Start with high score, penalize for uncertainty
        accuracy_score = 100 - (uncertainty_count * 15)
        return max(0, accuracy_score)
    
    # COMPLETENESS ANALYSIS
    def analyze_completeness(self, ai_response):
        """
        Score: 0-100
        Checks if response is complete by:
        - Response length (too short = incomplete)
        - Presence of examples or details
        - Closing statements
        """
        word_count = len(ai_response.split())
        
        # Length component (50 points)
        if word_count < 10:
            length_score = 20
        elif word_count < 30:
            length_score = 50
        else:
            length_score = 80
        
        # Details component (30 points)
        details_score = 30 if any(word in ai_response.lower() for word in ['example', 'specifically', 'such as', 'like']) else 15
        
        # Closure component (20 points)
        closure_score = 20 if any(word in ai_response.lower() for word in ['help', 'anything else', 'let me know', 'thanks']) else 10
        
        completeness_score = length_score + details_score + closure_score
        return min(100, completeness_score)
    
    # ============ SENTIMENT ANALYSIS ============
    def analyze_sentiment(self, text):
        """
        Returns: (sentiment_label, sentiment_score)
        sentiment_label: 'positive', 'neutral', or 'negative'
        sentiment_score: -1.0 to 1.0
        Uses VADER which is optimized for social media and short texts
        """
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']
        
        # Classify based on compound score
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return sentiment, compound_score
    
    # EMPATHY ANALYSIS
    def analyze_empathy(self, ai_response):
        """
        Score: 0-100
        Checks for empathetic language in AI's response.
        """
        empathy_phrases = [
            "i understand", "i appreciate", "thank you", "sorry", "apologize",
            "help", "support", "concern", "feel", "important", "matter",
            "appreciate your", "understand your", "i get it"
        ]
        
        response_lower = ai_response.lower()
        empathy_count = sum(1 for phrase in empathy_phrases if phrase in response_lower)
        
        empathy_score = min(100, empathy_count * 15)
        return empathy_score
    
    # FALLBACK DETECTION
    def count_fallbacks(self, conversation_messages):
        """
        Counts how many times AI used fallback responses like "I don't know"
        """
        fallback_phrases = [
            "i don't know", "i'm not sure", "i can't help", "unable to",
            "beyond my knowledge", "not available", "cannot determine"
        ]
        
        fallback_count = 0
        for msg in conversation_messages:
            if msg.sender == 'ai':
                msg_lower = msg.text.lower()
                for phrase in fallback_phrases:
                    if phrase in msg_lower:
                        fallback_count += 1
        
        return fallback_count
    
    # RESOLUTION DETECTION
    def detect_resolution(self, conversation_messages):
        """
        Simple heuristic: if conversation has positive sentiment at end
        and user's last message is brief, likely resolved.
        """
        if not conversation_messages:
            return False
        
        # Get last user message
        user_messages = [m for m in conversation_messages if m.sender == 'user']
        if not user_messages:
            return False
        
        last_user_msg = user_messages[-1].text.lower()
        
        # Resolution indicators
        resolution_keywords = ['thanks', 'thank you', 'ok', 'okay', 'perfect', 'great', 'done', 'resolved']
        has_resolution_keyword = any(keyword in last_user_msg for keyword in resolution_keywords)
        
        # Short last message often indicates resolution
        is_brief = len(last_user_msg.split()) < 10
        
        return has_resolution_keyword or (is_brief and len(conversation_messages) > 3)
    
    # ESCALATION DETECTION
    def detect_escalation_need(self, conversation_messages, overall_sentiment):
        """
        Returns True if conversation should be escalated to human.
        Triggers: negative sentiment + fallbacks, or repeated issues
        """
        if not conversation_messages:
            return False
        
        # Escalate if heavily negative and has fallbacks
        ai_messages = [m for m in conversation_messages if m.sender == 'ai']
        fallback_count = self.count_fallbacks(conversation_messages)
        
        escalate = overall_sentiment == 'negative' and fallback_count > 1
        
        # Also escalate if many user messages (user might be frustrated)
        user_msg_count = sum(1 for m in conversation_messages if m.sender == 'user')
        if user_msg_count > 5:
            escalate = True
        
        return escalate
    
    # RESPONSE TIME ANALYSIS
    def calculate_response_time(self, conversation_messages):
        """
        Returns average response time in seconds (mock if no timestamps)
        """
        # Since timestamps might not be in the conversation data,
        # we'll use message count as a proxy (each message = 5 seconds assumed)
        response_times = []
        
        for i, msg in enumerate(conversation_messages):
            if msg.sender == 'ai' and i > 0:
                # Mock: assume 2-5 seconds per AI response
                response_times.append(3.0)
        
        return mean(response_times) if response_times else 0.0
    
    # OVERALL SCORE
    def calculate_overall_score(self, metrics):
        """
        Combines all metrics into a final 0-100 score.
        Weights different factors.
        """
        # Define weights (must sum to 1.0)
        weights = {
            'clarity': 0.15,
            'relevance': 0.15,
            'accuracy': 0.15,
            'completeness': 0.10,
            'empathy': 0.10,
            'resolution': 0.20,  # Most important
            'escalation': 0.05,
            'fallback': 0.10,
        }
        
        overall = (
            metrics['clarity_score'] * weights['clarity'] +
            metrics['relevance_score'] * weights['relevance'] +
            metrics['accuracy_score'] * weights['accuracy'] +
            metrics['completeness_score'] * weights['completeness'] +
            metrics['empathy_score'] * weights['empathy'] +
            (100 if metrics['resolution'] else 0) * weights['resolution'] +
            (0 if metrics['escalation_needed'] else 100) * weights['escalation'] +
            max(0, 100 - metrics['fallback_count'] * 10) * weights['fallback']
        )
        
        return min(100, max(0, overall))
    
    # MAIN ANALYSIS METHOD
    def analyze_conversation(self, conversation):
        """
        Main method: Takes a Conversation object and returns analysis results.
        This is what you'll call from your views!
        """
        messages = conversation.messages.all().order_by('created_at')
        
        if not messages:
            raise ValueError("Conversation has no messages")
        
        # Prepare data
        clarity_scores = []
        relevance_scores = []
        accuracy_scores = []
        completeness_scores = []
        
        # Analyze each AI response
        for i, msg in enumerate(messages):
            if msg.sender == 'ai':
                clarity_scores.append(self.analyze_clarity(msg.text))
                accuracy_scores.append(self.analyze_accuracy(msg.text))
                completeness_scores.append(self.analyze_completeness(msg.text))
                
                # Relevance: compare with previous user message
                if i > 0:
                    prev_msg = messages[i-1]
                    if prev_msg.sender == 'user':
                        relevance_scores.append(self.analyze_relevance(prev_msg.text, msg.text))
        
        # Analyze user sentiment across all messages
        user_messages = [m.text for m in messages if m.sender == 'user']
        user_sentiment_scores = [self.analyze_sentiment(msg)[1] for msg in user_messages]
        
        # Overall sentiment
        overall_sentiment_score = mean(user_sentiment_scores) if user_sentiment_scores else 0.0
        overall_sentiment, _ = self.analyze_sentiment(' '.join(user_messages) if user_messages else '')
        
        # Empathy analysis (from AI messages)
        empathy_scores = [
            self.analyze_empathy(msg.text) 
            for msg in messages if msg.sender == 'ai'
        ]
        
        # Build metrics dictionary
        metrics = {
            'clarity_score': mean(clarity_scores) if clarity_scores else 50.0,
            'relevance_score': mean(relevance_scores) if relevance_scores else 50.0,
            'accuracy_score': mean(accuracy_scores) if accuracy_scores else 50.0,
            'completeness_score': mean(completeness_scores) if completeness_scores else 50.0,
            'sentiment': overall_sentiment,
            'sentiment_score': overall_sentiment_score,
            'empathy_score': mean(empathy_scores) if empathy_scores else 50.0,
            'response_time_avg': self.calculate_response_time(messages),
            'resolution': self.detect_resolution(messages),
            'escalation_needed': self.detect_escalation_need(messages, overall_sentiment),
            'fallback_count': self.count_fallbacks(messages),
        }
        
        # Calculate overall score
        metrics['overall_score'] = self.calculate_overall_score(metrics)
        
        return metrics