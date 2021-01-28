from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity,
)
from django.db import models


class LabManager(models.Manager):
    def search(self, search_text):
        search_vectors = (
            SearchVector(
                'project_desc', weight='A'
            )
        ) 
        search_query = SearchQuery(
            search_text
        )
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity(
            'project_desc', search_text
        )
        qs = (
            self.get_queryset()
            .filter(search_vector=search_query)
            .annotate(rank=search_rank + trigram_similarity)
            .order_by('-rank')
        )
        return qs