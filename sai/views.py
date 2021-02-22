import os
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Sai_IN, Sai_OUT
from sai.serializers import Sai_IN_Serializer, Sai_OUT_Serializer, Sai_OUT_Post_Serializer, FileSaiSerializer, \
    ParameterwSaiSerializer
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response



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
# @api_view(['GET'])
# def statistiquesView(request, format=None):
#     """
#      recevoir les statistiques concernant les donnees de transfert
#     """
#     transfert_count = len(Sai_OUT.objects.all())
#     compte_count = len(Compte.objects.all())
#     serializer_part = CompteSerializer(Sai_OUT.objects.all(), many=True).data
#     transfert_serializer_part = TransfertSerializer(Sai_OUT.objects.all(), many=True).data
#     transfert_order_serializer_part = TransfertSerializer(Sai_OUT.objects.all().order_by("-create_at"), many=True).data
#     globalmontant = sommeTotal(serializer_part)
#     lastTransfert_serialize = TransfertSerializer(Sai_OUT.objects.all().order_by("-create_at")[:5], many=True).data
#     top3Transfert_serialize = TransfertSerializer(Sai_OUT.objects.all().order_by("-montant")[:3], many=True).data
#     user_serialize = UserSerializer(User.objects.all().order_by("date_joined")[:5], many=True).data
#     my_list = {}
#     valuesTab = []
#     #listeByDate = statsbyDate(transfert_serializer_part)
#     montan=0
#     for data in transfert_order_serializer_part:
#         montan = montan + data["montant"]
#         valuesTab.append(data["montant"])
#         if data["originalName"] in my_list:
#             my_list.update({data["originalName"]: my_list[data["originalName"]] + data["montant"]})
#         else:
#             my_list[data["originalName"]] = data["montant"]
#     print(my_list)
#     listeByDate = statsbyDate(transfert_serializer_part)
#     total_account = 0
#     return Response({"nbreTransfert": transfert_count, "globalmontant": globalmontant, "byDate": listeByDate,
#                      "liste": my_list, "valuesTab": valuesTab, "lastTransfert": lastTransfert_serialize,
#                      "userList": user_serialize, "top3": top3Transfert_serialize,})
    #return HttpResponse(transfert_count)@api_view(['GET'])


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


class SaiViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Sai_IN.objects.all()
    serializer_class = Sai_IN_Serializer
    # filterset_fields = ['PLMN_Carrier']
    search_fields = ['^PLMN_Carrier']
    # ordering_fields = ['create_at']
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ParameterwSaiSerializer)
    def parametresai(self, request, *args, **kwargs):

        serializer = FileSaiSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Sai_IN.objects.filter(Hva="")
        serializer_class = Sai_IN_Serializer
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
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
                Opcode=df["Opcode"][i], HVA=df["HVA"][i], EFF=df["Eff "][i],
                Total_Transactions=df["Total Transactions"][i], Failed_Transactions=df["Failed Transactions"][i],
            )
        else:
            sai: object = object(
                Interval_Time=df["Unnamed: 0"][i], PLMN_Carrier=df["Unnamed: 1"][i],
                Direction=df["Unnamed: 2"][i], Service=df["Unnamed: 3"][i],
                Opcode=df["Unnamed: 4"][i], HVA=df["Unnamed: 5"][i], EFF=df["Unnamed: 6"][i],
                Total_Transactions=df["Unnamed: 7"][i], Failed_Transactions=df["Unnamed: 8"][i],
            )
        i = i + 1
        liste.append(sai)

    data = object.objects.bulk_create(liste)

    return data
