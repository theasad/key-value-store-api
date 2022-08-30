from rest_framework import generics, status, views
from rest_framework.response import Response
from django.conf import settings
from apps.data.serializers import KeyValStoreSerializer

from apps.data.models import KeyVal
from apps.data.utils import reset_ttl, format_pair


class KeyValAPIView(views.APIView):
    def post(self, request, format=None):
        if data := self.request.data:
            # Formating data with key and value
            data_list = [{'key': key, 'value': value}
                         for key, value in data.items()]
            serializer = KeyValStoreSerializer(data=data_list, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = format_pair(serializer.data)
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({'details': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        keys = request.GET.get('keys')
        keys_list = keys.split(',') if keys else []
        queryset = KeyVal.objects.non_expired()
        if keys_list:
            queryset = queryset.filter(key__in=keys_list)
            # Update ttl with new ttl
            reset_ttl(queryset)
        serializer = KeyValStoreSerializer(queryset, many=True)
        response = format_pair(serializer.data)
        return Response(response)

    def patch(self, request, *args, **kwargs):
        if not (data := request.data):
            return Response({'details': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        # Formating data with key and value
        non_expired_kv_queryset = KeyVal.objects.non_expired()
        key_list = []
        for key, value in data.items():
            try:
                kv_obj = non_expired_kv_queryset.get(key=key)
                kv_obj.value = value
                kv_obj.save()
                key_list.append(key)
            except KeyVal.DoesNotExist:
                pass
        queryset = non_expired_kv_queryset.filter(key__in=key_list)
        serializer = KeyValStoreSerializer(queryset, many=True)
        response = format_pair(serializer.data)
        return Response(response, status=status.HTTP_200_OK)
