from django.shortcuts import render


def index_view(request):
    """
    Renders the community landing page with Discord integration.
    """
    return render(request, 'community/index.html')
