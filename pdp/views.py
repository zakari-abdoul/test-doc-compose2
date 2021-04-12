import os
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Pdp_IN, Pdp_OUT
from pdp.serializers import FilePdpSerializer, ParameterwPdpSerializer, Pdp_IN_Serializer, Pdp_OUT_Serializer  
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from datetime import datetime
import time



#####################################################################
#####################################################################
class PdpViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Pdp_IN.objects.all()
    serializer_class = Pdp_IN_Serializer
    # filterset_fields = ['PLMN_Carrier']
    search_fields = ['^Date']
    # ordering_fields = ['create_at']
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ParameterwPdpSerializer)
    def parametrepdp(self, request, *args, **kwargs):
        serializer = ParameterwPdpSerializer(data=request.data)
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
                queryset = Pdp_OUT.objects.filter(Opérateur=country_operator).filter(Date__gte=dateDebut).filter(Date__lte=dateFin)
                razbi = Pdp_OUT_Serializer(queryset, many=True)
            else:
                queryset = Pdp_IN.objects.filter(Opérateur=country_operator).filter(Date__gte=dateDebut).filter(Date__lte=dateFin)
                razbi = Pdp_In_Serializer(queryset, many=True)

            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FilePdpSerializer)
    def uploadPdp(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        serializer = FilePdpSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['inputFile']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
            print(df)
            liste = []
            if serializer.validated_data['type'] =="OUT":
                liste = insertData(df, Pdp_OUT, "out")
            else:
                liste = insertData(df, Pdp_IN, "in")


            return Response({"numberofligne": len(liste), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def insertData(df, object, roam):
    liste = []
    i = 1
    while i < len(df): 
        if roam == "out":
            pdp: object = object(
                Date=df["Date"][i], Operator=df["Operator"][i],
                GTP_C_Procedure_Attempts=df["GTP-C Procedure Attempts"][i], GTP_C_Procedure_Failures=df["GTP-C Procedure Failures"][i],
                GTP_C_Procedure_Failure=df["GTP-C Procedure Failure %"][i], GTP_C_Procedure_Average_Latency_msec=df["GTP-C Procedure Average Latency (msec)"][i], Eff_PDP_Act=df["Eff PDP Act"][i],
            )
        else:
            pdp: object = object(
                Date=df["Date"][i], Operator=df["Operator"][i],
                GTP_C_Procedure_Attempts_IN=df["GTP-C Procedure Attempts IN"][i], GTP_C_Procedure_Failures_IN=df["GTP-C Procedure Failures IN"][i],
                GTP_C_Procedure_Failure_IN =df["GTP-C Procedure Failure % IN"][i], GTP_C_Procedure_Average_Latency_msec_IN=df["GTP-C Procedure Average Latency (msec) IN"][i], Eff_PDP_Act_IN=df["Eff PDP Act IN"][i],
        )
        i = i + 1
        liste.append(pdp)           

    data = object.objects.bulk_create(liste)
    return data