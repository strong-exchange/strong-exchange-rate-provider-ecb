from collections import defaultdict


rates: dict[str, str] = {}
latest_daily_rate_for: str | None = None


# ToDo: check memory consumption
# Date:
#     symbol: value
history_data = defaultdict(dict)
