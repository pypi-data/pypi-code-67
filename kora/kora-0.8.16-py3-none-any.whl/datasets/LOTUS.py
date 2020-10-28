"""
LOTUS Speech Corpus for ASR, by NECTEC
Licensed under CC-BY-NC-SA
"""

import os


def download():
    url = "https://github.com/korakot/corpus/releases/download/v1.0/AIFORTHAI-LotusCorpus.zip"
    print("NECTEC licenses LOTUS under CC-BY-NC-SA")
    print("Start downloading: .. ")
    os.system(f"wget {url}")
    os.system("unzip AIFORTHAI-LotusCorpus.zip")
    # --strip-components=1
    os.system("mv LOTUS-CD-FREE/* .")
    os.system("rmdir LOTUS-CD-FREE")
    print("Finished")
