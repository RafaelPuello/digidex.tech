from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from pygbif import species


class NameSuggestView(APIView):
    """
    View for the name_suggest API in pygbif.
    """
    def get(self, request):
        name = request.query_params.get('name')
        rank = request.query_params.get('rank')
        limit = int(request.query_params.get('limit', 10))

        if not name:
            raise ValidationError("The 'name' parameter is required for name_suggest.")

        try:
            results = species.name_suggest(q=name, rank=rank, limit=limit)
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class NameBackboneView(APIView):
    """
    View for the name_backbone API in pygbif.
    """
    def get(self, request):
        name = request.query_params.get('name')
        rank = request.query_params.get('rank')
        kingdom = request.query_params.get('kingdom')
        family = request.query_params.get('family')
        genus = request.query_params.get('genus')
        verbose = request.query_params.get('verbose', 'false') == 'true'
        limit = int(request.query_params.get('limit', 10))

        if not name:
            raise ValidationError("The 'name' parameter is required for name_backbone.")

        try:
            results = species.name_backbone(
                name=name,
                rank=rank,
                kingdom=kingdom,
                family=family,
                genus=genus,
                verbose=verbose,
                limit=limit
            )
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class NameLookupView(APIView):
    """
    View for the name_lookup API in pygbif.
    """
    def get(self, request):
        name = request.query_params.get('name')
        rank = request.query_params.get('rank')
        limit = int(request.query_params.get('limit', 10))

        if not name:
            raise ValidationError("The 'name' parameter is required for name_lookup.")

        try:
            results = species.name_lookup(q=name, rank=rank, limit=limit)
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class NameUsageView(APIView):
    """
    View for the name_usage API in pygbif.
    """
    def get(self, request):
        name = request.query_params.get('name')
        rank = request.query_params.get('rank')
        limit = int(request.query_params.get('limit', 10))

        if not name:
            raise ValidationError("The 'name' parameter is required for name_usage.")

        try:
            results = species.name_usage(name=name, rank=rank, limit=limit)
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
