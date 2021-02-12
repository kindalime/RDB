from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity,
)
from django.db import models
from django.db.models.functions import Greatest
from psycopg2.extensions import adapt


class LabManager(models.Manager):
    def search(self, search_text):
        search_vectors = (
            SearchVector('name', weight='A') 
            + SearchVector('project_desc', weight='B')
            + SearchVector('pi_name', weight='C')
            + SearchVector('email', weight='D')
        )

        search_query = BetterSearchQuery(search_text, search_type='raw')

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

class BetterSearchQuery(SearchQuery):
    """
    Alter the tsquery executed by SearchQuery
    """
    def as_sql(self, compiler, connection):
        # Or <-> available in Postgres 9.6
        print(self.source_expressions)
        value = adapt('%s:*' % ' & '.join(self.source_expressions[0].value.split()))

        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = 'to_tsquery({}::regconfig, {})'\
                .format(config_sql, value)
            params = config_params
        else:
            template = 'to_tsquery({})'\
                .format(value)
            params = []

        if self.invert:
            template = '!!({})'.format(template)

        return template, params