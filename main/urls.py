from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ProtectedView,
    UserSearchView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    FriendsListView,
    PendingFriendRequestsView
)
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:pk>/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/<int:pk>/reject/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
