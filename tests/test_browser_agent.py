import asyncio

import pytest

from ollama_config import BrowserAgent, BrowserAgentConfig
from browser_use import Agent, BrowserSession
from langchain_ollama import ChatOllama


class DummyAgent(Agent):
    """Agent that returns a fixed history."""

    async def run(self):
        return ["done"]


def test_create_agent_initializes(browser_config):
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    assert isinstance(agent.llm, ChatOllama)
    assert isinstance(agent.browser_session, BrowserSession)
    assert agent.browser_session.is_connected()
    asyncio.run(agent.close())


def test_run_task_success(monkeypatch, browser_config):
    monkeypatch.setattr("ollama_config.Agent", DummyAgent)
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    result = asyncio.run(agent.run_task("test"))
    assert result == ["done"]
    asyncio.run(agent.close())


def test_run_task_retry(monkeypatch, browser_config):
    calls = {}

    class FailingAgent(Agent):
        async def run(self):
            calls.setdefault("count", 0)
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("fail")
            return ["ok"]

    monkeypatch.setattr("ollama_config.Agent", FailingAgent)
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    result = asyncio.run(agent.run_task("retry"))
    assert result == ["ok"]
    assert calls["count"] == 2
    asyncio.run(agent.close())


def test_close_stops_session(browser_config):
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    assert agent.browser_session.is_connected()
    asyncio.run(agent.close())
    assert agent.browser_session is None


def test_run_task_reconnect(monkeypatch, browser_config):
    monkeypatch.setattr("ollama_config.Agent", DummyAgent)
    agent = BrowserAgent(browser_config)
    asyncio.run(agent.create_agent())
    # Simulate lost connection
    asyncio.run(agent.browser_session.stop())
    assert not agent.browser_session.is_connected()

    calls = {"count": 0}
    original_create = agent.create_agent

    async def wrapped():
        calls["count"] += 1
        await original_create()

    monkeypatch.setattr(agent, "create_agent", wrapped)
    result = asyncio.run(agent.run_task("reconnect"))
    assert result == ["done"]
    assert calls["count"] == 1
    asyncio.run(agent.close())
