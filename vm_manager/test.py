from vm_manager.manager import Manager


def test1():
    m = Manager()
    m.connect_to_machine("localhost", 1234)
    data = "hello network"
    m.send_data_to(data.encode(), 0)
    m.dispose()


test1()
