from typing import Any, Iterable, Generator, Dict

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    record: Dict[str, Any] = {}
    curr_timestamp = None

    for line in events:
        message_type = line["type"]
        if message_type == "sample": # sample message
            station_name = line["stationName"]
            timestamp = line["timestamp"]
            temperature = line["temperature"]

            if curr_timestamp is None or timestamp > curr_timestamp:
                # record for new/later timestamp
                curr_timestamp = timestamp

            if station_name not in record:   # first record of the station
                record[station_name] = {}
                record[station_name]["high"] = line["temperature"]
                record[station_name]["low"] = line["temperature"]

            else : # station record already exists
                if temperature > record[station_name]["high"] :
                    record[station_name]["high"] = temperature # new high temperature
                elif temperature < record[station_name]["low"] :
                    record[station_name]["low"] = temperature  # new low temperature

        elif message_type == "control":   # control message
            if not record or curr_timestamp is None: # no existing record
                continue    # ignore

            output = {}
            output["type"] = line["command"]
            output["asOf"] = curr_timestamp

            if line["command"] == "snapshot":   # control message type 1 : snapshot
                output["stations"] = record.copy()

            elif line["command"] == "reset":  # control message type 2 : reset
                record = {}

            yield output

        else:
            raise ValueError(f"input: {message_type} is an unknown message type")
