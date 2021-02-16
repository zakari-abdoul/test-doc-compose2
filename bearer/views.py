from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
from .resources import BearerResource
from .models import Bearer
from bearer.serializers import BearerSerializer
from rest_framework import generics
# Serializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


# to import the bearer
@api_view(['POST'])
def import_Bearer(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = BearerResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        # if file_format == 'CSV':
        #     imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
        #     result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        # elif file_format == 'JSON':
        #     imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
        #     # Testing data import
        #     result = employee_resource.import_data(dataset, dry_run=True) 
            
        # if not result.has_errors():
        #     # Import now
        #     #
        #     employee_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')


#  the API view for bearer GET and POST
@api_view(['GET', 'POST'])
def Bearer_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Bearer.objects.all()[:20]
        serializer = BearerSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data=request.data
        serializer = BearerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  the API view for bearer GET with a primary key
@api_view(['GET', 'DELETE'])
def Bearer_time_list(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Bearer.objects.filter(Interval_Time=pk)[:20]
        serializer = BearerSerializer(snippets, many=True)
        # for data in serializer.data:
        #     print(data)
        #     print(data['Total_Transactions'])
        return Response(serializer.data)

    elif request.method == 'DELETE':
        snippets = Bearer.objects.filter()
        snippets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
