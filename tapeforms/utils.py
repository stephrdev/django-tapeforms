from itertools import chain

from django.utils.functional import Promise


def is_safe(text):
    """Checks whether the string is safe."""
    if isinstance(text, Promise):
        text = str(text)
    return hasattr(text, '__html__')


def join_css_class(css_class, *additional_css_classes):
    """
    Returns the union of one or more CSS classes as a space-separated string.
    Note that the order will not be preserved.
    """
    css_set = set(chain.from_iterable(
        c.split(' ') for c in [css_class, *additional_css_classes] if c))
    return ' '.join(css_set)
