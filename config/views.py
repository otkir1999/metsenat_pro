from config.models import Sponsor, Sponsorship, University, Student
from config.paginations import CustomPagination
from config.serializers import (
                                AddStudentSerializer, SendPetitionSerializer,
                                SponsorListSerializer, SponsorSerializer, 
                                SponsorShipSerializer, UniversitySerializer,
                                StudentSerializer
                                ) 

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, filters
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import datetime
from datetime import datetime, timezone, date
import pytz
import pandas as pd
from django.conf import settings
from django.db.models import Sum
from collections import Counter


class SendPetitionView(APIView):
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(request_body=SendPetitionSerializer)
    def post(self, request):
        serializer = SendPetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Ma'lumotlar tekshirish uchun yuborildi."
            },
             status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [AllowAny]


class AddStudentView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    @swagger_auto_schema(request_body=AddStudentSerializer)
    def post(self, request, format=None):
        serializer = AddStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentFilterByStudentTypeView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get(self, request, student_type):
        students = Student.objects.filter(student_type=student_type)
        serializer = StudentSerializer(students, many=True)
        return Response (serializer.data)


class StudentFilterByUniversityView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get(self, request, pk):
        students = self.queryset.filter(university=pk)
        serializer = StudentSerializer(students, many=True) 
        return Response(serializer.data)
    

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]


class SponsorView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'first_name']


class SponsorFilterByStatusAndMoneyView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'first_name']
    
    def get(self, request, status, sponsorship_money):
        sponsors = Sponsor.objects.filter(status=status, sponsorship_money=sponsorship_money)
        serializer = SponsorListSerializer(sponsors, many=True) 
        return Response(serializer.data)


class SponsorFilterByStatusView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'first_name']
    
    def get(self, request, status):
        sponsors = Sponsor.objects.filter(status=status)
        serializer = SponsorListSerializer(sponsors, many=True) 
        return Response(serializer.data)


class SponsorFilterByMoneyView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'first_name']
    
    def get(self, request, sponsorship_money):
        sponsors = Sponsor.objects.filter(sponsorship_money=sponsorship_money)
        serializer = SponsorListSerializer(sponsors, many=True) 
        return Response(serializer.data)


class SponsorFilterByDateView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'first_name']
    
    def get(self, request, from_date, to_date):
        try:
            sponsors = Sponsor.objects.filter(created_at__gte=from_date, created_at__lte=to_date)
            print(sponsors)
            serializer = SponsorListSerializer(sponsors, many=True) 
            return Response(serializer.data)
        except Exception as e :
            return Response("Format xato kiritildi.")


class DashboardView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=["Statistics"])
    def get(self, request):
        all_expenses = Sponsor.objects.all().aggregate(expenses=Sum('spent_money'))
        required_pay = Student.objects.all().aggregate(expenses=Sum('contract'))
        amount_pay = Counter(required_pay) - Counter(all_expenses)

        month_map = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = {
                'vaqt': month_map,
                        
                 'homiylar_soni': [
                     Sponsor.objects.filter(
                                            created_at__month__gte=i,
                                            created_at__month__lt=i+1
                                                    ).count() for i in range(12) 
                                   ],
                'talabalar_soni': [
                     Student.objects.filter(
                                            created_at__month__gte=i,
                                            created_at__month__lt=i+1
                                                    ).count() for i in range(12) 
                                   ]}
          
        df = pd.DataFrame(data)
        with pd.ExcelWriter("statistics.xlsx") as writer:
            df.to_excel(writer, index=False)
        return Response({
            "statistika": df,
            'jami tolangan summa': all_expenses,
            'jami soralgan summa': required_pay,
            'tolanishi kerak summa': amount_pay   
        })    


class SponsorshipView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorShipSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sponsor__first_name', 'sponsor__last_name', 'student__first_name', 'student__first_name']
    

class SponsorShipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorShipSerializer
