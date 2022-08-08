import os.path
from unittest import TestCase

from ali_oss.upload import upload_img


class Test(TestCase):
    def test_upload_img(self):
        fp = "/Users/mark/Pictures/微信精选/宫崎骏-2001-千与千寻/cover_growth.jpg"
        fn = os.path.basename(fp)
        result = upload_img(fp)
        self.assertEqual(fn, os.path.basename(result), msg="上传后的文件地址结尾应该与basename一致")
