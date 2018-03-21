from jupyter_client import KernelManager
km = KernelManager()
km.start_kernel()
kc = km.client()
# now execute something in the client
#msg_id = kc.execute("2+2")
#reply = kc.get_shell_msg(msg_id)

def run_code(kc, code):
    kc.execute(code)

    while True:
        try:
            kc_msg = kc.get_iopub_msg(timeout=1)
            if 'content' in kc_msg and 'data' in kc_msg['content']:
                print('the kernel produced data {}'.format(kc_msg['content']['data']))
                break
        except:
            print('timeout kc.get_iopub_msg')
            pass


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

run_code(kc, "1+1")

#for command in commands:
#    run_code(kc,command)
