import logging
import os
import re

from ali_oss.upload import upload_img


def ensureImgPath(fp: str, uri: str, imgRoot: str = None):
    """
    attention, it's relative file
    and test tells me when join a _fp with a relative path, we should use its father direcotry path as the base
    see the relpath(yet useless here): https://stackoverflow.com/a/9768491/9422455

    :param fp:
    :param uri:
    :param imgRoot:
    :return:
    """
    imgName = uri.rsplit("/")[-1]
    if imgRoot:
        imgPath = os.path.join(imgRoot, imgName)
    else:
        fd = os.path.dirname(fp)
        imgPath = os.path.join(fd, uri)
    assert os.path.exists(imgPath), f"img file joined [{imgPath}] not exists."
    return imgPath


def uploadImgsFromMd(fp: str, imgRoot: str = None, backup=True) -> None:
    """
    将一个markdown文档里的本地的图片替换为在线图片
    :param fp:
    :param imgRoot:
    :return:
    """

    def uploadImgFromRegexBasedOnFilePath(m: re.Match) -> str:
        """
        将绝对、相对地址的图像链接，转化为上传到服务端后的在线链接
        :param m:
        :return:
        """
        logging.info("matched  : " + m.group())
        uri = m.group()  # type: str
        assert not uri.startswith('http')
        img_real_abs_path = ensureImgPath(fp, uri, imgRoot)
        try:
            converted = upload_img(img_real_abs_path)
            logging.info("converted: " + converted)
            # print(f"converted from {ip} to {converted}")
            return converted
        except Exception as e:
            logging.warning(">>> failed to convert: " + uri)
            print(">>> failed to convert: " + uri)
            return uri

    temp = ""
    f1 = open(fp)
    logging.info("-" * 22)
    logging.info("handling: " + fp)
    for line in f1.readlines():
        if re.search(r'<img', line) is not None:
            # skip http
            line = re.sub(
                r'(?<=src=")(?!http).*?(?=")',
                uploadImgFromRegexBasedOnFilePath, line
            )
        elif re.search(r'!\[.*?]\((?!http).*?\)', line) is not None:
            # very tricky here: limit to not matching second ")"
            line = re.sub(r'(?<=]\()[^)]+?(?=\))', uploadImgFromRegexBasedOnFilePath, line)
        temp += line
    f1.close()

    # backup file
    if backup:
        os.rename(fp, fp + '.bak')
        with open(fp, "w") as f:
            f.write(temp)
    logging.info("finished\n")


if __name__ == '__main__':
    fp = '/Users/mark/keeps-learning/my-website/library/docs/Software/Docusaurus/pr-eslint.md'
    imgRoot = os.path.join(os.path.dirname(fp), '.imgs')
    uploadImgsFromMd(fp, imgRoot)
