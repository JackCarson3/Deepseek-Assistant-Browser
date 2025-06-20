import asyncio

from ollama_config import BrowserAgent, BrowserAgentConfig


def test_chatollama_parameters(monkeypatch):
    created = {}

    def fake_init(self, model, base_url, temperature):
        created["model"] = model
        created["base_url"] = base_url
        created["temperature"] = temperature

    monkeypatch.setattr(
        "langchain_ollama.ChatOllama.__init__",
        fake_init,
        raising=False,
    )

    config = BrowserAgentConfig(
        model_name="foo", ollama_url="http://bar", temperature=0.5
    )
    agent = BrowserAgent(config)
    asyncio.run(agent.create_agent())
    assert created == {
        "model": "foo",
        "base_url": "http://bar",
        "temperature": 0.5,
    }
    asyncio.run(agent.close())
