from argparse import Namespace
from typing import Annotated

import nonebot.adapters.onebot.v12 as onebot
from nonebot import on_shell_command, logger
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.params import ArgPlainText
from nonebot.params import ShellCommandArgs
from nonebot.rule import ArgumentParser

WT_MESSAGE = "哎呀，这里需要文字哦~"

parser = ArgumentParser()
parser.add_argument('title', nargs='?')
parser.add_argument('des', nargs='?')
parser.add_argument('url', nargs='?')

article = on_shell_command("article", parser=parser, aliases={"文章"}, priority=10, block=True)


@article.handle()
async def _(matcher: Matcher, args: Annotated[Namespace, ShellCommandArgs()]):
    logger.debug(args)
    if args.title is not None:
        matcher.set_arg("title", onebot.Message(args.title))
    if args.des is not None:
        matcher.set_arg("des", onebot.Message(args.des))
    if args.url is not None:
        matcher.set_arg("url", onebot.Message(args.url))


@article.got("title", "说一下文章的标题吧~")
async def _(title: Annotated[onebot.Message, Arg()]):
    if not title.only("text"):
        await article.reject(WT_MESSAGE)


@article.got("des", "说一下文章的简介吧~")
async def _(des: Annotated[onebot.Message, Arg()]):
    if not des.only("text"):
        await article.reject(WT_MESSAGE)


@article.got("url", "说一下文章的链接吧~")
async def _(url: Annotated[onebot.Message, Arg()]):
    if not url.only("text"):
        await article.reject(WT_MESSAGE)


@article.got("image", "说一下文章的配图吧~")
async def _(title: Annotated[onebot.Message, ArgPlainText()],
            des: Annotated[onebot.Message, ArgPlainText()],
            url: Annotated[onebot.Message, ArgPlainText()],
            image: Annotated[onebot.Message, Arg()]):
    if image.only("image") or image.only("wx.emoji"):
        file_id = image[0].data.get("file_id")
        logger.debug(file_id)
    else:
        await article.send("这个不是图片呢，跳过它了~")
        file_id = None

    await article.finish(onebot.MessageSegment("wx.link", {
        "title": title,
        "des": des,
        "url": url,
        "file_id": file_id
    }))
