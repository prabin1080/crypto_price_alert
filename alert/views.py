from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .cache import alert_list_cache
from .models import Alert
from .paginations import PageNumberPagination
from .permissions import IsAuthenticated, AlertPermission
from .serializers import AlertSerializer


class AlertListCreateAPIView(ListCreateAPIView):
    """
    GET can take three query params - (page_size, page, status)
    """
    permission_classes = (IsAuthenticated, )
    queryset = Alert.objects.order_by('-created')
    serializer_class = AlertSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        _status = self.request.query_params.get('status')
        if _status is not None:
            queryset = queryset.filter(status=_status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        extra_key = request.get_full_path()
        res = alert_list_cache.get(request.user.pk, extra_key=extra_key)
        if res:
            return Response(res)
        res = super().get(request, *args, **kwargs)
        if res.status_code == status.HTTP_200_OK:
            alert_list_cache.set(request.user.pk, res.data, extra_key=extra_key)
        return res


class AlertRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AlertPermission,)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def perform_update(self, serializer):
        alert_list_cache.delete(self.request.user.pk)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        alert_list_cache.delete(self.request.user.pk)
        instance.soft_delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
