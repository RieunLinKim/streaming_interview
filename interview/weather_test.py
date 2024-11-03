from . import weather

def test_empty_input():
    assert not list(weather.process_events([]))

def test_regular_input():   # expected sample and control messages
    sample_message1 = {
                    "type": "sample",
                    "stationName": "Foster Weather Station",
                    "timestamp": 1672531199999,
                    "temperature": 37.1
                    }

    sample_message2 = {
                    "type": "sample",
                    "stationName": "Foster Weather Station",
                    "timestamp": 1672531200000,
                    "temperature": 32.5
                    }

    snapshot_message1 = {
                        "type": "control", 
                        "command": "snapshot"
                        }

    snapshot_output1 = {
                        "type": "snapshot",
                        "asOf": 1672531200000,
                        "stations": {
                                    "Foster Weather Station": {"high": 37.1, "low": 32.5}
                                    }
                        }

    reset_message = {
                    "type": "control", 
                    "command": "reset"
                    }

    reset_output = {
                    "type": "reset",
                    "asOf": 1672531200000
                    }

    sample_message3 = {
                "type": "sample",
                "stationName": "Foster Weather Station",
                "timestamp": 1672531200001,
                "temperature": 39
                }

    snapshot_message2 = {
                        "type": "control", 
                        "command": "snapshot"
                        }

    snapshot_output2 = {
                        "type": "snapshot",
                        "asOf": 1672531200001,
                        "stations": {
                                    "Foster Weather Station": {"high": 39, "low": 39}
                                    }
                        }

    test_input = [sample_message1,
                sample_message2,
                snapshot_message1,
                reset_message,
                sample_message3,
                snapshot_message2]

    assert [snapshot_output1, reset_output, snapshot_output2] \
            == list(weather.process_events(test_input))

def test_unknown_message():
    try:
        weather.process_events([{}])
    except ValueError as e:
        print(f"The unknown message error was successfully caught: {e}")
