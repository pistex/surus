import pprint
from rest_framework import viewsets
from .models import Debugger
from .serializers import DebuggerSerializer

class DebuggingAPIView(viewsets.ModelViewSet):
    queryset = Debugger.objects.all()
    serializer_class = DebuggerSerializer

    def create(self, request, *args, **kwargs):
        print("create method of debugging endpoint is called")
        return super(DebuggingAPIView, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print("list method of debugging endpoint is called")
        pprint.pprint(self.request.user.is_authenticated)
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
