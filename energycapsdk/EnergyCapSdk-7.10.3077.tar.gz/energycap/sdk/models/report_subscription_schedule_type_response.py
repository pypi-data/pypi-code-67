# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReportSubscriptionScheduleTypeResponse(Model):
    """ReportSubscriptionScheduleTypeResponse.

    :param report_subscription_schedule_type_id: The identifier of the
     schedule type
    :type report_subscription_schedule_type_id: int
    :param report_subscription_schedule_type_name: The name of the schedule
     type
    :type report_subscription_schedule_type_name: str
    :param day_indicators: Available day indicators for this schedule type
    :type day_indicators:
     list[~energycap.sdk.models.ReportSubscriptionDayIndicatorChild]
    """

    _attribute_map = {
        'report_subscription_schedule_type_id': {'key': 'reportSubscriptionScheduleTypeId', 'type': 'int'},
        'report_subscription_schedule_type_name': {'key': 'reportSubscriptionScheduleTypeName', 'type': 'str'},
        'day_indicators': {'key': 'dayIndicators', 'type': '[ReportSubscriptionDayIndicatorChild]'},
    }

    def __init__(self, report_subscription_schedule_type_id=None, report_subscription_schedule_type_name=None, day_indicators=None):
        super(ReportSubscriptionScheduleTypeResponse, self).__init__()
        self.report_subscription_schedule_type_id = report_subscription_schedule_type_id
        self.report_subscription_schedule_type_name = report_subscription_schedule_type_name
        self.day_indicators = day_indicators
