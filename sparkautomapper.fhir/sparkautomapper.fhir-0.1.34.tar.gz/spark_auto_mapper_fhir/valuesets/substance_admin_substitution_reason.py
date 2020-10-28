from typing import Callable, Type, Any

from spark_auto_mapper_fhir.valuesets.FhirValueSetBase import FhirValueSetBase
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType

from spark_auto_mapper_fhir.classproperty import genericclassproperty
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri


# noinspection PyMethodParameters
# noinspection PyPep8Naming
class SubstanceAdminSubstitutionReason(FhirValueSetBase):
    """
    https://hl7.org/FHIR/v3/SubstanceAdminSubstitutionReason/vs.html
    """
    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    # noinspection PyPep8Naming,SpellCheckingInspection
    class classproperty(object):
        def __init__(
            self, f: Callable[..., 'SubstanceAdminSubstitutionReason']
        ) -> None:
            self.f: Callable[..., 'SubstanceAdminSubstitutionReason'] = f

        def __get__(
            self, obj: Any, owner: Type['SubstanceAdminSubstitutionReason']
        ) -> 'SubstanceAdminSubstitutionReason':
            return self.f(owner)

    @classproperty
    def NameOfYourFirstValue(cls) -> 'SubstanceAdminSubstitutionReason':
        """
        Comment
        """
        # noinspection PyCallingNonCallable
        return SubstanceAdminSubstitutionReason("A")

    @genericclassproperty
    def codeset(cls) -> FhirUri:
        return "http://terminology.hl7.org/CodeSystem/v3-ActReason"
