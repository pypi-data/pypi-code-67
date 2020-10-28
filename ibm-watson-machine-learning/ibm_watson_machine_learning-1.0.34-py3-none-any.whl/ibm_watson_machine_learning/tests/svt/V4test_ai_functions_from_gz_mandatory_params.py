import unittest

from ibm_watson_machine_learning.utils.log_util import get_logger
from preparation_and_cleaning import *
from models_preparation import *


class TestAIFunction(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    scoring_url = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestAIFunction.logger.info("Service Instance: setting up credentials")
        self.function_filepath = os.path.join(os.getcwd(), 'artifacts', 'ai_function.gz')

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()

        self.function_name = 'simplest AI function'
        self.deployment_name = "Test deployment"

    def test_01_service_instance_details(self):
        TestAIFunction.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'APIClient')

        TestAIFunction.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()
        TestAIFunction.logger.debug(details)

        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_02_create_ai_function(self):

        self.client.repository.FunctionMetaNames.show()

        ai_function_details = self.client.repository.store_function(self.function_filepath, 'simplest AI function')

        TestAIFunction.function_uid = self.client.repository.get_function_uid(ai_function_details)
        function_url = self.client.repository.get_function_href(ai_function_details)
        TestAIFunction.logger.info("AI function ID:" + str(TestAIFunction.function_uid))
        TestAIFunction.logger.info("AI function URL:" + str(function_url))
        self.assertIsNotNone(TestAIFunction.function_uid)
        self.assertIsNotNone(function_url)
        TestAIFunction.runtime_uid = self.client.runtimes.get_uid(ai_function_details)

    def test_03_download_ai_function_content(self):
        try:
            os.remove('test_ai_function.tar.gz')
        except:
            pass

        self.client.repository.download(TestAIFunction.function_uid, filename='test_ai_function.tar.gz')

        try:
            os.remove('test_ai_function.gz')
        except:
            pass

    def test_04_get_details(self):
        details = self.client.repository.get_function_details()
        self.assertTrue(self.function_name in str(details))

        details = self.client.repository.get_function_details(self.function_uid)
        self.assertTrue(self.function_name in str(details))

        details = self.client.repository.get_details()
        self.assertTrue("functions" in details)

        details = self.client.repository.get_details(self.function_uid)
        self.assertTrue(self.function_name in str(details))

    def test_05_list(self):
        self.client.repository.list()

        self.client.repository.list_functions()

    def test_06_create_deployment(self):
        TestAIFunction.logger.info("Create deployment")
        deploy_meta = {
            self.client.deployments.ConfigurationMetaNames.NAME: self.deployment_name,
            self.client.deployments.ConfigurationMetaNames.DESCRIPTION: "deployment_description",
            self.client.deployments.ConfigurationMetaNames.ONLINE:{}
        }
        deployment = self.client.deployments.create(artifact_uid=self.function_uid, meta_props=deploy_meta)
        TestAIFunction.logger.debug("deployment: " + str(deployment))
        TestAIFunction.scoring_url = self.client.deployments.get_scoring_href(deployment)
        TestAIFunction.logger.debug("Scoring href: {}".format(TestAIFunction.scoring_url))
        TestAIFunction.deployment_uid = self.client.deployments.get_uid(deployment)
        TestAIFunction.logger.debug("Deployment uid: {}".format(TestAIFunction.deployment_uid))
        self.assertTrue("online" in str(deployment))

    def test_07_get_deployment_details(self):
        TestAIFunction.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details()
        TestAIFunction.logger.debug("Deployment details: {}".format(deployment_details))
        self.assertTrue(self.deployment_name in str(deployment_details))

    def test_08_score(self):
        scoring_data = {
            "input_data": [{
            "fields": ["Gender", "Status", "Children", "Age", "Customer_Status"],
            "values": [
                ["Male", "M", 2, 48, "Inactive"],
                ["Female", "S", 0, 23, "Inactive"]
            ]
            }]
        }
        predictions = self.client.deployments.score(TestAIFunction.scoring_url, scoring_data)
        print("Predictions: {}".format(predictions))
        self.assertTrue("values" in str(predictions))

    def test_09_delete_deployment(self):
        TestAIFunction.logger.info("Delete deployment")
        self.client.deployments.delete(TestAIFunction.deployment_uid)

    def test_10_delete_function(self):
        TestAIFunction.logger.info("Delete function")
        self.client.repository.delete(TestAIFunction.function_uid)


if __name__ == '__main__':
    unittest.main()
