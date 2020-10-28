import asyncio
from typing import (
    Mapping,
    Dict,
    Callable,
    Any,
    Coroutine,
    Optional,
    Iterator,
    List,
    Union,
)

from anyio import create_task_group

from mypy_extensions import TypedDict


EventsMapping = Union[Dict[str, Union["Callable[..., Any]", "EventHandler"]], "Events"]


class EventTarget(TypedDict):
    target: str
    preventDefault: bool  # noqa
    stopPropagation: bool  # noqa


def event(
    function: Optional[Callable[..., Any]] = None,
    stop_propagation: bool = False,
    prevent_default: bool = False,
    target_id: Optional[str] = None,
) -> Union["EventHandler", Callable[[Callable[..., Any]], "EventHandler"]]:
    """Create an event handler function with extra functionality.

    You're always free to add callbacks by assigning them to element callbacks.

    .. code-block:: python

        element = idom.html.button(onClick=my_callback)

    However you may want the ability to prevent the default action associated
    with the event from taking place, or stoping the event from propagating up
    the DOM. This decorator allows you to add that functionality to your callbacks.

    Parameters:
        function:
            A coroutine of the form ``async handler(event)`` where ``event`` is
            a dictionary of event data.
        stop_propagation:
            Block the event from propagating further up the DOM.
        prevent_default:
            Stops the default actional associate with the event from taking place.
        target_id:
            Sets the ID used to identify this handler in the resulting VDOM which
            is usually just automatically generated. This parameter is used when
            testing.
    """
    handler = EventHandler(stop_propagation, prevent_default, target_id=target_id)
    if function is not None:
        handler.add(function)
        return handler
    else:
        return handler.add


class Events(Mapping[str, "EventHandler"]):
    """A container for event handlers.

    Assign this object to the ``"eventHandlers"`` field of an element model.
    """

    __slots__ = "_handlers"

    def __init__(self) -> None:
        self._handlers: Dict[str, EventHandler] = {}

    def on(
        self, event: str, stop_propagation: bool = False, prevent_default: bool = False
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """A decorator for adding an event handler.

        Parameters:
            event:
                The camel-case name of the event, the word "on" is automatically
                prepended. So passing "keyDown" would refer to the event "onKeyDown".
            stop_propagation:
                Block the event from propagating further up the DOM.
            prevent_default:
                Stops the default actional associate with the event from taking place.

        Returns:
            A decorator which accepts an event handler function as its first argument.
            The parameters of the event handler function may indicate event attributes
            which should be sent back from the frontend. See :class:`EventHandler` for
            more info.

        Examples:
            Simple "onClick" event handler:

            .. code-block:: python
                def clickable_element():
                    events = Events()

                    @events.on("click")
                    def handler(event):
                        # do something on a click event
                        ...

                    return idom.vdom("button", "hello!", eventHandlers=events)
        """
        if not event.startswith("on"):
            event = "on" + event[:1].upper() + event[1:]

        if event not in self._handlers:
            handler = EventHandler(stop_propagation, prevent_default)
            self._handlers[event] = handler
        else:
            handler = self._handlers[event]

        def setup(function: Callable[..., Any]) -> Callable[..., Any]:
            handler.add(function)
            return function

        return setup

    def __contains__(self, key: Any) -> bool:
        return key in self._handlers

    def __len__(self) -> int:
        return len(self._handlers)

    def __iter__(self) -> Iterator[str]:
        return iter(self._handlers)

    def __getitem__(self, key: str) -> "EventHandler":
        return self._handlers[key]

    def __repr__(self) -> str:  # pragma: no cover
        return repr(self._handlers)


class EventHandler:
    """An object which defines an event handler.

    Get a serialized reference to the handler via :meth:`Handler.serialize`.

    The event handler object acts like a coroutine when called.

    Parameters:
        event_name:
            The camel case name of the event.
        target_id:
            A unique identifier for the event handler. This is generally used if
            an element has more than on event handler for the same event type. If
            no ID is provided one will be generated automatically.
    """

    __slots__ = (
        "__weakref__",
        "_coro_handlers",
        "_func_handlers",
        "_target_id",
        "_prevent_default",
        "_stop_propogation",
    )

    def __init__(
        self,
        stop_propagation: bool = False,
        prevent_default: bool = False,
        target_id: Optional[str] = None,
    ) -> None:
        self._coro_handlers: List[Callable[..., Coroutine[Any, Any, Any]]] = []
        self._func_handlers: List[Callable[..., Any]] = []
        self._target_id = target_id or str(id(self))
        self._stop_propogation = stop_propagation
        self._prevent_default = prevent_default

    @property
    def id(self) -> str:
        """ID of the event handler."""
        return self._target_id

    def add(self, function: Callable[..., Any]) -> "EventHandler":
        """Add a callback to the event handler.

        Parameters:
            function:
                The event handler function. Its parameters may indicate event attributes
                which should be sent back from the fronend unless otherwise specified by
                the ``properties`` parameter.
        """
        if asyncio.iscoroutinefunction(function):
            self._coro_handlers.append(function)
        else:
            self._func_handlers.append(function)
        return self

    def remove(self, function: Callable[..., Any]) -> None:
        """Remove the function from the event handler.

        Raises:
            ValueError: if not found
        """
        if asyncio.iscoroutinefunction(function):
            self._coro_handlers.remove(function)
        else:
            self._func_handlers.remove(function)

    def serialize(self) -> EventTarget:
        """Serialize the event handler."""
        return {
            "target": self._target_id,
            "preventDefault": self._prevent_default,
            "stopPropagation": self._stop_propogation,
        }

    async def __call__(self, data: List[Any]) -> Any:
        """Trigger all callbacks in the event handler."""
        if self._coro_handlers:
            async with create_task_group() as group:
                for handler in self._coro_handlers:
                    await group.spawn(handler, *data)
        for handler in self._func_handlers:
            handler(*data)

    def __contains__(self, function: Any) -> bool:
        if asyncio.iscoroutinefunction(function):
            return function in self._coro_handlers
        else:
            return function in self._func_handlers

    def __repr__(self) -> str:  # pragma: no cover
        return f"{type(self).__name__}({self.serialize()})"
