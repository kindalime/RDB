from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity,
)
from django.db import models
from django.db.models.functions import Greatest


class LabManager(models.Manager):
    def search(self, search_text):
        search_vectors = (
            SearchVector('name', weight='A') 
            + SearchVector('project_desc', weight='B')
            + SearchVector('pi_name', weight='C')
            + SearchVector('email', weight='D')
        )

        search_query = SearchQuery(search_text)

        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = Greatest(
            TrigramSimilarity('name', search_text),
            TrigramSimilarity('project_desc', search_text),
            TrigramSimilarity('pi_name', search_text),
            TrigramSimilarity('email', search_text),
        )
        search_rank += trigram_similarity

        qs = (
            self.get_queryset()
            .filter(search_vector=search_query)
            .annotate(rank=search_rank)
            .order_by('-rank')
        )
        return qs