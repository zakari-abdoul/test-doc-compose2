# from django.shortcuts import render
# from django.http import HttpResponse
# from tablib import Dataset
# from .resources import Pdp_IN_Resource
# from .models import Pdp_IN
# from .serializers import Pdp_IN_Serializer
# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.response import Response



# """
# This part is for the SAI In
# """
# @api_view(['POST'])
# def import_data(request):
#     if request.method == 'POST':
#         file_format = request.POST['file-format']
#         employee_resource = Pdp_IN_Serializer()
#         dataset = Dataset()
#         new_employees = request.FILES['importData']

#         if file_format == 'CSV':
#             imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
#             result = employee_resource.import_data(dataset, dry_run=True)                                                                 
#         elif file_format == 'JSON':
#             imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
#             # Testing data import
#             result = employee_resource.import_data(dataset, dry_run=True) 

#         if not result.has_errors():
#             # Import now
#             employee_resource.import_data(dataset, dry_run=False)

#     # return render(request, 'import.html') 
#     return Response(serializer.data)



# @api_view(['GET', 'POST'])
# def Pdp_IN_view(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Pdp_IN.objects.all()
#         serializer = Pdp_IN_Serializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = Pdp_IN_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)