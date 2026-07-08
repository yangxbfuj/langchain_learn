from wechatbot import WeChatBot

from ch2.practice.agent.runner import build_runner

bot = WeChatBot()

angent_runner = build_runner()


@bot.on_message
async def handle(msg):
    result = await angent_runner.ainvoke(msg.text)
    await bot.reply(msg, result)


bot.run()  # 扫码登录 + 开始监听
