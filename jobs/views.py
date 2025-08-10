from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication
from .permissions import IsHirer, IsJobOwner
from .serializers import JobSerializer, JobApplicationSerializer
from django.conf import settings

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsHirer()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        job_type = self.request.query_params.get('job_type')
        if job_type in ['full_time', 'internship']:
            queryset = queryset.filter(job_type=job_type)
        return queryset

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsJobOwner]
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ApplyToJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

class MyApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

class JobApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)
        if job.posted_by != self.request.user:
            raise permissions.PermissionDenied("You do not own this job.")
        return JobApplication.objects.filter(job=job)
    
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobOwner]

class EmailApplicantsView(APIView):
    permission_classes = [IsHirer]

    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        if job.posted_by != request.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        subject = request.data.get("subject")
        message = request.data.get("message")
        applicant_ids = request.data.get("applicant_ids", [])

        if not subject or not message:
            return Response({"detail": "Subject and message required"}, status=status.HTTP_400_BAD_REQUEST)

        applications = JobApplication.objects.filter(job=job, id__in=applicant_ids)
        recipients = [app.applicant.email for app in applications if app.applicant.email]

        if not recipients:
            return Response({"detail": "No valid email addresses found"}, status=status.HTTP_400_BAD_REQUEST)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
        return Response({"detail": "Emails sent successfully"})
    
class MyJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsHirer]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class JobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsHirer]

    def get_queryset(self):
        job_id = self.kwargs['pk']
        job = get_object_or_404(Job, pk=job_id)

        if job.posted_by != self.request.user:
            raise PermissionDenied("You are not allowed to view applications for this job.")

        return JobApplication.objects.filter(job=job)   







