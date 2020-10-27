from typing import Any, Dict, Optional, Tuple

from click import ClickException
from openapi_client.rest import ApiException  # type: ignore

from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.util import format_api_exception


def get_cloud_json_from_id(cloud_id: str, api_client: DefaultApi) -> Dict["str", Any]:
    try:
        cloud = api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id
        ).result
    except ApiException:
        raise ClickException(
            f"The cloud with id, {cloud_id} has been deleted. Please create a new cloud with `anyscale cloud setup`."
        )
    return {
        "id": cloud.id,
        "name": cloud.name,
        "provider": cloud.provider,
        "region": cloud.region,
        "credentials": cloud.credentials,
    }


def get_cloud_id_and_name(
    api_client: DefaultApi,
    cloud_id: Optional[str] = None,
    cloud_name: Optional[str] = None,
) -> Tuple[str, str]:
    if cloud_id and cloud_name:
        raise ClickException(
            "Both '--cloud-id' and '--cloud-name' specified. Please only use one."
        )
    elif cloud_name:
        with format_api_exception(ApiException):
            resp_get_cloud = api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post(
                cloud_name_options={"name": cloud_name}
            )
        cloud = resp_get_cloud.result
    elif cloud_id:
        with format_api_exception(ApiException):
            resp_get_cloud = api_client.get_cloud_api_v2_clouds_cloud_id_get(
                cloud_id=cloud_id
            )

        cloud = resp_get_cloud.result
    else:
        with format_api_exception(ApiException):
            clouds = api_client.list_clouds_api_v2_clouds_get().results
        if len(clouds) > 1:
            raise ClickException(
                "Multiple clouds: {}\n"
                "Please specify the one you want to refer to.".format(
                    [cloud.name for cloud in clouds]
                )
            )
        cloud = clouds[0]
    return cloud.id, cloud.name
