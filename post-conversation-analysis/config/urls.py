from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from conversations.views import ConversationViewSet, MessageViewSet, ConversationAnalysisViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'analysis', ConversationAnalysisViewSet, basename='analysis')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

# Optional: Add API auth
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]