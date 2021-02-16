from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
from .resources import SaiResource, Sai_OUT_Resource
from .models import Sai_IN, Sai_OUT
# Serializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from sai.serializers import Sai_IN_Serializer, Sai_OUT_Serializer, Sai_OUT_Post_Serializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import generics



#############################################################
# This part is for the SAI IN
#############################################################
@api_view(['POST'])
def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = SaiSerializer()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return Response(serializer.data)



@api_view(['GET', 'POST'])
def Sai_IN_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Sai_IN.objects.all()
        serializer = Sai_IN_Serializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SaiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Sai_IN_time_list(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Sai.objects.filter(Type=pk)[:20]
        serializer = SaiSerializer(snippets, many=True)
        # for data in serializer.data:
        #     print(data)
        #     print(data['Total_Transactions'])
        return Response(serializer.data)





@api_view(['GET','DELETE'])
def Sai_IN_detail(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Sai.objects.filter(id=pk)
        serializer = SaiSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        snippets = Sai.objects.filter(id=pk)
        snippets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


#############################################################
# This part is for the SAI OUT
#############################################################
#  Importing datafile by admin
@api_view(['POST'])
def import_data_SAI_OUT(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = Sai_OUT_Serializer()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return Response(serializer.data)

# class Sai_OUT_list(generics.ListCreateAPIView):
#     queryset = Sai_OUT.objects.all()
#     serializer_class = Sai_OUT_Serializer


@api_view(['GET', 'POST'])
def Sai_OUT_list(request):
    """
    List of all code snippets, or create a new SAI OUT List.
    """
    if request.method == 'GET':
        snippets = Sai_OUT.objects.all()[:20]
        serializer = Sai_OUT_Serializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':        
        donnee=request.data     
        serializer = Sai_OUT_Post_Serializer(data=donnee)
        if serializer.is_valid():
            affiche = Sai_OUT.objects.filter(Interval_Time=donnee["Interval_Time"], Opcode=donnee["Opcode"])
            razbi = Sai_OUT_Serializer(affiche, many=True)
            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','POST'])
# def Sai_OUT_time_list(request, pk):
#     if request.method == 'GET':
#         snippets = Sai_OUT.objects.filter(Interval_Time=pk)[:10]
#         serializer = Sai_OUT_Serializer(snippets, many=True)
#         return Response(serializer.data)  
    

#     elif request.method == 'POST':
#         data = request.data
#         serializer = sai_OUT_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)