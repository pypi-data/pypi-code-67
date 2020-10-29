from zipfile import ZipFile
import io
# dir = "/mnt/d/Documents/Chores/homework/NSS/main/lab/sslc/test/valid/"
# file_name = "com.android.vending-16.apk"
# import sm
import getopt, sys
import os.path
import base64
# from parse import args
def genkey(args):
    pubkey = args.pubkey.encode('utf-8')
    privkey = args.privkey.encode('utf-8')
    passwd = args.password.encode('utf-8')
    keyfile = args.key.encode('utf-8')
    sm.generate_SM2_key_files(pubkey, privkey, passwd)
    key = sm.read_private_key(privkey, passwd)
    pkcs8 = sm.write_pkcs8(keyfile, key, passwd)

def sign(args):
    ifile = args.input
    priv_key = args.key.encode('utf-8')
    pubkey = args.pubkey.encode('utf-8')
    ofile = args.output
    sign_apk = ZipFile(ofile, mode='w')
    with ZipFile(ifile, 'r') as zfile:
        mf = b'Manifest-Version: 1.0\nBuilt-By: Sign tool\nCreated-By: Siliang Qin\n'
        dgst = b''
        for finfo in zfile.infolist():
            if('META-INF' in finfo.filename):
                continue
            content = zfile.read(finfo.filename)
            sign_apk.writestr(finfo.filename, content)
            s = sm.SM3(content)
            dgst += b'\nName: %s\nSM3-Digest: %s\n' % (
                finfo.filename.encode('utf-8'), base64.b64encode(s))
        mf += dgst
        sign_apk.writestr('META-INF/MANIFEST.MF', mf)
        sf = b"Signature-Version: 1.0\nX-Android-APK-Signed: 2\n"
        sf += b"SM3-Digest-Manifest: "
        sf += base64.b64encode(sm.SM3(mf))
        sf += b'\nCreated-By: 1.0 (Android)\n'
        sf += dgst
        sign_apk.writestr('META-INF/CERT.SF', sf)
        key = sm.read_pkcs8(priv_key)
        # key = sm.read_private_key(priv_key, "12345678")
        pubkey = sm.read_public_key(pubkey)
        # sign = sm.SM2_SIGN(sf, key)
        x509 = sm.generate_x509(key, pubkey, b'cert.x509')
        p7 = sm.pkcs7_sign(x509, key, sf.replace(b'\n', b''))
        # print(p7)
        sign_apk.writestr('META-INF/CERT.SM2', p7)
        # print(sign)
        # print(sm.pkcs7_verify(p7, sf.replace(b'\n', b'')))
    sign_apk.close()

def parse_sf(sf):
    lines = sf.split(b'\n')
    name = ''
    d = {}
    for line in lines:
        l = line.strip(b'\n').replace(b' ', b'').split(b':')
        # print(l)
        try:
            if len(l) > 1:
                d[l[0]] = l[1]
            if b'SM3-Digest' == l[0]:
                d[d[b'Name'].decode('utf-8')] = l[1]
        except:
            print(l)
    return d
        

def verify(args):
    ifile = args.input
    with ZipFile(ifile, 'r') as zfile:
        sf = zfile.read('META-INF/CERT.SF')
        sm3 = parse_sf(sf)
        for finfo in zfile.infolist():
            if('META-INF' in finfo.filename):
                continue
            content = zfile.read(finfo.filename)
            s = sm.SM3(content)
            s = base64.b64encode(s)
            print(finfo.filename + ":")
            print("CERT.SF  : %s" % sm3[finfo.filename])
            print("File hash: %s" % s)
            print()
            if (s != sm3[finfo.filename]):
                print(finfo.filename + "SM3 hash check failed")
                sys.exit(-1)
                
        mf = zfile.read('META-INF/MANIFEST.MF')
        mfsm3 = sm.SM3(mf)
        mfsm3 = base64.b64encode(mfsm3)
        print("META-INF/MANIFEST.MF:")
        print("CERT.SF  : %s" % sm3[b"SM3-Digest-Manifest"])
        print("File hash: %s" % mfsm3)
        if mfsm3 != sm3[b'SM3-Digest-Manifest']:
            print("MANIFEST.MF SM3 Check Failed!")
            sys.exit(-1)
        print()
        sm2 = zfile.read('META-INF/CERT.SM2')
        print("Verifying Signature...")
        # sm.init()
        if sm.pkcs7_verify(sm2,sf.replace(b'\n', b'')):
            print("Success")
        else:
            print("Failed")
            sys.exit(-1)
