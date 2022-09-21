from django.db import models


class Sponsor(models.Model):
    STATUS = (
        ('new', 'new'),
        ('approved', 'approved'),
        ('moderation', 'moderation'),
        ('canceled', 'canceled'),
    )
    Person_Type = (
        ('legal', 'legal'),
        ('physical', 'physical'),
    )
    Pay_Type = (
        ('cash', 'cash'),
        ('card', 'card'),
        ('salary', 'salary'),
    )
    
    person_type = models.CharField(max_length=100, choices=Person_Type)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True)
    sponsorship_money = models.PositiveIntegerField(null=True, blank=True)
    company = models.CharField(max_length=100,null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    pay_type = models.CharField(max_length=100, choices=Pay_Type, null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['id']
        verbose_name = "Homiy"
        verbose_name_plural = "Homiy"


class University(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Universitet"
        verbose_name_plural = "Universitet"


class Student(models.Model):
    Student_Type = (
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('Phd', 'Phd'),
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    student_type = models.CharField(max_length=100, choices=Student_Type, null=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='students')
    contract = models.PositiveBigIntegerField()
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['id']
        verbose_name = "Talaba"
        verbose_name_plural = "Talaba"


class Sponsorship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='sponsorships', null=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsorships')
    money = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['id']
        verbose_name = "Homiylik"
        verbose_name_plural = "Homiylik"
