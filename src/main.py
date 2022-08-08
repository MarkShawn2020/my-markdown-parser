import argparse
import os

from md_analysis.fetchMds import yieldMds
from md_analysis.uploadImgsFromMd import uploadImgsFromMd

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("command", choices=["upload-imgs"], default="upload-imgs")
    args.add_argument("-s", "--source")
    args.add_argument("--imgRoot", help="图片集中存储的文件夹地址")

    parser = args.parse_args()

    source = parser.source
    assert os.path.exists(source), f"source [{source}] not exists!"
    IS_DIR = os.path.isdir(source)

    imgRoot = parser.imgRoot
    if imgRoot:
        assert os.path.exists(imgRoot), f"img root [{imgRoot}] not exists!"

    if parser.command == "upload-imgs":
        if not IS_DIR:
            uploadImgsFromMd(source, imgRoot=imgRoot)
        else:
            for fp in yieldMds(source):
                uploadImgsFromMd(fp["path"], imgRoot=imgRoot)
