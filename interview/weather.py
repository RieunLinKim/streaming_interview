from typing import Any, Iterable, Generator
from collections import deque

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    responses = deque()
    for line in events:
        if set(line.keys()) == {"type", "stationName", "timestamp", "temperature"}: # sample message
            responses.append(line)
                
        elif set(line.keys()) == {"type", "command"}:   # control message
        


        yield line
