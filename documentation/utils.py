# get attr
from operator import attrgetter


def sort_queryset(objects, order, is_reverse):
    """
    Returns an ordered array according to a sort order
    """
    return sorted(
        objects,
        key=lambda x: (
            attrgetter(order)(x).lower()
            if (
                type(attrgetter(order)(x)) == unicode
                or type(attrgetter(order)(x)) == str
            )
            else attrgetter(order)(x)
        ),
        reverse=is_reverse
    )


def order_queryset(objects, ordering):
    """
    Returns an ordered array by applying different order criteria
    """
    for order in ordering:
        is_reverse = order.startswith('-')
        order = order[1:] if is_reverse else order
        objects = sort_queryset(objects, order, is_reverse)
    return objects
