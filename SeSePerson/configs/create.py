from ipaddress import IPv4Address
from pathlib import Path

from .console import Console

console = Console()


def init_config(config_path: Path, default_config_path: Path):
    console.print("\n[b]涩涩人，启动！[/b]\n", style="#87ceeb")

    console.info("这是你第一次启动本项目, 请根据提示填写信息")
    console.info("如中途填写错, 你可以直接退出, 再次启动以重新填写")
    console.info("如需使用默认值, Enter 跳过方可\n")

    console.info("[b]Bot 主体设置[/b]\n", style="white")
    host = console.get(
        "Bot 监听的主机名 (IP). 如有控制台相关需求, 建议: [green]0.0.0.0[/green] (默认: [green]127.0.0.1[/green])",
        "127.0.0.1",
        IPv4Address,
        "输入不正确 示例: 127.0.0.1",
    )
    port = console.get(
        "Bot 对外开放的端口 (Port). 范围建议: [green]10000-60000[/green] (默认: [green]20000[/green])",
        "20000",
        int,
        "输入不正确 示例: 20000",
    )
    superusers = console.get(
        "超级用户 (wxid), 即涩涩人的[b]主人[/b]. 可填多个, 用英文逗号 (,) 隔开 (默认: [green]wxid_y1145141919810[/green])",
        "wxid_y1145141919810",
        str,
        "输入不正确 示例: wxid_y1145141919810",
    )
    access_token = console.get(
        "协议端通信密钥, 此项留空[b]将无法进入控制台[/b]. 无长度限制 示例: [green]21^sASDA!@3l67GJlk7sd!14#[/green]",
        "",
        str,
        "输入不正确 示例: 21^sASDA!@3l67GJlk7sd!14# (请尽可能复杂, 无长度限制)",
    )
    proxy = console.get(
        "是否有代理. 格式参考: http(s)://127.0.0.1:8100 (如无请 Enter 以跳过)",
        "",
        str,
        "输入不正确 示例: http://127.0.0.1:8100",
    )
    console.success("Bot 主体配置完成\n")

    console.success("[white]至此, 所需基本配置已填写完毕[white]")

    raw_conf = default_config_path.read_text("utf-8")
    raw_conf = raw_conf.format(host=host,
                               port=port,
                               superusers=superusers.split(","),
                               access_token=access_token,
                               proxy=proxy)
    config_path.write_text(raw_conf, encoding="utf-8")
