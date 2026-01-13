@login_required
def block_explorer(request):
    # Public ledger view
    blocks = Block.objects.order_by('-index')
    return render(request, 'voting/block_explorer.html', {'blocks': blocks})
