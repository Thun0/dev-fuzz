# TODO: move config to file and create parser
config = {
    "verbose": False,
    "debug": True,

    "vm_manager": {
        "hypervisor_uri": "qemu:///system"
    },

    "mutator": {
        "max_mutated_bytes": 0.01
    },

    "receiver": {
        "port" : 31337
    },

    "corpus": {
        "dir_path" : "corpus/"
    },

    "projects_dir": "projects/",
    "project": "",
    "adb_port": 5037
}
