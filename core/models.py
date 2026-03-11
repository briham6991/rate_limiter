from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=10, unique=True)
    role = models.SmallIntegerField(default=2, db_comment="(1=superadmin, 2=admin, 3=readonly)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Custom User'    



class PlanInformation(models.Model): 
    plan_id = models.BigAutoField(primary_key=True)
    plan_name = models.CharField(max_length=100, unique=True)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2, db_comment="In Rupees")
    monthly_request_limit = models.BigIntegerField(default=100000)
    requests_per_minute = models.BigIntegerField(default=100)
    requests_per_hour = models.BigIntegerField(default=1000)
    requests_per_day = models.BigIntegerField(default=10000)
    plan_status = models.SmallIntegerField(default=2, db_comment="(1=active, 2=inactive, 3=paused)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plan_information'
        verbose_name = 'Plan Information'


class CompanyInformation(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=250)
    email_id = models.EmailField(unique=True) # check for argumrnt to put in EmailValidator
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    join_date = models.DateTimeField(null=True, blank=True)
    is_company_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_information'
        verbose_name = 'Company Information'


class KeyInformation(models.Model):
    key_id = models.BigAutoField(primary_key=True)
    key_value = models.CharField(max_length=64, unique=True) #TODO: generate this key value using some secure method
    company_id = models.ForeignKey(CompanyInformation, on_delete=models.PROTECT) #This ensures no two companies can have same keys
    plan_id = models.ForeignKey(PlanInformation, on_delete=models.PROTECT) 
    activation_time = models.DateTimeField(db_comment="provided by the issuer")
    valid_till = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT) #TODO:make this. this part is important
    last_used_at = models.DateTimeField(null=True)
    key_status = models.SmallIntegerField(default=2, db_comment="(1=active, 2=inactive, 3=paused)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'key_information'
        verbose_name = 'Key Information'


class KeyUtilizationInfo(models.Model):
    key_info_id = models.BigAutoField(primary_key=True)
    key_id = models.ForeignKey(KeyInformation, on_delete=models.PROTECT) #NOTE: Read about project than decide
    request_datetime = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    response_status = models.SmallIntegerField(db_comment="(1=success, 2=failure, 3=pending)")
    response_time_ms = models.BigIntegerField()

    class Meta:
        db_table = 'key_utilization_info'
        verbose_name = 'Key Utilization Information'











    


