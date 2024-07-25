import io
from argparse import Namespace
from typing import Annotated

import aiohttp
import nonebot.adapters.onebot.v12 as onebot
from PIL import Image
from nonebot import on_shell_command
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.params import ShellCommandArgs
from nonebot.rule import ArgumentParser

from ..utils.cache import FileCache
from ..utils.downloader import download_url, FileTooLargeError

parser = ArgumentParser()
parser.add_argument('url', nargs='?')

sticker = on_shell_command("sticker", parser=parser, aliases={"贴纸", "表情"}, priority=10, block=True)


@sticker.handle()
async def _(matcher: Matcher, args: Annotated[Namespace, ShellCommandArgs()], bot: onebot.Bot, ):
    # 提供url的时候需要下载然后生成
    if args.url is not None:
        # 下载sticker
        try:
            image_bytes = await download_url(args.url)
        except FileTooLargeError:
            await sticker.finish("文件太大，我下载不了呜呜😢")
            return
        except aiohttp.ClientPayloadError:
            await sticker.finish("网络错误，导致下载失败了😞")
            return
        except Exception as e:
            raise e

        # sticker转格式
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # 验证图片没有被损坏
            gif_stream = io.BytesIO()
            image = Image.open(io.BytesIO(image_bytes))  # 重新打开因为verify()会关闭文件
            image.save(gif_stream, format='GIF')
            image_bytes = gif_stream.getvalue()
        except (IOError, SyntaxError):
            await sticker.finish("这好像不是一张图片欸😿")
            return
        except Exception as e:
            raise e

        # 上传bot
        image_id = await FileCache.upload_bytes(data=image_bytes, name="sticker.gif", bot=bot)
        matcher.set_arg("image", onebot.Message(onebot.MessageSegment.image(file_id=image_id)))


@sticker.got("image", "请发图片，我来帮你做成sticker哦😊")
async def _(image: Annotated[onebot.Message, Arg()]):
    if image.only("image") or image.only("wx.emoji"):
        file_id = image[0].data.get("file_id")
    else:
        return await sticker.finish("这个不是图片呢，不能做成sticker呢😣")

    await sticker.finish(onebot.MessageSegment("wx.emoji", {"file_id": file_id}))
