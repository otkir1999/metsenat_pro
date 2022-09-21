from rest_framework.validators import ValidationError
from rest_framework.generics import get_object_or_404
from .models import Student, Sponsor, Sponsorship
from django.db.models import Sum
from django.db.models.functions import Coalesce




def validate_sponsorship_money_create(validated_data):
    sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))
    student = get_object_or_404(Student, id=validated_data.get('student_id'))
    money = validated_data.get('money')

    sponsor_spent_money = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
    student_gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
    sponsor_left_money = sponsor.sponsorship_money - sponsor_spent_money
    
    if money <= sponsor_left_money:
        if student_gained_money + money <= student.contract:
            sponsorship = Sponsorship.objects.create(**validated_data)
            return sponsorship
        else:
            raise ValidationError({'msg': 'Sponsorship money has exceeded the contract amount!'})
    else:
        raise ValidationError({'msg': 'Sponsor has not this money!'})



def validate_sponsorship_money_update(instance, validated_data):
    sponsor = get_object_or_404(Sponsor, id=validated_data['sponsor_id'])
    student = instance.student
    money = validated_data['money']

    sponsor_spent_money = \
        sponsor.sponsorships.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
    student_gained_money = \
        student.sponsorships.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
    sponsor_left_money = sponsor.sponsorship_money - sponsor_spent_money

    if money <= sponsor_left_money:
        if student_gained_money + money <= student.contract:
            instance.money = money
            instance.sponsor = sponsor
            instance.save()
            return instance
        else:
            raise ValidationError({'msg': 'Sponsorship money has exceeded the contract amount!'})
    else:
        raise ValidationError({'msg': 'Sponsor has not this money!'})


