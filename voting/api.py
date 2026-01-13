from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Election, Candidate
from core.models import Block
import json

@login_required
def election_data_api(request, election_id):
    # Returns vote counts for a specific election based on BLOCKCHAIN data
    try:
        election = Election.objects.get(id=election_id)
        candidates = Candidate.objects.filter(election=election)
        
        # Initialize counts
        counts = {c.id: 0 for c in candidates}
        candidate_names = {c.id: c.party for c in candidates} # Label by Party
        
        # Scan Blockchain (Simulation of reading ledger)
        # In a very large chain, this would be indexed off-chain.
        blocks = Block.objects.all()
        for block in blocks:
            try:
                data = json.loads(block.data)
                # Check if block data belongs to this election
                if str(data.get('election_id')) == str(election_id):
                    c_id = int(data.get('candidate_id'))
                    if c_id in counts:
                        counts[c_id] += 1
            except:
                continue
                
        # Format for Chart.js
        labels = [candidate_names[cid] for cid in counts.keys()]
        data = [counts[cid] for cid in counts.keys()]
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'title': election.title
        })
        
    except Election.DoesNotExist:
        return JsonResponse({'error': 'Election not found'}, status=404)
