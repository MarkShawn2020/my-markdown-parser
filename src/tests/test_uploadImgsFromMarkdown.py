from unittest import TestCase

from md_analysis.uploadImgsFromMd import uploadImgsFromMd


class Test(TestCase):
    def test_upload_local_imgs_from_markdown_file(self):
        fp = "/Users/mark/mark_keeps_learning/core/notes/wechat-moments-dump.md"
        uploadImgsFromMd(fp)
        with open(fp) as f:
            s = f.read()
            self.assertTrue("](." not in s)
