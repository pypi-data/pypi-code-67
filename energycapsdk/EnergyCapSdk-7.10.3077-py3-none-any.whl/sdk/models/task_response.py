# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TaskResponse(Model):
    """TaskResponse.

    :param has_attachments:
    :type has_attachments: bool
    :param task_id:
    :type task_id: int
    :param task_gu_id: The task guid
    :type task_gu_id: str
    :param task_type:
    :type task_type: ~energycap.sdk.models.TaskType
    :param begin_date: The date and time the task began
    :type begin_date: datetime
    :param end_date: The date and time the task finished. If the task is not
     finished, endDate will have no value
    :type end_date: datetime
    :param user:
    :type user: ~energycap.sdk.models.UserChild
    :param message: The task's message
    :type message: str
    :param output: The task's output. For certain task types, this field could
     be sizeable
    :type output: object
    :param settings: The task's settings
    :type settings: object
    :param status: The task's status
    :type status: str
    :param task_note: User provided note/comment for this Task
    :type task_note: str
    """

    _attribute_map = {
        'has_attachments': {'key': 'hasAttachments', 'type': 'bool'},
        'task_id': {'key': 'taskId', 'type': 'int'},
        'task_gu_id': {'key': 'taskGUId', 'type': 'str'},
        'task_type': {'key': 'taskType', 'type': 'TaskType'},
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'user': {'key': 'user', 'type': 'UserChild'},
        'message': {'key': 'message', 'type': 'str'},
        'output': {'key': 'output', 'type': 'object'},
        'settings': {'key': 'settings', 'type': 'object'},
        'status': {'key': 'status', 'type': 'str'},
        'task_note': {'key': 'taskNote', 'type': 'str'},
    }

    def __init__(self, has_attachments=None, task_id=None, task_gu_id=None, task_type=None, begin_date=None, end_date=None, user=None, message=None, output=None, settings=None, status=None, task_note=None):
        super(TaskResponse, self).__init__()
        self.has_attachments = has_attachments
        self.task_id = task_id
        self.task_gu_id = task_gu_id
        self.task_type = task_type
        self.begin_date = begin_date
        self.end_date = end_date
        self.user = user
        self.message = message
        self.output = output
        self.settings = settings
        self.status = status
        self.task_note = task_note
