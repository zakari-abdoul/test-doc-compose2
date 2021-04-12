import os
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Sai_IN, Sai_OUT
from sai.serializers import Sai_IN_Serializer, Sai_OUT_Serializer, FileSaiSerializer,ParameterwSaiSerializer
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
import time




#############################################################
# This part is for the SAI IN
#############################################################
@api_view(['POST'])
def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = Sai_IN_Serializer()
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

        return Response(result)



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
        serializer = Sai_IN_Serializer(data=request.data)
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
        snippets = Sai_IN.objects.filter(Type=pk)[:20]
        serializer = Sai_IN_Serializer(snippets, many=True)
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
        snippets = Sai_IN.objects.filter(id=pk)
        serializer = Sai_IN_Serializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        snippets = Sai_IN.objects.filter(id=pk)
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

        return Response(result)

# class Sai_OUT_list(generics.ListCreateAPIView):
#     queryset = Sai_OUT.objects.all()
#     serializer_class = Sai_OUT_Serializer


@api_view(['GET', 'POST'])
def Sai_OUT_list(request):
    """
    List of all code snippets, or create a new SAI OUT List.
    """
    if request.method == 'GET':
        sai_out = Sai_IN.objects.all()[:20]
        serializer = Sai_IN_Serializer(sai_out, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':        
        donnee=request.data     
        serializer = Sai_OUT_Post_Serializer(data=donnee)
        if serializer.is_valid():
            affiche = Sai_OUT.objects.filter(Interval_Time=donnee["Interval_Time"], Opcode=donnee["Opcode"])
            razbi = Sai_OUT_Serializer(affiche, many=True)
            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# def statsbyDate(transfert_serializer_part):
#     my_list = {}
#     for data in transfert_serializer_part:
#         datestring = data["create_at"]
#         date_time_obj =datetime.datetime.strptime(datestring[:-1], "%Y-%m-%dT%H:%M:%S.%f")
#
#         if str(date_time_obj.date()) in my_list:
#             my_list.update({str(date_time_obj.date()): my_list[str(date_time_obj.date())] + data["montant"]})
#         else:
#             my_list[str(date_time_obj.date())] = data["montant"]
#     return my_list
#
#

class SaiViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Sai_OUT.objects.all()
    serializer_class = Sai_OUT_Serializer
    # filterset_fields = ['PLMN_Carrier']
    search_fields = ['^PLMN_Carrier']
    # ordering_fields = ['create_at']
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(methods=['get'], detail=False, url_name='attempssai')
    def getattemps(self, request, *args, **kwargs):

        type = kwargs['target_id']
        if type == "out":
            #queryset = Sai_OUT.objects.all()[:1000]
            queryset = Sai_OUT.objects.all()
            razbi = Sai_OUT_Serializer(queryset, many=True)
        else:
            queryset = Sai_IN.objects.all()
            razbi = Sai_IN_Serializer(queryset, many=True)
        my_list = {}
        for data in razbi.data:
            #montan = montan + data["montant"]
            if data["Interval_Time"] in my_list:
                current = my_list[data["Interval_Time"]] + data["EFF"]
                my_list.update({data["Interval_Time"]: current/2})
            else:
                my_list[data["Interval_Time"]] = data["EFF"]

        return Response({"liste": my_list})

    @action(detail=False, methods=['post'], serializer_class=ParameterwSaiSerializer)
    def parametresai(self, request, *args, **kwargs):
        serializer = ParameterwSaiSerializer(data=request.data)
        if serializer.is_valid():
            dateDebut = serializer.validated_data['dateDebut']
            dateFin = serializer.validated_data['dateFin']
            country_operator = serializer.validated_data['country_operator']
            roaming = serializer.validated_data['roaming']
            
            # Creation et conversion des variables date            
            # my_time1 = time.strptime(dateDebut, '%b %d, %Y %I:%M')
            # my_time2 = time.strptime(dateFin, '%b %d, %Y %I:%M')
            # timestamp1 = time.mktime(my_time1)
            # timestamp2 = time.mktime(my_time2)
            # Conversion de Interval_Time en seconde
            # k = Sai_OUT.objects.get(Interval_Time)
            # CInterval_Time = time.strptime(k, '%b %d, %Y %I:%M')
            # Interval_Time_finale = time.mktime(CInterval_Time)

            if roaming == "OUT":
                queryset1 = Sai_OUT.objects.filter(PLMN_Carrier=country_operator).filter(Interval_Time_finale__gte=dateDebut).filter(Interval_Time_finale__lte=dateFin)
                razbi = Sai_OUT_Serializer(queryset1, many=True)                               

            else:
                queryset = Sai_IN.objects.filter(PLMN_Carrier=country_operator).filter(Interval_Time__gte=dateDebut).filter(Interval_Time__lte=dateFin)
                razbi = Sai_IN_Serializer(queryset, many=True)
                

            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FileSaiSerializer)
    def uploadsai(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        serializer = FileSaiSerializer(data=request.data)
        if serializer.is_valid():

            uploaded_file = serializer.validated_data['inputFile']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
            # df_new = df.rename(columns={'Interval Time': 'Interval_Time', 'Service': 'Service',
            #                             'PLMN Carrier': 'PLMN_Carrier', 'Direction': 'Direction',
            #                             'Opcode': 'Opcode', 'HVA': 'HVA', 'EFF': 'EFF',
            #                             'Total Transactions': 'Total_Transactions',
            #                             'Failed Transactions': 'Failed_Transactions'})

            print(df)
            #print(df_new)

            liste = []
            if serializer.validated_data['type'] =="OUT":
                liste = insertData(df, Sai_OUT, "out")
            else:
                liste = insertData(df, Sai_IN, "in")


            return Response({"numberofligne": len(liste), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def insertData(df, object, roam):
    liste = []
    i = 1
    if roam == "in":
        i = 4
    while i < len(df):
        if roam == "out":
            sai: object = object(
                Interval_Time=df["Interval Time"][i], PLMN_Carrier=df["PLMN Carrier"][i],
                Direction=df["Direction"][i], Service=df["Service"][i],
                Opcode=df["Opcode"][i], HVA=df["HVA"][i], Total_Transactions=df["Total Transactions"][i],
                Failed_Transactions=df["Failed Transactions"][i], EFF=df["EFF"][i],
            )
        else:
            sai: object = object(
                Interval_Time=df["Unnamed: 0"][i], PLMN_Carrier=df["Unnamed: 1"][i],
                Direction=df["Unnamed: 2"][i], Service=df["Unnamed: 3"][i],
                Opcode=df["Unnamed: 4"][i], HVA=df["Unnamed: 5"][i], Total_Transactions=df["Unnamed: 6"][i],
                Failed_Transactions=df["Unnamed: 7"][i], EFF=df["Unnamed: 8"][i],
            )
        i = i + 1
        # insert this part if we just need to verify the true values
        
        # if(sai.PLMN_Carrier == sai.HVA):
        liste.append(sai)
        # elif (sai.HVA == 221_Senegal Orange)
            # return ("On prends pas en compte les données si Les PLMN_Carrier sont different des HVA")
            

    data = object.objects.bulk_create(liste)
    return data
