from jupyter_client import KernelManager
import queue
from jupyter_client.manager import run_kernel
from jupyter_client.manager import start_new_kernel
from pprint import PrettyPrint


class SimpleKernel():
    """
    ## Description
    **SimpleKernel**:
     A simplistic Jupyter kernel client wrapper.

    Additional information in [this GitHub issue]
    (

    )
    """

    def __init__(self):
        """
        ## Description
        Initializes the `kernel_manager` and `client` objects
        and starts the kernel. Also initializes the pretty printer
        for displaying object properties and execution result
        payloads.

        ## Parameters
        None.
        """
        self.kernel_manager, self.client = start_new_kernel()
        ### Initialize the channel. Otherwise first execution request is
        ### not run.
        self.client.start_channels()
        #self.client.wait_for_ready()

        ### Initialize pretty printer
        self.pp = PrettyPrint(indent=2)

    def execute(self, code, verbose=False, full=False):
        """
        ## Description
        **execute**:
        Executes a code string in the kernel. Can return either
        the full execution response payload, or just `stdout`. Also,
        there is a verbose mode that displays the execution process.

        ## Parameters
        code : string
            The code string to get passed to `stdin`.
        verbose : bool (default=False)
            Whether to display processing information.
        full : bool (default False)
            Whether to return the full response payload,
            or just `stdout`.

        ## Returns
        `stdout` or the full response payload.
        """
        if verbose:
            print("----------------")
            print("executing code: " + code)

        ### Execute the code
        msg_id = self.client.execute(code)
        ### Collect the response payload
        reply = self.client.get_shell_msg(msg_id)

        ### Continue polling for execution to complete
        while True:
            try:
                io_msg = self.client.get_iopub_msg(timeout=1)
                if verbose:
                    print("io_msg content")
                    print(io_msg['content'])
            except queue.Empty:
                if verbose:
                    print('timeout get_iopub_msg')
                break

        if verbose:
            print("----------------\n\n")

        if full:
            return reply
        else:
            return reply['content']

    def showManager(self):
        """
        ## Description
        **showManager**:
        Pretty Print kernel manager object.
        """

        self.pp(self.kernel_manager)

    def showClient(self):
        """
        ## Description
        **showClient**:
        Pretty Print client object.
        """

        self.pp(self.client)

    def prettyPrint(self, payload):
        """
        ## Description
        **prettyPrint**:
        A convenience method to pretty print the reply payload.

        ## example
        ```
        >>> reply = my_kernel.execute("1+1")
        >>> my_kernel.prettyPrint(reply)
        ```

    def __del__(self):
        """
        ## Description
        **__del__**:
        Destructor. Shuts down kernel safely.
        """
        self.kernel_manager.shutdown_kernel()
