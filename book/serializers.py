from rest_framework import serializers
from.models import Book
from rest_framework.serializers import ModelSerializer
class BookSerializer(serializers.Serializer):
    book_name=serializers.CharField()
    author=serializers.CharField()
    price=serializers.IntegerField()
    def create(self,validated_data):
        return Book.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.book_name=validated_data.get("book_name")
        instance.author=validated_data.get("author")
        instance.price=validated_data.get("price")
        instance.save()
        return instance

class BookModelSerializers(ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"

class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()