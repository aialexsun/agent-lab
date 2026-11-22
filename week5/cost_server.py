"""MCP server that offers the cloud cost tools to any MCP app."""
from mcp.server.mcpserver import MCPServer

import cost_tools

server = MCPServer("cost-tools")


@server.tool()
def lookup_price(service: str, size: str) -> float:
    """Return the monthly price in USD for a cloud service and size.

    service: vm, postgres or storage. size: small, medium, large or 100gb.
    """
    return cost_tools.lookup_price(service, size)


@server.tool()
def sum_costs(items: list[dict]) -> float:
    """Add up monthly costs. Each item has name, unit_price (USD) and quantity."""
    return cost_tools.sum_costs(items)


@server.tool()
def convert_currency(amount: float, from_cur: str, to_cur: str) -> float:
    """Convert an amount between USD, EUR and CUR."""
    return cost_tools.convert_currency(amount, from_cur, to_cur)


@server.resource("prices://all")
def all_prices() -> str:
    """The full price list as CSV text."""
    return cost_tools.PRICES_FILE.read_text()


if __name__ == "__main__":
    server.run()
