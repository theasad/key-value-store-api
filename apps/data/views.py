from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from apps.data.serializers import KeyValStoreSerializer

from apps.data.models import KeyVal
from apps.data.utils import reset_ttl, format_pair


class KeyValListCreateView(generics.ListCreateAPIView):
    serializer_class = KeyValStoreSerializer
    permission_classes = ()
    queryset = KeyVal.objects.all()

    def create(self, request, *args, **kwargs):
        data = self.request.data
        if data:
            # Formating data with key and value
            data_list = [{'key': key, 'value': value}
                         for key, value in data.items()]
            serializer = self.get_serializer(data=data_list, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'details': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        keys = self.request.GET.get('keys')
        keys_list = keys.split(',') if keys else []
        queryset = self.get_queryset()
        if keys_list:
            queryset = queryset.filter(key__in=keys_list)
        response = format_pair(queryset)
        return Response(response)


class KeyValUpdateView(generics.UpdateAPIView):
    serializer_class = KeyValStoreSerializer
    permission_classes = ()
    queryset = KeyVal.objects.all()

    def patch(self, request, *args, **kwargs):
        data = self.request.data
        if data:
            # Formating data with key and value
            non_expired_kv_queryset = KeyVal.objects.non_expired()
            data_list = []
            kv_obj = []
            for key, value in data.items():
                try:
                    kv_obj.append(non_expired_kv_queryset.get(key=key))
                    data_list.append({'key': key, 'value': value})
                    # kv_obj.value = value
                    # kv_obj.save()
                except KeyVal.DoesNotExist:
                    pass
            # data_list = [{'key': key, 'value': value}
            #              for key, value in data.items()]
            print(data_list)
            print(kv_obj)
            serializer = self.get_serializer(
                data=data_list, instance=non_expired_kv_queryset, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
