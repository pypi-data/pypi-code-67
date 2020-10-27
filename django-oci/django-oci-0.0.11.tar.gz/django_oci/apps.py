"""

Copyright (c) 2020, Vanessa Sochat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from django.apps import AppConfig


class DjangoOciConfig(AppConfig):
    name = "django_oci"
    verbose_name = "Opencontainer Distribution specification for Django"

    def ready(self):
        import django_oci.signals

        assert django_oci.signals
