"""
update @rq
1. install ali-oss-sdk, ref: https://help.aliyun.com/document_detail/85288.html
$ pip3 install oss2

2. verify the dependency of oss2: crcmod, passed when no error generated
$ python3
> import crcmod._crcfunext

[简单上传](https://help.aliyun.com/document_detail/88426.html)
Object完整路径。Object完整路径中不能包含Bucket名称。
Object命名规范如下：
    使用UTF-8编码。
    长度必须在1~1023字符之间。
    不能以正斜线（/）或者反斜线（\\）开头。

"""

import logging
import os
from typing import List
from urllib.parse import quote

import oss2


def _get_filename_robust(_fp: str) -> List[str]:
    if not os.path.exists(_fp):
        raise Exception("not exist file at: " + _fp)

    # use quote in case of space or chinese words: https://stackoverflow.com/a/40557716/9422455
    filename = quote(os.path.basename(_fp))
    logging.info({"file_path": _fp})
    return [filename, _fp]


def _upload_ali_oss(endpoint, bucket_name, fp: str) -> str:
    fn, fp = _get_filename_robust(fp)
    result = ali_oss_bucket.put_object_from_file(fn, fp)

    assert result.status == 200
    filepath_oss = f"https://{bucket_name}.{endpoint}/{fn}"
    logging.info({"filepath_oss": filepath_oss})
    return filepath_oss


def upload_img(fp: str):
    return _upload_ali_oss(ALI_ENDPOINT, ALI_BUCKET_NAME, fp)


ALI_AK = os.environ["ALI_AK"]
ALI_SK = os.environ["ALI_SK"]
ali_oss_auth = oss2.Auth(ALI_AK, ALI_SK)

ALI_ENDPOINT = os.environ["ALI_ENDPOINT"]
ALI_BUCKET_NAME = os.environ["ALI_BUCKET_NAME"]
ali_oss_bucket = oss2.Bucket(ali_oss_auth, ALI_ENDPOINT, ALI_BUCKET_NAME)
