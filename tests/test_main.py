
from bitcli.main import BitCLITest

def test_bitcli(tmp):
    with BitCLITest() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with BitCLITest(argv=argv) as app:
        app.run()
