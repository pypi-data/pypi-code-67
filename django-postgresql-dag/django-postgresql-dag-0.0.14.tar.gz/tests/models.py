from django.db import models
from django_postgresql_dag.models import node_factory, edge_factory

class NetworkEdge(edge_factory("NetworkNode", concrete=False)):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = f"{self.parent.name} {self.child.name}"
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'tests'


class NetworkNode(node_factory(NetworkEdge)):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tests'
