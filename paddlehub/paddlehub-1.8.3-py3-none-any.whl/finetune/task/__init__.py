#coding:utf-8
#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .base_task import BaseTask, RunEnv, RunState
from .classifier_task import ClassifierTask, ImageClassifierTask, TextClassifierTask, MultiLabelClassifierTask
from .detection_task import DetectionTask
from .generation_task import TextGenerationTask
from .matching_task import PairwiseTextMatchingTask, PointwiseTextMatchingTask
from .reading_comprehension_task import ReadingComprehensionTask
from .regression_task import RegressionTask
from .sequence_task import SequenceLabelTask
