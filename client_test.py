import queue
from jupyter_client.manager import start_new_kernel

kernel_manager, client = start_new_kernel()


def runCode(code):

    ### Execute the code
    client.execute(code)

    ### Get the execution status
    ### When the execution state is "idle" it is complete
    io_msg = client.get_iopub_msg(timeout=1)
    io_msg_content = io_msg['content']
    ### We're going to catch this here before we start polling
    if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
        return "no output"

    ### Continue polling for execution to complete
    ### which is indicated by having an execution state of "idle"
    while True:
        ### Save the last message content. This will hold the solution.
        ### The next one has the idle execution state indicating the execution
        ###is complete, but not the stdout output
        temp = io_msg_content

        ### Poll the message
        try:
            io_msg = client.get_iopub_msg(timeout=1)
            io_msg_content = io_msg['content']
            if (
                    'execution_state' in io_msg_content
                    and io_msg_content['execution_state'] == 'idle'
                ):
                break
        except queue.Empty:
            print("timeout get_iopub_msg")
            break

    ### Check the message for various possibilities
    if 'data' in temp: # Indicates completed operation
        out = temp['data']['text/plain']
    elif 'name' in temp and temp['name'] == "stdout": # indicates output
        out = temp['text']
    elif 'traceback' in temp: # Indicates error
        print("ERROR")
        out = '\n'.join(temp['traceback']) # Put error into nice format
    else:
        out = ''

    return out



commands = \
[
    '!pwd',
    '!echo "hello"',
    '!ls',
    '1+1',
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
    print(">>>" + command)
    out = runCode(command)
    print(out)


"""
>>>!pwd

>>>!echo "hello"
"hello"

>>>!ls

>>>1+1
2
>>>a=5

>>>b=0

>>>print()


>>>b
0
>>>print()


>>>print("hello there")
hello there

>>>print(a*10)
50

>>>c=1/b
ERROR
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-12-47a519732db5> in <module>()
----> 1 c=1/b

ZeroDivisionError: division by zero
"""