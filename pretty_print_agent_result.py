from rich.console import Console, Group
from rich.panel import Panel


async def pprint(result, question):
    console = Console()
    answer_panel = Panel(result["messages"][-1].content, title="Answer")
    group = Group(*[
        Panel(msg.model_dump_json(indent=2), title=f"{i}: {type(msg).__name__}")
        for i, msg in enumerate(result["messages"])
    ])
    messages_pannel = Panel(group, title="Messages")
    full_panel = Panel(Group(answer_panel, messages_pannel), title=question)
    console.print(full_panel)
