import asyncio
import pytest

from ollama_config import BrowserAgent, BrowserAgentConfig


@pytest.fixture(params=[True, False])
def browser_config(request):
    """Return BrowserAgentConfig with different headless modes."""
    return BrowserAgentConfig(headless=request.param)


@pytest.fixture
def browser_agent(browser_config):
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    yield agent
    asyncio.run(agent.close())
