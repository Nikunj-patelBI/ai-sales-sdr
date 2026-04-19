"""Base agent class implementing the ReAct pattern with MCP tool access."""
from __future__ import annotations

import structlog
from anthropic import Anthropic

log = structlog.get_logger(__name__)


class BaseAgent:
    """ReAct agent: reason -> act -> observe -> repeat until goal is achieved."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        model: str = "claude-sonnet-4-6",
        max_iterations: int = 20,
    ) -> None:
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.max_iterations = max_iterations
        self.client = Anthropic()
        self.tools: list[dict] = []
        self.history: list[dict] = []

    def register_tools(self, tools: list[dict]) -> None:
        """Register MCP-provided tool schemas the agent can call."""
        self.tools = tools

    async def execute_tool(self, tool_use) -> str:
        """Execute a tool call. Subclasses wire this to actual MCP servers."""
        raise NotImplementedError

    async def run(self, goal: str) -> dict:
        """Run the agent loop until the goal is achieved or max_iterations hit."""
        messages: list[dict] = [{"role": "user", "content": goal}]

        for iteration in range(self.max_iterations):
            log.info("agent_iteration", agent=self.name, iteration=iteration)

            response = self.client.messages.create(
                model=self.model,
                system=self.system_prompt,
                messages=messages,
                tools=self.tools,
                max_tokens=4096,
            )

            if response.stop_reason == "end_turn":
                return {"status": "done", "iterations": iteration, "result": response}

            tool_results = []
            for block in response.content:
                if getattr(block, "type", None) == "tool_use":
                    result = await self.execute_tool(block)
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result}
                    )

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        return {"status": "max_iterations", "iterations": self.max_iterations}
