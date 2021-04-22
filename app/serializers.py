from rest_framework import serializers
from .models import Lab

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ('name', 'pi_name', 'department', 'work_remote', 
                  'work_in_person', 'accept_undergrads', 'accept_grads', 
                  'email', 'website', 'mentors', 'funded', 'project_desc', 
                  'created_date', 'modified_date', 'slug', 'likes')