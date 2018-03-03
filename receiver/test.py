import receiver


def test1():
    r = receiver.Receiver(1234)
    data = r.test_receive()
    print(data.decode())


test1()
