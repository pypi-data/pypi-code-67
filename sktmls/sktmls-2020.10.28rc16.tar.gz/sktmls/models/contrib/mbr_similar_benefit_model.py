import random
from collections import OrderedDict
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List

from pytz import timezone

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient
from sktmls.models import MLSRuleModel, MLSModelError

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {
    "hourly": "%Y%m%d%H",
    "daily": "%Y%m%d",
    "weekly": "%Y%W",
    "monthly": "%Y%m",
    "yearly": "%Y",
    "none": "%c%f",
}


class MbrSimilarBenefitModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    멤버십 유사 혜택 추천에 특화된 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        categories: List[str],
        item_type: str,
        num_pick: int = 1,
        random_cycle: str = "daily",
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 리스트 (필수 피쳐: `user_id`, `use_benefit`, `like_benefit`)
        - categories: (list(str)) 전체 카테고리 리스트. 필수 피쳐 이후 피쳐 순서와 동일해야 합니다.
        - item_type: (str) 결과의 `type`에 표기할 값
        - num_pick: (optional) (int) 랜덤 추출할 갯수 (기본값: 1)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`|`none`) (기본값: `daily`)
            - `none`의 경우 매 호출마다 초기화합니다.

        ## Example

        ```python
        my_model_v1 = MbrSimilarBenefitModel(
            model_name="my_model",
            model_version="v1",
            features=["user_id", "use_benefit", "like_benefit", "available_benefit_activity", "available_benefit_asianfood", "available_benefit_beauty"],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="mbr_similar_benefit",
            num_pick=14,
            random_cycle="daily"
        )

        result = my_model_v1.predict(["1234567890", None, ["1", "5", "6"], ["a1", "a2", "a3", "a4"], None, ["b1", "b2", "3", "4"]])
        ```
        """
        assert (
            isinstance(features, list) and len(features) > 0 and features[0] == "user_id"
        ), "`features`가 유효하지 않습니다. `features`의 첫 값은 반드시 `user_id`이어야 합니다."
        assert isinstance(categories, list) and len(categories) + 3 == len(
            features
        ), "전체 카테고리 리스트 길이가 필수 피쳐를 제외한 피쳐의 수와 다릅니다."
        assert isinstance(num_pick, int) and num_pick > 0, "`num_pick`이 유효하지 않습니다. 반드시 1 이상의 값을 가져야 합니다."
        assert random_cycle in SEED_FORMAT, "허용되지 않는 `random_cycle`값입니다."

        super().__init__(model_name, model_version, features)

        self.pf_client = MLSProfileAPIClient(runtime_env=MLSRuntimeENV.MMS)

        self.categories = categories
        self.item_type = item_type
        self.num_pick = num_pick
        self.random_cycle = random_cycle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        for i, f in enumerate(x[1:]):
            if f is not None and not isinstance(f, list):
                raise MLSModelError(f"MbrSimilarBenefitModel: {self.features[i + 1]}이 리스트 형식으로 전달되지 않았습니다.")

        user_id = x[0]
        use_benefit = x[1] or []
        like_benefit = x[2] or []

        if not use_benefit and not like_benefit:
            return {"items": []}

        available_benefit = {
            category: x[i + 3]
            for i, category in enumerate(self.categories)
            if isinstance(x[i + 3], list) and len(x[i + 3]) >= 1
        }

        random.seed(f"{user_id}{self.item_type}{datetime.now(TZ).strftime(SEED_FORMAT[self.random_cycle])}")

        source_act_benefit = [("use", i) for i in use_benefit] + [("like", i) for i in like_benefit]
        source_act, source_benefit_id = random.choice(source_act_benefit)

        item_profile = self.pf_client.get_item_profile(
            profile_id="tmembership_benefit", item_id=source_benefit_id, keys=["brand", "similar_items"]
        )

        if (
            None in item_profile.values()
            or "brand_id" not in item_profile["brand"]
            or not isinstance(item_profile["similar_items"], list)
            or not item_profile["similar_items"]
        ):
            return {"items": []}

        source_brand = str(item_profile["brand"]["brand_id"])
        target_benefit_list = item_profile["similar_items"]

        available_benefit_list = reduce(lambda a, b: a + b, available_benefit.values(), [])
        valid_target_benefit_list = list(
            OrderedDict.fromkeys(filter(lambda x: x in available_benefit_list, target_benefit_list))
        )

        candidates = [
            {
                "id": benefit,
                "name": "#",
                "type": self.item_type,
                "props": {
                    "context_id": f"{source_act}_brand_{source_brand}",
                    "context_nm": f"브랜드_{source_brand}_{'사용' if source_act == 'use' else '좋아요'}_유사혜택",
                },
            }
            for benefit in valid_target_benefit_list
        ]

        num_pick = min(self.num_pick, len(candidates))
        top_candidates = candidates[:num_pick]

        return {"items": top_candidates}
