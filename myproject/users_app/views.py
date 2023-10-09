
from . import models
from .models import CustomUser, UserProfile
from .serialazers import UserProfileSerializer


# Create your views here.
class UserProfileViewSet(models.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)