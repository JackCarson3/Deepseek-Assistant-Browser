import logging
from dataclasses import dataclass, field
from typing import Any, Optional, Tuple

from browser_use import Agent, BrowserProfile, BrowserSession
from browser_use.logging_config import setup_logging
from langchain_ollama import ChatOllama


@dataclass
class BrowserAgentConfig:
    """Configuration for :class:`BrowserAgent`.

    Parameters correspond to ``browser_use`` and Ollama options.
    """

    model_name: str = "deepseek"  # default model
    ollama_url: str = "http://localhost:11434"  # local ollama server
    temperature: float = 0.2
    headless: bool = True
    viewport: Optional[Tuple[int, int]] = None
    disable_security: bool = False
    deterministic_rendering: bool = False
    browser_args: list[str] = field(default_factory=list)
    browser_options: dict[str, Any] = field(default_factory=dict)
    retries: int = 1


class BrowserAgent:
    """Wrapper around ``browser_use.Agent`` using an Ollama LLM.

    The agent orchestrates a language model and a browser session to carry out
    complex tasks expressed in natural language.
    """

    def __init__(self, config: Optional[BrowserAgentConfig] = None) -> None:
        self.config = config or BrowserAgentConfig()
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm: Optional[ChatOllama] = None
        self.browser_session: Optional[BrowserSession] = None

    async def _cleanup_session(self) -> None:
        if self.browser_session is not None:
            try:
                await self.browser_session.kill()
                self.logger.info("Browser session terminated")
            except Exception as exc:
                self.logger.warning("Error terminating browser session: %s", exc)
            finally:
                self.browser_session = None

    def _build_profile(self) -> BrowserProfile:
        viewport = (
            {"width": self.config.viewport[0], "height": self.config.viewport[1]}
            if self.config.viewport
            else None
        )
        profile = BrowserProfile(
            headless=self.config.headless,
            viewport=viewport,
            disable_security=self.config.disable_security,
            deterministic_rendering=self.config.deterministic_rendering,
            args=self.config.browser_args,
            **self.config.browser_options,
            stealth=True,
        )
        return profile

    async def create_agent(self) -> None:
        """Initialize the LLM and browser session.

        This method sets up ``ChatOllama`` and launches a ``BrowserSession``
        according to :class:`BrowserAgentConfig`.
        """
        try:
            self.logger.info("Creating ChatOllama with model %s", self.config.model_name)
            self.llm = ChatOllama(
                model=self.config.model_name,
                base_url=self.config.ollama_url,
                temperature=self.config.temperature,
            )

            profile = self._build_profile()
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
        """Run a task description through the agent with retry support.

        Parameters
        ----------
        task_description:
            Natural language instruction to execute in the browser.

        Returns
        -------
        list
            Interaction history returned by ``browser_use.Agent``.
        """
        attempts = 0
        while attempts <= self.config.retries:
            if self.browser_session is None or self.llm is None or not self.browser_session.is_connected():
                await self._cleanup_session()
                await self.create_agent()
            assert self.browser_session is not None and self.llm is not None
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser_session=self.browser_session,
            )
            try:
                self.logger.info("Running task: %s (attempt %s)", task_description, attempts + 1)
                history = await agent.run()
                self.logger.info("Task finished")
                return history
            except Exception as exc:
                attempts += 1
                self.logger.exception("Agent run failed: %s", exc)
                await self._cleanup_session()
                if attempts > self.config.retries:
                    raise
                self.logger.info("Retrying task...")

    async def close(self) -> None:
        """Close the browser session and clean up."""
        if self.browser_session is not None:
            try:
                await self.browser_session.stop()
                self.logger.info("Browser session closed")
            except Exception as exc:
                self.logger.warning("Error closing browser session: %s", exc)
            finally:
                await self._cleanup_session()

    async def __aenter__(self) -> "BrowserAgent":
        """Context manager entry, calls :meth:`create_agent`."""
        await self.create_agent()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Context manager exit, ensuring resources are released."""
        await self.close()

