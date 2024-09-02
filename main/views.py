from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FriendRequest
from .serializers import FriendRequestSerializer, UserSerializer, LoginSerializer

# Pagination class to limit results to 10 per page
class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'].lower())
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ProtectedView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Authenticated request!'}, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Extract the search query from the request parameters for email or username
        search_query = self.request.query_params.get('search', '').strip().lower()

        if search_query:
            return User.objects.filter(
                Q(email__iexact=search_query) | Q(email__icontains=search_query) | Q(username__icontains=search_query)
            )
        return User.objects.none()
    
# Throttle class to limit sending of friend requests (3 requests per minute)
class FriendRequestRateThrottle(UserRateThrottle):
    rate = '3/min'

class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class AcceptFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            friend_request = self.get_object()
            print(friend_request.receiver,friend_request.status,request.user,friend_request.receiver != request.user,friend_request.status != 'pending',friend_request.receiver != request.user or friend_request.status != 'pending')
            if friend_request.receiver == request.user or friend_request.status != 'pending':
                return Response({"error": "Friend request not found or already processed."}, status=status.HTTP_404_NOT_FOUND)
            
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            friend_request = self.get_object()
            if friend_request.receiver != request.user or friend_request.status != 'pending':
                return Response({"error": "Friend request not found or already processed."}, status=status.HTTP_404_NOT_FOUND)
            
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accepted_requests = FriendRequest.objects.filter(
            Q(sender=user, status='accepted') | Q(receiver=user, status='accepted')
        )
        friend_ids = {fr.sender.id if fr.receiver == user else fr.receiver.id for fr in accepted_requests}
        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status='pending')
