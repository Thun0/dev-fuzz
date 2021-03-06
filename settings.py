# TODO: move config to file and create parser
config = {
    "verbose": False,
    "debug": True,

    "mutator": {
        "max_mutated_bytes": 0.01,
        "max_flipped_bits": 0.05
    },

    "projects_dir": "projects/",
    "corpuses_dir": "corpuses/",
    "adb_port": 5037,
    "devices_start_port": 57001,
    "agent_path": "agent/bin/agent"
}
