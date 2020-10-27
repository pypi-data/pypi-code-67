# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GroupPlaceGroupResponse(Model):
    """GroupPlaceGroupResponse.

    :param place_group_id: The place group identifier
    :type place_group_id: int
    :param place_group_code: The place group code
    :type place_group_code: str
    :param place_group_info: The place group info
    :type place_group_info: str
    :param auto_group: Indicates if this place group is an autogroup
    :type auto_group: bool
    :param member_count: The number of places in this group
    :type member_count: int
    :param member_count_with_topmost: The number of places within the
     currently authenticated user's topmost
    :type member_count_with_topmost: int
    :param place_group_category:
    :type place_group_category: ~energycap.sdk.models.PlaceGroupCategoryChild
    :param limit_members_by_topmost: Indicates if the place group has been set
     limit the list of members by the user's topmost
    :type limit_members_by_topmost: bool
    :param user_defined_auto_group: Indicates if this place group is an user
     defined auto group
    :type user_defined_auto_group: bool
    :param user_defined_auto_group_filters: The filters applied to determine
     the members of a user defined auto group
    :type user_defined_auto_group_filters:
     list[~energycap.sdk.models.FilterResponse]
    :param last_updated: The last time a member was inserted, updated, or
     deleted from the group
    :type last_updated: datetime
    """

    _attribute_map = {
        'place_group_id': {'key': 'placeGroupId', 'type': 'int'},
        'place_group_code': {'key': 'placeGroupCode', 'type': 'str'},
        'place_group_info': {'key': 'placeGroupInfo', 'type': 'str'},
        'auto_group': {'key': 'autoGroup', 'type': 'bool'},
        'member_count': {'key': 'memberCount', 'type': 'int'},
        'member_count_with_topmost': {'key': 'memberCountWithTopmost', 'type': 'int'},
        'place_group_category': {'key': 'placeGroupCategory', 'type': 'PlaceGroupCategoryChild'},
        'limit_members_by_topmost': {'key': 'limitMembersByTopmost', 'type': 'bool'},
        'user_defined_auto_group': {'key': 'userDefinedAutoGroup', 'type': 'bool'},
        'user_defined_auto_group_filters': {'key': 'userDefinedAutoGroupFilters', 'type': '[FilterResponse]'},
        'last_updated': {'key': 'lastUpdated', 'type': 'iso-8601'},
    }

    def __init__(self, place_group_id=None, place_group_code=None, place_group_info=None, auto_group=None, member_count=None, member_count_with_topmost=None, place_group_category=None, limit_members_by_topmost=None, user_defined_auto_group=None, user_defined_auto_group_filters=None, last_updated=None):
        super(GroupPlaceGroupResponse, self).__init__()
        self.place_group_id = place_group_id
        self.place_group_code = place_group_code
        self.place_group_info = place_group_info
        self.auto_group = auto_group
        self.member_count = member_count
        self.member_count_with_topmost = member_count_with_topmost
        self.place_group_category = place_group_category
        self.limit_members_by_topmost = limit_members_by_topmost
        self.user_defined_auto_group = user_defined_auto_group
        self.user_defined_auto_group_filters = user_defined_auto_group_filters
        self.last_updated = last_updated
