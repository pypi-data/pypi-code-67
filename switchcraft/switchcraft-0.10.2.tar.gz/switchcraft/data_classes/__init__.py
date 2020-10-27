"""Data Classes for common AWS events."""

from switchcraft.data_classes.config_event import ConfigEvent

# Overriding '__all__' to ensure that public access to classes are controlled.
__all__ = [
    ConfigEvent
]
