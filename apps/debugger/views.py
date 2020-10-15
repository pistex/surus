from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.api.permissions import IsCreator, IsAuthor
from .models import Debugger
from .serializers import DebuggerSerializer

class DebuggingAPIView(viewsets.ModelViewSet):
    queryset = Debugger.objects.all()
    serializer_class = DebuggerSerializer

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     update_destroy = ['update', 'partial_update', 'destroy']
    #     if self.action == 'create':
    #         permission_classes = [IsCreator]
    #     elif self.action in update_destroy:
    #         permission_classes = [IsAuthor]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print("create method of debugging endpoint is called")
        return super(DebuggingAPIView, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print("list method of debugging endpoint is called")
        print(request.META)
        print(request.user)
        return super(DebuggingAPIView, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        print("retrieve method of debugging endpoint is called")
        return super(DebuggingAPIView, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print("update method of debugging endpoint is called")
        return super(DebuggingAPIView, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        print("partial update method of debugging endpoint is called")
        return super(DebuggingAPIView, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        print("destroy method of debugging endpoint is called")
        return super(DebuggingAPIView, self).destroy(request, *args, **kwargs)
