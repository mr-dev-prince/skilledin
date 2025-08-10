from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    posted_by_username = serializers.ReadOnlyField(source='posted_by.username')
    has_applied = serializers.SerializerMethodField()
    applicant_count = serializers.IntegerField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'description', 
            'tech_stack', 'link', 'created_at', 'posted_by_username', 'poster', 'has_applied', 'applicant_count', 'job_type'
        ]

    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.applications.filter(applicant=request.user).exists()
        return False

    def get_applicant_count(self, obj):
        return obj.applications.count()

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.ReadOnlyField(source='applicant.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_title', 'applicant_username', 'cover_letter', 'status', 'applied_at']
        read_only_fields = ['status', 'applicant_username', 'job_title', 'applied_at']
