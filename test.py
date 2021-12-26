import interactions
import apscheduler
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = interactions.Client(token="???")
scheduler = AsyncIOScheduler()
scheduler.start()

def isint(n):
    try:
        int(n)
        return True
    except:
        return False

@bot.event
async def on_ready():
    print("ready")

@bot.command(
    name="우편함",
    description="미래의 누군가에게 편지를 부쳐보세요!",
    scope=[820964115131793449],#, 851650387039617035], 
    options=[interactions.Option(type=interactions.OptionType.USER, name="send_to", description="이분에게 작성하실 편지가 전달돼요! 전달 대상을 선택하시면 돼요!", required=True), 
            interactions.Option(type=interactions.OptionType.STRING, name="content", description="편지의 내용을 작성해 주세요!", required=True), 
            interactions.Option(type=interactions.OptionType.STRING, name="open_date", description="편지가 자동으로 전달될 날짜를 지정해 주세요! 반드시 <년>:<월>:<일>:<시>:<분>의 양식을 24시계로 채워서 전달해 주세요!", required=True)]
)
async def test(ctx, send_to, content, open_date):

    #parse dates
    dates=open_date.split(":")
    a=0
    for date in dates:
        if not isint(date):
            a+=1
    if len(dates)==5 and a==0:
        targetdate=datetime.datetime(year=int(dates[0]), month=int(dates[1]), day=int(dates[2]), hour=int(dates[3]), minute=int(dates[4]))
    else:
        await ctx.send("날짜의 양식이 잘못된 것 같아요! <년>:<월>:<일>:<시>:<분>의 양식으로 입력해 주세요! 24시계로 작성하는 것도 잊지 마시고요!\n*24시계: 오후 10시를 22시로 표기하는 방식", ephemeral=True)
        return
    if targetdate>datetime.datetime.now():
        pass
    else:
        await ctx.send("흠.. 날짜가 아무래도 이상해요! 과거로 편지를 부치는 건 불가능해요!", ephemeral=True)
        return

    scheduler.add_job(sendletter, 'date', run_date=targetdate, kwargs={"send_to": send_to, "_from": ctx.author.user.id, "content": content, "then": (datetime.datetime.now()).replace(microsecond=0)}, replace_existing=False)

    await ctx.send("우편함에 편지가 들어갔습니다!", ephemeral=True)

async def sendletter(send_to, _from, content, then):
    origin=await bot.http.get_user(int(_from))
    channel = interactions.api.models.channel.Channel(**await bot.http.create_dm(recipient_id=int(send_to)))
    await bot.http.send_message(channel_id=int(channel.id), content=
        f"""{origin["username"]}님께서 {str(then)}에 메시지를 보내셨습니다.
        ```{content}```
    """)

bot.start()