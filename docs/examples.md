# Example Task Templates

This repository includes several pre-built task templates organized by category. These templates can be used with `TaskExecutor` to automate common workflows.

## Categories
- **research** – tasks focused on knowledge gathering and summarization
- **data collection** – scraping or extracting information from the web
- **e-commerce** – price comparison and shopping utilities
- **social media** – monitoring platforms for specific mentions

## News Summarization
`examples/news_summarization.py` demonstrates summarizing recent news on a given topic.

**Expected output** (truncated):
```
Status: success
History: ['handled Summarize the latest news about ...']
```

## Price Comparison
`examples/price_comparison.py` launches a task to compare prices for a product.

**Expected output** (truncated):
```
Status: success
History: ['handled Compare prices for ...']
```

## Social Media Monitoring
`examples/social_media_monitoring.py` monitors social media for a keyword.

**Expected output** (truncated):
```
Status: success
History: ['handled Monitor social media ...']
```

## Error Handling
`examples/error_handling.py` shows how to catch exceptions and inspect the task result for failures.

## Performance Patterns
`examples/performance_patterns.py` runs multiple tasks concurrently using `asyncio.gather` to maximize throughput.

