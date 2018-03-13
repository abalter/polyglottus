from jupyter_client import KernelManager
import queue
from jupyter_client.manager import run_kernel
from jupyter_client.manager import start_new_kernel


class MyKernel():
    def __init__(self):
        self.kernel_manager, self.client = start_new_kernel()
        self.client.start_channels
        #self.client.wait_for_ready()

    def run_code(self, code):
        print("----------------")
        print("executing code: " + code)

        msg_id = self.client.execute(code)
        reply = self.client.get_shell_msg(msg_id)
        #print("printing reply content")
        #print(reply['content'])
        #print()

        while True:
            try:
                io_msg = self.client.get_iopub_msg(timeout=1)
                print("io_msg content")
                print(io_msg['content'])
            except queue.Empty:
                print('timeout get_iopub_msg')
                break

        print("----------------\n\n")

    def __del__(self):
        self.kernel_manager.shutdown_kernel()
