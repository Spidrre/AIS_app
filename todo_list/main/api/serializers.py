from rest_framework import serializers


from ..models import Testtask


class TestTaskSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField()
    title = serializers.CharField(max_length=100)

    class Meta:
        model = Testtask
        fields = [
            'id', 'number', 'title'
        ]


