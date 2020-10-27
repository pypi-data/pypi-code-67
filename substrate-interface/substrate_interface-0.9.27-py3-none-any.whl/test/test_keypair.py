# Python Substrate Interface Library
#
# Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from substrateinterface import Keypair
from bip39 import bip39_validate


class KeyPairTestCase(unittest.TestCase):

    def test_generate_mnemonic(self):
        mnemonic = Keypair.generate_mnemonic()
        self.assertTrue(bip39_validate(mnemonic))

    def test_invalid_mnemic(self):
        mnemonic = "This is an invalid mnemonic"
        self.assertFalse(bip39_validate(mnemonic))

    def test_create_sr25519_keypair(self):
        mnemonic = "old leopard transfer rib spatial phone calm indicate online fire caution review"
        keypair = Keypair.create_from_mnemonic(mnemonic, address_type=0)

        self.assertEqual(keypair.ss58_address, "16ADqpMa4yzfmWs3nuTSMhfZ2ckeGtvqhPWCNqECEGDcGgU2")

    def test_only_provide_ss58_address(self):

        keypair = Keypair(ss58_address='16ADqpMa4yzfmWs3nuTSMhfZ2ckeGtvqhPWCNqECEGDcGgU2')
        self.assertEqual(keypair.public_key, '0xe4359ad3e2716c539a1d663ebd0a51bdc5c98a12e663bb4c4402db47828c9446')

    def test_only_provide_public_key(self):

        keypair = Keypair(
            public_key='0xe4359ad3e2716c539a1d663ebd0a51bdc5c98a12e663bb4c4402db47828c9446',
            address_type=0
        )
        self.assertEqual(keypair.ss58_address, '16ADqpMa4yzfmWs3nuTSMhfZ2ckeGtvqhPWCNqECEGDcGgU2')

    def test_provide_no_ss58_address_and_public_key(self):
        self.assertRaises(ValueError, Keypair)

    def test_incorrect_private_key_length_sr25519(self):
        self.assertRaises(
            ValueError, Keypair, private_key='0x23', ss58_address='16ADqpMa4yzfmWs3nuTSMhfZ2ckeGtvqhPWCNqECEGDcGgU2'
        )

    def test_incorrect_public_key(self):
        self.assertRaises(ValueError, Keypair, public_key='0x23')

    def test_sign_and_verify(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic)
        signature = keypair.sign("Test123")
        self.assertTrue(keypair.verify("Test123", signature))

    def test_sign_and_verify_hex_data(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic)
        signature = keypair.sign("0x1234")
        self.assertTrue(keypair.verify("0x1234", signature))

    def test_sign_and_verify_incorrect_signature(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic)
        signature = "0x4c291bfb0bb9c1274e86d4b666d13b2ac99a0bacc04a4846fb8ea50bda114677f83c1f164af58fc184451e5140cc8160c4de626163b11451d3bbb208a1889f8a"
        self.assertFalse(keypair.verify("Test123", signature))

    def test_sign_and_verify_invalid_signature(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic)
        signature = "Test"
        self.assertRaises(TypeError, keypair.verify, "Test123", signature)

    def test_sign_and_verify_invalid_message(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic)
        signature = keypair.sign("Test123")
        self.assertFalse(keypair.verify("OtherMessage", signature))

    def test_create_ed25519_keypair(self):
        mnemonic = "old leopard transfer rib spatial phone calm indicate online fire caution review"
        keypair = Keypair.create_from_mnemonic(mnemonic, address_type=0, crypto_type=Keypair.ED25519)

        self.assertEqual(keypair.ss58_address, "16dYRUXznyhvWHS1ktUENGfNAEjCawyDzHRtN9AdFnJRc38h")

    def test_sign_and_verify_ed25519(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic, crypto_type=Keypair.ED25519)
        signature = keypair.sign("Test123")

        self.assertTrue(keypair.verify("Test123", signature))

    def test_sign_and_verify_invalid_signature_ed25519(self):
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_mnemonic(mnemonic, crypto_type=Keypair.ED25519)
        signature = "0x4c291bfb0bb9c1274e86d4b666d13b2ac99a0bacc04a4846fb8ea50bda114677f83c1f164af58fc184451e5140cc8160c4de626163b11451d3bbb208a1889f8a"
        self.assertFalse(keypair.verify("Test123", signature))

    def test_unsupport_crypto_type(self):
        self.assertRaises(
            ValueError, Keypair.create_from_seed,
            seed_hex='0xda3cf5b1e9144931?a0f0db65664aab662673b099415a7f8121b7245fb0be4143',
            crypto_type=2
        )

    def test_create_keypair_from_private_key(self):
        keypair = Keypair.create_from_private_key(
            ss58_address='16ADqpMa4yzfmWs3nuTSMhfZ2ckeGtvqhPWCNqECEGDcGgU2',
            private_key='0x1f1995bdf3a17b60626a26cfe6f564b337d46056b7a1281b64c649d592ccda0a9cffd34d9fb01cae1fba61aeed184c817442a2186d5172416729a4b54dd4b84e'
        )
        self.assertEqual(keypair.public_key, '0xe4359ad3e2716c539a1d663ebd0a51bdc5c98a12e663bb4c4402db47828c9446')


if __name__ == '__main__':
    unittest.main()
