import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

"""Testing utilities and stub modules for optional dependencies."""

import types

if "browser_use" not in sys.modules:
    browser_use = types.ModuleType("browser_use")

    class BrowserProfile:  # type: ignore
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class BrowserSession:  # type: ignore
        def __init__(self, browser_profile=None):
            self.browser_profile = browser_profile
            self._connected = False

        async def start(self):
            self._connected = True

        async def stop(self):
            self._connected = False

        async def kill(self):
            self._connected = False

        def is_connected(self) -> bool:
            return self._connected

    class Agent:  # type: ignore
        def __init__(self, task, llm=None, browser_session=None):
            self.task = task
            self.llm = llm
            self.browser_session = browser_session

        async def run(self):
            return [f"handled {self.task}"]

    logging_config = types.ModuleType("browser_use.logging_config")

    def setup_logging():
        pass

    logging_config.setup_logging = setup_logging

    browser_use.Agent = Agent
    browser_use.BrowserProfile = BrowserProfile
    browser_use.BrowserSession = BrowserSession
    browser_use.logging_config = logging_config

    sys.modules["browser_use"] = browser_use
    sys.modules["browser_use.logging_config"] = logging_config

if "langchain_ollama" not in sys.modules:
    langchain_ollama = types.ModuleType("langchain_ollama")

    class ChatOllama:  # type: ignore
        def __init__(self, model: str, base_url: str, temperature: float):
            self.model = model
            self.base_url = base_url
            self.temperature = temperature

    langchain_ollama.ChatOllama = ChatOllama
    sys.modules["langchain_ollama"] = langchain_ollama

