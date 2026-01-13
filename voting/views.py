from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Election, Vote, Candidate
from core.models import Block
from core.blockchain import Blockchain
from .forms import ElectionForm, CandidateApplicationForm
import json

@login_required
def create_election(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            return redirect('admin_dashboard')
    else:
        form = ElectionForm()
        
    return render(request, 'voting/create_election.html', {'form': form})

@login_required
def apply_candidature(request):
    if request.user.role != 'candidate':
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CandidateApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('candidate_dashboard')
    else:
        form = CandidateApplicationForm()
    return render(request, 'voting/apply_candidature.html', {'form': form})

@login_required
def manage_elections(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
    
    elections = Election.objects.all().order_by('-start_date')
    pending_candidates = Candidate.objects.filter(is_approved=False)
    
    return render(request, 'voting/manage_elections.html', {
        'elections': elections,
        'pending_candidates': pending_candidates
    })

from .forms import AdminCandidateForm

@login_required
def admin_add_candidate(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AdminCandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.is_approved = True # Admin-created are auto-approved
            candidate.save()
            return redirect('manage_elections')
    else:
        form = AdminCandidateForm()
    
    return render(request, 'voting/admin_add_candidate.html', {'form': form})

@login_required
def end_election(request, election_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
    
    election = get_object_or_404(Election, id=election_id)
    election.is_active = False
    election.save()
    return redirect('manage_elections')

@login_required
def delete_election(request, election_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
    
    election = get_object_or_404(Election, id=election_id)
    election.delete()
    return redirect('manage_elections')

@login_required
def approve_candidate(request, candidate_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.is_approved = True
    candidate.save()
    # Link candidate to election properly? It's foreign key so it's linked.
    return redirect('manage_elections')

@login_required
def voter_dashboard(request):
    if request.user.role != 'voter':
        return redirect('dashboard')
    
    elections = Election.objects.filter(is_active=True).prefetch_related('candidates')
    # Filter elections where user hasn't voted
    voted_elections_ids = Vote.objects.filter(voter=request.user).values_list('election_id', flat=True)
    available_elections = elections.exclude(id__in=voted_elections_ids)
    
    # Vote History
    vote_history = Vote.objects.filter(voter=request.user).order_by('-timestamp')
    
    context = {
        'elections': available_elections, 
        'voted_elections': voted_elections_ids,
        'vote_history': vote_history
    }
    return render(request, 'voting/voter_dashboard.html', context)

@login_required
def candidate_dashboard(request):
    election_id = request.GET.get('election_id')
    
    # Context variables
    election = None
    candidate_profile = None
    vote_count = 0
    results = [] # List of {'candidate': obj, 'count': int}
    
    # 1. Determine Election
    if request.user.role == 'admin' or request.user.is_superuser:
        if election_id:
            election = get_object_or_404(Election, id=election_id)
        else:
            return redirect('manage_elections')
    elif request.user.role == 'candidate':
        try:
            candidate_profile = Candidate.objects.get(user=request.user)
            election = candidate_profile.election
        except Candidate.DoesNotExist:
            pass
    else:
        return redirect('dashboard')
        
    # 2. Calculate Results if Election exists
    if election:
        candidates = election.candidates.all()
        # Initialize counts
        counts = {c.id: 0 for c in candidates}
        
        # Parse Blockchain
        blocks = Block.objects.all()
        for b in blocks:
            try:
                if b.index == 0: continue # Skip genesis
                data = json.loads(b.data)
                
                # Check if this block belongs to this election
                if str(data.get('election_id')) == str(election.id):
                    c_id = int(data.get('candidate_id'))
                    if c_id in counts:
                        counts[c_id] += 1
            except Exception as e:
                # print(f"Error parsing block {b.index}: {e}")
                pass
        
        # Build Results List
        for cand in candidates:
            c_count = counts.get(cand.id, 0)
            results.append({
                'name': cand.user.username,
                'party': cand.party,
                'count': c_count
            })
            
            # If current user is this candidate, set their specific count
            if candidate_profile and cand.id == candidate_profile.id:
                vote_count = c_count
                
    context = {
        'election': election,
        'candidate': candidate_profile,
        'vote_count': vote_count, # Specific to logged in candidate
        'results': results, # All candidates
        'is_admin': (request.user.role == 'admin' or request.user.is_superuser)
    }
    return render(request, 'voting/candidate_dashboard.html', context)

@login_required
def cast_vote(request, election_id):
    if request.method != 'POST':
        return redirect('voter_dashboard')
        
    election = get_object_or_404(Election, id=election_id)
    candidate_id = request.POST.get('candidate')
    
    # Check eligibility
    if Vote.objects.filter(election=election, voter=request.user).exists():
        # Already voted
        return redirect('voter_dashboard')
        
    # Create Block
    # Data structure: election_id, candidate_id, voter_hash (anon)
    import hashlib
    voter_hash = hashlib.sha256(str(request.user.id).encode()).hexdigest()
    
    block_data = {
        'election_id': election.id,
        'candidate_id': int(candidate_id),
        'voter_hash': voter_hash
    }
    
    new_block = Blockchain.add_block(block_data)
    
    # Create Off-chain Record (to prevent double voting easily in UI)
    Vote.objects.create(
        election=election,
        voter=request.user,
        block_index=new_block.index
    )
    
    return render(request, 'voting/vote_success.html', {'block': new_block, 'election': election})

@login_required
def block_explorer(request):
    blocks = Block.objects.order_by('-index')
    return render(request, 'voting/block_explorer.html', {'blocks': blocks})
