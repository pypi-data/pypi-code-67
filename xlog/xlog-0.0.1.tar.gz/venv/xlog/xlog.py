import argparse, sys, os
from loguru import logger as logu


def init(ProjName,LogPath,Level):
    file_name = ProjName + "_" + Level + ".log"
    LogPath = LogPath + file_name
    print(LogPath)
    fmt = "{time:YYYY-MM-DD-HH:mm:ss}  |  {level}  |  {message}"
    logu.add(LogPath, level=Level, format=fmt)

def logger(Message):
    logur.info(Message)

init('16s','./','INFO')
logger("Test")

