import os
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Bearer_In, Bearer_Out
from bearer.serializers import Bearer_In_Serializer, Bearer_OUT_Serializer, FileBearerSerializer, ParameterwBearerSerializer 
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from datetime import datetime
import time


# to import the bearer
@api_view(['POST'])
def import_Bearer(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = BearerResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']  
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
#####################################################################
#####################################################################
class BearerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Bearer_Out.objects.all()
    serializer_class = Bearer_OUT_Serializer
    # filterset_fields = ['PLMN_Carrier']
    search_fields = ['^Date']
    # ordering_fields = ['create_at']
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ParameterwBearerSerializer)
    def parametre(self, request, *args, **kwargs):
        serializer = ParameterwBearerSerializer(data=request.data)
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
                queryset = Bearer_Out.objects.filter(Opérateur=country_operator).filter(Date__gte=dateDebut).filter(Date__lte=dateFin)
                razbi = Bearer_OUT_Serializer(queryset, many=True)
            else:
                queryset = Bearer_In.objects.filter(Opérateur=country_operator).filter(Date__gte=dateDebut).filter(Date__lte=dateFin)
                razbi = Bearer_In_Serializer(queryset, many=True)

            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FileBearerSerializer)
    def upload(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        serializer = FileBearerSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['inputFile']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
            print(df)
            liste = []
            if serializer.validated_data['type'] =="OUT":
                liste = insertData(df, Bearer_Out, "out")
            else:
                liste = insertData(df, Bearer_In, "in")


            return Response({"numberofligne": len(liste), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def insertData(df, object, roam):
    liste = []
    i = 1
    while i < len(df): 
        if roam == "out":
            bearer: object = object(
                Date = time.mktime(time.strptime(df["Date"][i], '%b %d, %Y %I:%M')),
                Opérateur=df["Opérateur"][i],
                GTPv2_C_Attempts_OUT=df["GTPv2-C Attempts OUT"][i], GTPv2_C_Failures_OUT=df["GTPv2-C Failures OUT"][i],
                GTPv2_C_Failure_OUT=df["GTPv2-C Failure OUT %"][i], GTPv2_C_Average_Latency_msec_OUT=df["GTPv2-C Average Latency (msec) OUT"][1], GTPv2_C_Average_Session_Duration_msec_OUT=df["GTPv2-C Average Session Duration (msec) OUT"][i],
                Efficacité_OUT=df["Efficacité OUT"][i],
            )
        else:
            bearer: object = object(
                Date = time.mktime(time.strptime(df["Date"][i], '%b %d, %Y %I:%M')),
                Opérateur=df["Opérateur"][i],
                GTPv2_C_Attempts_IN=df["GTPv2-C Attempts IN"][i], GTPv2_C_Failures_IN=df["GTPv2-C Failures IN"][i],
                GTPv2_C_Failure_IN=df["GTPv2-C Failure IN %"][i], GTPv2_C_Average_Latency_msec_IN=df["GTPv2-C Average Latency (msec) IN"][i],
                GTPv2_C_Average_Session_Duration_msec_IN=df["GTPv2-C Average Session Duration (msec) IN"][i],
                Efficacité_IN=df["Efficacité IN"][i],
        )
        i = i + 1
        liste.append(bearer)           

    data = object.objects.bulk_create(liste)
    return data