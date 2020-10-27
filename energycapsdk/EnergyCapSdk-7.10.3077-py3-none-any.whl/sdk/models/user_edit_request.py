# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UserEditRequest(Model):
    """UserEditRequest.

    :param user_code: The user code. This is the user name that is used on
     sign-in <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type user_code: str
    :param full_name: The user's full name <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type full_name: str
    :param password: The user's password. Password is not changed if this
     field is empty.
     Not available for users whose identity is managed externally. <span
     class='property-internal'>Must be between 0 and 128 characters</span>
     <span class='property-internal'>Required (defined)</span>
    :type password: str
    :param email: The user's email address <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 128 characters</span>
    :type email: str
    :param cost_center_id: NOTE: This property will be deprecated
     Use TopmostCostCenterIds with a single valued list to update a user to a
     single topmost cost center
     Update a user to a single topmost cost center id
     The CostCenterId must be in the editing user's topmost
     If this value is not null then TopmostCostCenterIds must be null <span
     class='property-internal'>Topmost (CostCenter)</span> <span
     class='property-internal'>Required (defined)</span>
    :type cost_center_id: int
    :param topmost_cost_center_ids: Update a user to one multiple topmost cost
     center ids
     The CostCenterIds must be in the editing user's topmost
     If this is not null then CostCenterId must be null <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type topmost_cost_center_ids: list[int]
    :param place_id: NOTE: This property will be deprecated
     Use TopmostPlaceIds with a single valued list to update a user to a single
     topmost place
     Update a user to a single topmost place id
     The PlaceId must be in the editing user's topmost
     If this value is not null then TopmostPlaceIds must be null <span
     class='property-internal'>Topmost (Place)</span> <span
     class='property-internal'>Required (defined)</span>
    :type place_id: int
    :param topmost_place_ids: Update a user to one or multiple topmost place
     ids
     The PlaceIds must be in the editing user's topmost
     If this is not null then PlaceId must be null <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type topmost_place_ids: list[int]
    :param active_directory: Whether or not the user signs in using active
     directory. This is used for install client only <span
     class='property-internal'>Required</span>
    :type active_directory: bool
    :param active: Whether or not the user is active <span
     class='property-internal'>Required</span>
    :type active: bool
    :param password_expiration_interval: Days until the user's password
     expires
     Must be set to 0 for users whose identity is managed externally. <span
     class='property-internal'>Required</span>
    :type password_expiration_interval: int
    :param strong_password: Force the user's password to have a minimum of 8
     characters,
     containing at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol.
     Must be set to false for users whose identity is managed externally. <span
     class='property-internal'>Required</span>
    :type strong_password: bool
    :param force_password_change: Force the user to change their password on
     next login.
     Must be set to false for users whose identity is managed externally. <span
     class='property-internal'>Required</span>
    :type force_password_change: bool
    :param user_role_id: The user's role <span
     class='property-internal'>Required</span>
    :type user_role_id: int
    :param max_approval_amount: The maximum bill amount (in dollars) the user
     can approve
     If not included, the user has no max limit <span
     class='property-internal'>Required (defined)</span>
    :type max_approval_amount: int
    :param report_group_id: The user's report group. If not included, set to
     the default report group <span class='property-internal'>Required</span>
    :type report_group_id: int
    :param user_groups: List of user group ids
     If null or not passed the groups a user assigned to will NOT be modified
     If an empty list the user will be removed from all groups <span
     class='property-internal'>Required (defined)</span>
    :type user_groups: list[int]
    """

    _validation = {
        'user_code': {'required': True, 'max_length': 32, 'min_length': 0},
        'full_name': {'required': True, 'max_length': 32, 'min_length': 0},
        'password': {'max_length': 128, 'min_length': 0},
        'email': {'required': True, 'max_length': 128, 'min_length': 0},
        'active_directory': {'required': True},
        'active': {'required': True},
        'password_expiration_interval': {'required': True},
        'strong_password': {'required': True},
        'force_password_change': {'required': True},
        'user_role_id': {'required': True},
        'report_group_id': {'required': True},
    }

    _attribute_map = {
        'user_code': {'key': 'userCode', 'type': 'str'},
        'full_name': {'key': 'fullName', 'type': 'str'},
        'password': {'key': 'password', 'type': 'str'},
        'email': {'key': 'email', 'type': 'str'},
        'cost_center_id': {'key': 'costCenterId', 'type': 'int'},
        'topmost_cost_center_ids': {'key': 'topmostCostCenterIds', 'type': '[int]'},
        'place_id': {'key': 'placeId', 'type': 'int'},
        'topmost_place_ids': {'key': 'topmostPlaceIds', 'type': '[int]'},
        'active_directory': {'key': 'activeDirectory', 'type': 'bool'},
        'active': {'key': 'active', 'type': 'bool'},
        'password_expiration_interval': {'key': 'passwordExpirationInterval', 'type': 'int'},
        'strong_password': {'key': 'strongPassword', 'type': 'bool'},
        'force_password_change': {'key': 'forcePasswordChange', 'type': 'bool'},
        'user_role_id': {'key': 'userRoleId', 'type': 'int'},
        'max_approval_amount': {'key': 'maxApprovalAmount', 'type': 'int'},
        'report_group_id': {'key': 'reportGroupId', 'type': 'int'},
        'user_groups': {'key': 'userGroups', 'type': '[int]'},
    }

    def __init__(self, user_code, full_name, email, active_directory, active, password_expiration_interval, strong_password, force_password_change, user_role_id, report_group_id, password=None, cost_center_id=None, topmost_cost_center_ids=None, place_id=None, topmost_place_ids=None, max_approval_amount=None, user_groups=None):
        super(UserEditRequest, self).__init__()
        self.user_code = user_code
        self.full_name = full_name
        self.password = password
        self.email = email
        self.cost_center_id = cost_center_id
        self.topmost_cost_center_ids = topmost_cost_center_ids
        self.place_id = place_id
        self.topmost_place_ids = topmost_place_ids
        self.active_directory = active_directory
        self.active = active
        self.password_expiration_interval = password_expiration_interval
        self.strong_password = strong_password
        self.force_password_change = force_password_change
        self.user_role_id = user_role_id
        self.max_approval_amount = max_approval_amount
        self.report_group_id = report_group_id
        self.user_groups = user_groups
