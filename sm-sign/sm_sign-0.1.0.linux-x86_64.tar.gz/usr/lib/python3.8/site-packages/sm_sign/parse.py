import argparse
import sys
from .sign import *
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="commands", dest = "command")
# generate keys
genkey_parser = subparsers.add_parser('genkey', help='Generate Key Pair')
genkey_parser.add_argument("-k","--key", help="pkcs8 key file for sign", required = True)
genkey_parser.add_argument("-p", "--password", help="password for privatekey", required = True)
genkey_parser.add_argument("--privkey", help="privatekey name", required = True)
genkey_parser.add_argument("--pubkey", help="public key name", required = True)
genkey_parser.set_defaults(func = genkey)

# sign apk
sign_parser = subparsers.add_parser('sign', help='Sign APK file')
sign_parser.add_argument("-i","--input", help="input apk file for sign", required = True)
sign_parser.add_argument("-o","--output", help="output apk file for sign", required = True)
sign_parser.add_argument("-k", "--key", help="pkcs8 private_key file for sign", required = True)
sign_parser.add_argument("--pubkey", help="pem public key file name", required = True)
sign_parser.set_defaults(func=sign)

# verify apk
verify_parser = subparsers.add_parser('verify', help="Verify APK")
verify_parser.add_argument("-i", "--input", help="input apk file for verify", required = True)
verify_parser.set_defaults(func=verify)
# parser.add_argument("-g", "--genkey", help="generate privkey and certificate file.", action = "store_true")
# parser.add_argument("-i","--input", help="input apk file for sign")
# parser.add_argument("-o","--output", help="output apk file for sign")
# parser.add_argument("-k","--key", help="key file for sign")
# parser.add_argument("-s","--sign", help="sign apk with given key", action = "store_true")
# parser.add_argument("-p", "--password", help="password for privatekey")
# parser.add_argument("--privkey", help="privatekey name")
# parser.add_argument("--pubkey", help="public key name")
# parser.add_argument("-v", "--verify", help="verify the signed apk", action = "store_true")
# try:
#     args = parser.parse_args()
# except:
#     parser.print_help()
#     sys.exit(0)
# print(args.echo)