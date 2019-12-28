from rest_framework import serializers
from apps.data.models import KeyVal


class KeyValListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(instance)
        book_mapping = {key_val.id: key_val for key_val in instance}
        data_mapping = {item['key']: item['value'] for item in validated_data}
        print('-----------------------00')
        print(data_mapping)
        print(book_mapping)
        # Perform updates.
        ret = []
        for key, value in data_mapping.items():
            key_val = book_mapping.get(key, None)
            print("---------------1")
            print(key_val)
            if key_val:
                d = {'value': value}
                ret.append(self.child.update(key_val, d))
        return ret


class KeyValStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVal
        fields = ('key', 'value',)
        list_serializer_class = KeyValListSerializer

    #  def update(self,instance,validated_data):
    #      pass
