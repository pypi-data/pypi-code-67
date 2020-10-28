# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkdrds.endpoint import endpoint_data

class CreateEvaluatePreCheckTaskRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Drds', '2019-01-23', 'CreateEvaluatePreCheckTask','Drds')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_AvgQpsGrowthScale(self):
		return self.get_query_params().get('AvgQpsGrowthScale')

	def set_AvgQpsGrowthScale(self,AvgQpsGrowthScale):
		self.add_query_param('AvgQpsGrowthScale',AvgQpsGrowthScale)

	def get_TaskName(self):
		return self.get_query_params().get('TaskName')

	def set_TaskName(self,TaskName):
		self.add_query_param('TaskName',TaskName)

	def get_DataGrowthScale(self):
		return self.get_query_params().get('DataGrowthScale')

	def set_DataGrowthScale(self,DataGrowthScale):
		self.add_query_param('DataGrowthScale',DataGrowthScale)

	def get_DbInfos(self):
		return self.get_query_params().get('DbInfo')

	def set_DbInfos(self, DbInfos):
		for depth1 in range(len(DbInfos)):
			if DbInfos[depth1].get('InstId') is not None:
				self.add_query_param('DbInfo.' + str(depth1 + 1) + '.InstId', DbInfos[depth1].get('InstId'))
			if DbInfos[depth1].get('DbPort') is not None:
				self.add_query_param('DbInfo.' + str(depth1 + 1) + '.DbPort', DbInfos[depth1].get('DbPort'))
			if DbInfos[depth1].get('DbName') is not None:
				self.add_query_param('DbInfo.' + str(depth1 + 1) + '.DbName', DbInfos[depth1].get('DbName'))
			if DbInfos[depth1].get('DbPassword') is not None:
				self.add_query_param('DbInfo.' + str(depth1 + 1) + '.DbPassword', DbInfos[depth1].get('DbPassword'))
			if DbInfos[depth1].get('DbUser') is not None:
				self.add_query_param('DbInfo.' + str(depth1 + 1) + '.DbUser', DbInfos[depth1].get('DbUser'))

	def get_EvaluateHours(self):
		return self.get_query_params().get('EvaluateHours')

	def set_EvaluateHours(self,EvaluateHours):
		self.add_query_param('EvaluateHours',EvaluateHours)