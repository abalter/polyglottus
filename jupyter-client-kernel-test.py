import jupyter_client
from sys import argv

def run_code(client, code):
    # now we can run code.  This is done on the shell channel
    print()
    print("running:")
    print(code)

    # execution is immediate and async, returning a UUID
    msg_id = client.execute(code)
    # get_msg can block for a reply
    reply = client.get_shell_msg(msg_id)

    status = reply['content']['status']
    
    if status == 'ok':
        print('succeeded!')
    elif status == 'error':
        print('failed!')
        for line in reply['content']['traceback']:
            print(line)

if __name__ == "__main__":

    id = argv[1]

    print("creating a connection to connection file " + id)

    cf=jupyter_client.find_connection_file(id)
    print("the connection file is " + cf)

    bkc=jupyter_client.BlockingKernelClient(connection_file=cf)
    bkc.load_connection_file()

    commands = \
    [
        'a=5',
        'b=0',
        'print()',
        'b',
        'print()',
        'print("hello there")',
        'print(a*10)',
        'c=1/b'
    ]

    for command in commands:
        out = bkc.execute_interactive(code=command)
#        run_code(bkc, comman)

