import asyncio
from mcp import Client, StdioServerParameters

async def main():
    params = StdioServerParameters(command="uv", args=["run", "cost_server.py"])
    async with Client(params) as client:
        tools = await client.list_tools()
        for t in tools.tools:
            print("tool:", t.name)
        r = await client.call_tool("lookup_price", {"service": "vm", "size": "medium"})
        print("lookup_price:", r.content[0].text)
        r = await client.call_tool("convert_currency", {"amount": 290, "from_cur": "USD", "to_cur": "CUR"})
        print("convert_currency:", r.content[0].text)

asyncio.run(main())