from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from goods.models import Products


def q_search(query):
    """
    Searches for a given query in the 'name' and 'description' fields of the Products model.

    Args:
        query (str): The query string to search for.

    Returns:
        QuerySet: A QuerySet containing all Products objects that match the query.
    """
    if not query:
        return Products.objects.all().order_by('id')  # Return all products

    vector = SearchVector('name', 'description')
    query_filter = SearchQuery(query)

    result = (
        Products.objects
        .filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        .annotate(rank=SearchRank(vector, query_filter))
        .filter(rank__gte=0)  # Lower the threshold to include results with lower relevance
        .order_by('-rank')
    )

    result = result.annotate(
        headline=SearchHeadline("name", query_filter, start_sel='<span style = "background-color: yellow">', stop_sel='</span>'),
        bodyline=SearchHeadline("description", query_filter, start_sel='<span style = "background-color: yellow">', stop_sel='</span>')
    )
    

    return result

    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()

    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)

    # return Products.objects.filter(q_objects)
