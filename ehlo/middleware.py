class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default language is French
        lang = request.session.get('django_language', 'fr')
        request.lang = lang
        response = self.get_response(request)
        return response
