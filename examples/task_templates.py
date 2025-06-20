from dataclasses import dataclass
from typing import Dict

@dataclass
class TaskTemplate:
    """Simple representation of a task template."""
    description: str
    category: str


task_templates: Dict[str, Dict[str, TaskTemplate]] = {
    "research": {
        "news_summarization": TaskTemplate(
            description="Summarize the latest news about '{topic}' from multiple sources.",
            category="research",
        ),
    },
    "data_collection": {
        "data_scrape": TaskTemplate(
            description="Collect data related to '{query}' from '{website}'.",
            category="data_collection",
        ),
    },
    "e-commerce": {
        "price_comparison": TaskTemplate(
            description="Compare prices for '{product}' across popular e-commerce sites.",
            category="e-commerce",
        ),
    },
    "social_media": {
        "monitoring": TaskTemplate(
            description="Monitor social media for posts mentioning '{keyword}' and summarize insights.",
            category="social_media",
        ),
    },
}


