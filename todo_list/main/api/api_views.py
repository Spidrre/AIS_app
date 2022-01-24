from rest_framework.generics import ListAPIView

from .serializers import TestTaskSerializer
from ..models import Testtask


from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status


class TestTaskList(APIView):
    renderer_classes = [JSONRenderer]

    @staticmethod
    def get(request):
        if request.GET.get('title', None):
            test_task = Testtask.objects.filter(title__exact=request.GET.get('title'))
        else:
            test_task = Testtask.objects.all()
        serializer = TestTaskSerializer(test_task, many=True)
        return Response({'test_task': serializer.data})


    @staticmethod
    def post(request):
        serializer = TestTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ContactRequest Created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestTaskDetail(APIView):
    renderer_classes = [JSONRenderer]

    # HTTP GET
    def get(self, request, pk):
        test_task = self.get_object(pk)
        if not test_task:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TestTaskSerializer(test_task)
        return Response(serializer.data)

    # HTTP PUT/PATCH
    def put(self, request, pk):
        test_task = self.get_object(pk)
        if not test_task:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TestTaskSerializer(test_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ContactRequest Updated!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # HTTP DELETE
    def delete(self, request, pk):
        test_task = self.get_object(pk)
        if not test_task:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        test_task.delete()
        return Response({'message': 'ContactRequest Deleted!'}, status=status.HTTP_200_OK)

    @staticmethod
    def get_object(pk):
        try:
            return Testtask.objects.get(pk=pk)
        except Testtask.DoesNotExist:
            return None