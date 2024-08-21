from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Data
from .serializer import DataSerializer

def index(request):
    return render(request, 'pages/home.html')

@api_view(['GET'])
def getData(request):
    app = Data.objects.all()
    serializer = DataSerializer(app, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getLastetData(request):
    records = Data.objects.all()
    data_len = len(records)
    res_data = [records[data_len-1]] # lastest data
    # print(res_data)
    serializer = DataSerializer(res_data, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def postData(request):
    print(request.data)
    serializer = DataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
