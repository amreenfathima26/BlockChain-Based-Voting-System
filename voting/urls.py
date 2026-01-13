from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('voter-dashboard/', views.voter_dashboard, name='voter_dashboard'),
    path('candidate-dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('vote/<int:election_id>/', views.cast_vote, name='cast_vote'),
    path('create-election/', views.create_election, name='create_election'),
    path('apply-candidature/', views.apply_candidature, name='apply_candidature'),
    path('manage-elections/', views.manage_elections, name='manage_elections'),
    path('end-election/<int:election_id>/', views.end_election, name='end_election'),
    path('approve-candidate/<int:candidate_id>/', views.approve_candidate, name='approve_candidate'),
    path('api/data/<int:election_id>/', api.election_data_api, name='election_data_api'),
    path('api/data/<int:election_id>/', api.election_data_api, name='election_data_api'),
    path('ledger/', views.block_explorer, name='block_explorer'),
    path('admin-add-candidate/', views.admin_add_candidate, name='admin_add_candidate'),
]
