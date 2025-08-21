from typing import Protocol, TYPE_CHECKING

from lib.utils import DotDict, Point


if TYPE_CHECKING:
    from lib.sew_stack import SewStack


class LayerProtocol(Protocol):
    paths: 'list[list[Point]]'
    config: DotDict
    element: 'SewStack'


def with_protocol(protocol):
    """Include a protocol in a Mixin only for type hinting.

    Normally we'd use a protocol in a mixin to indicate that we
    expect certain attributes to be available on self, as
    described here:

    https://mypy.readthedocs.io/en/stable/more_types.html#mixin-classes

    However, for some reason type-checkers then _only_ allow use of
    properties on self that are defined in the protocol.  For example,
    this doesn't work:

    class MyMixin:
        def foo(self):
            return "hi"

        def bar(self: LayerProtocol):
            thing = self.foo()
            if self.config.baz == thing:
                ...

    This fails because mypy says that "self.foo()" references unknown
    attribute "foo"... even though it's defined right there in MyMixin.
    This feels a little weird, but that's how it works.

    Instead, we do it like this:

    class MyMixin(with_protocol(LayerProtocol)):
        ...
    """
    if TYPE_CHECKING:
        return protocol
    else:
        return object
