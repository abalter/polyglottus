import jupyter_client
from jupyter_client import KernelManager

from sys import argv

def run_cmd(kc, cmd):

    kc.execute(cmd)

    while True:
        try:
            kc_msg = kc.get_iopub_msg(timeout=1)
            if 'content' in kc_msg and 'data' in kc_msg['content']:
                print('the kernel produced data {}'.format(kc_msg['content']['data']))
            break        
        except:
            print('timeout kc.get_iopub_msg')
            pass


if __name__ == "__main__":


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


    km = KernelManager()
    km.start_kernel()
    kc = km.client()
    
    for command in commands:
        run_cmd(kc, command)
