from typing import Optional

from spark_auto_mapper_fhir.backbone_elements.fhir_backbone_element_base import FhirBackboneElementBase
from spark_auto_mapper_fhir.fhir_types.boolean import FhirBoolean
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.time import FhirTime
from spark_auto_mapper_fhir.valuesets.days_of_week import DaysOfWeek


class PractitionerAvailableTimeBackboneElement(FhirBackboneElementBase):
    # noinspection PyPep8Naming
    def __init__(
        self,
        daysOfWeek: Optional[FhirList[DaysOfWeek]] = None,
        allDay: Optional[FhirBoolean] = None,
        availableStartTime: Optional[FhirTime] = None,
        availableEndTime: Optional[FhirTime] = None
    ) -> None:
        """
        PractitionerAvailableTimeBackboneElement Backbone Element in FHIR
        https://hl7.org/FHIR/practitionerrole-definitions.html#PractitionerRole.availableTime
        Times the Service Site is available


        :param daysOfWeek: mon | tue | wed | thu | fri | sat | sun
        :param allDay: Always available? e.g. 24 hour service
        :param availableStartTime: Opening time of day (ignored if allDay = true)
        :param availableEndTime: Closing time of day (ignored if allDay = true)
        """
        super().__init__(
            daysOfWeek=daysOfWeek,
            allDay=allDay,
            availableStartTime=availableStartTime,
            availableEndTime=availableEndTime
        )
