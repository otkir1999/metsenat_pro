from django.contrib import admin
from .models import Sponsor, Student, University, Sponsorship

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = (
                    'id', 'first_name', 'last_name', 'person_type',
                    'company', 'status', 'sponsorship_money',
                    'created_at'
                    
                   )
    list_editable = (
                    'first_name', 'last_name', 'person_type',
                    'company', 'status', 'sponsorship_money'
                    
    )
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = (
                    'id', 'first_name', 'last_name', 'student_type',
                    'university', 'contract', 'phone_number'
                    )


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = (
                    'id', 'name'
                   )


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = (
                    'id',
                    ) 