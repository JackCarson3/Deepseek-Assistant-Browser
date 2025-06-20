import logging
from dataclasses import dataclass
from typing import Optional

from browser_use import Agent, BrowserProfile, BrowserSession
from browser_use.logging_config import setup_logging
from langchain_ollama import ChatOllama


@dataclass
class BrowserAgentConfig:
    """Configuration for :class:`BrowserAgent`."""

    model_name: str = "deepseek"  # default model
    ollama_url: str = "http://localhost:11434"  # local ollama server
    temperature: float = 0.2
    headless: bool = True


class BrowserAgent:
    """Wrapper around ``browser_use.Agent`` using an Ollama LLM."""

    def __init__(self, config: Optional[BrowserAgentConfig] = None) -> None:
        self.config = config or BrowserAgentConfig()
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm: Optional[ChatOllama] = None
        self.browser_session: Optional[BrowserSession] = None

    async def create_agent(self) -> None:
        """Initialize the LLM and browser session."""
        try:
            self.logger.info("Creating ChatOllama with model %s", self.config.model_name)
            self.llm = ChatOllama(
                model=self.config.model_name,
                base_url=self.config.ollama_url,
                temperature=self.config.temperature,
            )

            profile = BrowserProfile(headless=self.config.headless, stealth=True)
            self.browser_session = BrowserSession(browser_profile=profile)
            await self.browser_session.start()
            self.logger.info(
                "Browser session started (%s)",
                "headless" if self.config.headless else "visible",
            )
        except Exception as exc:
            self.logger.exception("Failed to create agent: %s", exc)
            raise

    async def run_task(self, task_description: str):
        """Run a task description through the agent."""
        if self.browser_session is None or self.llm is None:
            await self.create_agent()
        assert self.browser_session is not None and self.llm is not None
        agent = Agent(
            task=task_description,
            llm=self.llm,
            browser_session=self.browser_session,
        )
        try:
            self.logger.info("Running task: %s", task_description)
            history = await agent.run()
            self.logger.info("Task finished")
            return history
        except Exception as exc:
            self.logger.exception("Agent run failed: %s", exc)
            raise

    async def close(self) -> None:
        """Close the browser session."""
        if self.browser_session is not None:
            try:
                await self.browser_session.close()
                self.logger.info("Browser session closed")
            except Exception as exc:
                self.logger.warning("Error closing browser session: %s", exc)
            finally:
                self.browser_session = None

