from jupyter_client import KernelManager
import queue
from jupyter_client.manager import run_kernel

class MyKernel():
    def __init__():
        kernel = KernelManager()
        kernel.start_kernel()
        client =  = km.client()

    def run_code(self, code):
        print("executing code: " + code)

        with run_kernel() as kc:
            msg_id = kc.execute("print(1+2)")
            reply = kc.get_shell_msg(msg_id)
            print(reply['content'])
            print()

            while True:
                try:
                    io_msg = kc.get_iopub_msg(timeout=1)
                    print(io_msg['content'])
                except queue.Empty:
                    print('timeout kc.get_iopub_msg')
                    break
