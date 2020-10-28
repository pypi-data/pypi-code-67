# coding: utf8
# contract_gen 2020-06-15 10:07:47.572305

__all__ = ["ZcCurveDefinitionRequestItem"]

from ..instrument._definition import ObjectDefinition
from ..enum_types.main_constituent_asset_class import MainConstituentAssetClass
from ..enum_types.risk_type import RiskType


class ZcCurveDefinitionRequestItem(ObjectDefinition):

    def __init__(
            self,
            index_name=None,
            main_constituent_asset_class=None,
            risk_type=None,
            currency=None,
            curve_tag=None,
            id=None,
            name=None,
            source=None,
            valuation_date=None
    ):
        super().__init__()
        self.index_name = index_name
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.currency = currency
        self.curve_tag = curve_tag
        self.id = id
        self.name = name
        self.source = source
        self.valuation_date = valuation_date

    @property
    def main_constituent_asset_class(self):
        """
        :return: enum AssetClass
        """
        return self._get_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass")

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass", value)

    @property
    def risk_type(self):
        """
        :return: enum RiskType
        """
        return self._get_enum_parameter(RiskType, "riskType")

    @risk_type.setter
    def risk_type(self, value):
        self._set_enum_parameter(RiskType, "riskType", value)

    @property
    def currency(self):
        """
        :return: str
        """
        return self._get_parameter("currency")

    @currency.setter
    def currency(self, value):
        self._set_parameter("currency", value)

    @property
    def curve_tag(self):
        """
        User defined string to identify the curve. It can be used to link output results to the curve definition.
        Only alphabetic, numeric and '- _.#=@' characters are supported.
        Optional.
        :return: str
        """
        return self._get_parameter("curveTag")

    @curve_tag.setter
    def curve_tag(self, value):
        self._set_parameter("curveTag", value)

    @property
    def id(self):
        """
        Id of the curve definition to get
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)

    @property
    def index_name(self):
        """
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)

    @property
    def name(self):
        """
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def source(self):
        """
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)

    @property
    def valuation_date(self):
        """
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_parameter("valuationDate", value)

