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

class DescribeInstancePerformanceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'polardbx', '2020-02-02', 'DescribeInstancePerformance','polardbx')
		self.set_method('POST')

	def get_DbInstanceName(self):
		return self.get_query_params().get('DbInstanceName')

	def set_DbInstanceName(self,DbInstanceName):
		self.add_query_param('DbInstanceName',DbInstanceName)

	def get_Keys(self):
		return self.get_query_params().get('Keys')

	def set_Keys(self,Keys):
		self.add_query_param('Keys',Keys)

	def get_EndTime(self):
		return self.get_query_params().get('EndTime')

	def set_EndTime(self,EndTime):
		self.add_query_param('EndTime',EndTime)

	def get_StartTime(self):
		return self.get_query_params().get('StartTime')

	def set_StartTime(self,StartTime):
		self.add_query_param('StartTime',StartTime)

	def get_NodeId(self):
		return self.get_query_params().get('NodeId')

	def set_NodeId(self,NodeId):
		self.add_query_param('NodeId',NodeId)