from django.urls import path
from .views import (
    JobListCreateView, JobDetailView, ApplyToJobView, MyApplicationsView, 
    JobApplicationsListView, ApplicationStatusUpdateView, EmailApplicantsView, 
    MyJobsView, JobApplicationsView
)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('applications/<int:pk>/update-status/', ApplicationStatusUpdateView.as_view(), name='application-update-status'),
    path('jobs/<uuid:pk>/email-applicants/', EmailApplicantsView.as_view(), name='email-applicants'),
    path('my-jobs/', MyJobsView.as_view(), name='my-jobs'),
    path('<uuid:pk>/applications/', JobApplicationsView.as_view(), name='job-applications'),
    path('<uuid:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('apply/', ApplyToJobView.as_view(), name='apply-to-job'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('<uuid:job_id>/applications/', JobApplicationsListView.as_view(), name='job-applications'),
]
