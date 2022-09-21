from dataclasses import fields
from rest_framework import serializers
from config.models import Sponsor, Student, University, Sponsorship
from config.validators import validate_sponsorship_money_create, validate_sponsorship_money_update
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class SponsorSerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ('id', 'person_type', 'first_name', 'last_name',
                  'middle_name', 'phone_number', 'sponsorship_money',
                  'spent_money', 'company', 'status'
                  )
        
    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return spent_money

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'name')


class StudentSerializer(serializers.ModelSerializer):
    gained_money = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'student_type', 'first_name', 'last_name',
                  'middle_name', 'phone_number', 'university',
                  'contract', 'gained_money'
                  )
    
    @staticmethod
    def get_gained_money(student):
        gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return gained_money


class SponsorShipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    sponsor = SponsorSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    
    class Meta:
        model = Sponsorship
        fields = ('id', 'student_id', 'student', 'sponsor_id', 'sponsor', 'money')
    
    def create(self, validated_data):
        instance = validate_sponsorship_money_create(validated_data)
        return instance
    
    def update(self, instance, validated_data):
        instance = validate_sponsorship_money_update(instance, validated_data)
        return instance

        
class SendPetitionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sponsor
        fields = (
                  'person_type', 'first_name', 'last_name', 'middle_name',
                  'phone_number', 'company', 'status'
        )
        extra_kwargs = {
        'status': {
            'read_only': True
        }
    }
    def create(self, validated_data):
        validated_data['status'] = 'moderation'
        return super().create(validated_data) 
          
  
class AddStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_type', 'first_name', 'last_name',
                  'middle_name', 'phone_number', 'university',
                  'contract'
                  )
  

class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
                  'id', 'first_name', 'last_name',
                  'middle_name', 'phone_number',
                  'sponsorship_money', 'status',
                  'created_at'
                  )
 

