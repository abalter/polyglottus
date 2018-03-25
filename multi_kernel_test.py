import sys
import queue
from jupyter_client.manager import start_new_kernel


def startKernel(kernel_name):
    return start_new_kernel(kernel_name=kernel_name)


def executeCommand(client, command):

    ### Execute the code
    client.execute(command)

    ### Get the execution status
    ### When the execution state is "idle" it is complete
    io_msg = client.get_iopub_msg(timeout=1)
    io_msg_content = io_msg['content']
    ### We're going to catch this here before we start polling
    if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
        return "no output"

    out = ""

    ### Continue polling for execution to complete
    ### which is indicated by having an execution state of "idle"
    while True:
        ### Save the last message content. This will hold the solution.
        ### The next one has the idle execution state indicating the execution
        ###is complete, but not the stdout output

        ### Poll the message
        try:
#            print("in try")
            io_msg = client.get_iopub_msg(timeout=1)
            io_msg_content = io_msg['content']
#            print("io_msg_content: " + str(io_msg_content))
            if (
                    'execution_state' in io_msg_content
                    and io_msg_content['execution_state'] == 'idle'
                ):
#                print("idle --> break")
                break
        except queue.Empty:
            print("timeout get_iopub_msg")
            break

        ### Check the message for various possibilities
        if 'data' in io_msg_content: # Indicates completed operation
#            print("has data")
            out = io_msg_content['data']['text/plain']
        elif 'name' in io_msg_content and io_msg_content['name'] == "stdout": # indicates output
#            print("has name")
            out += io_msg_content['text']
        elif 'traceback' in io_msg_content: # Indicates error
            print("ERROR")
            out = '\n'.join(io_msg_content['traceback']) # Put error into nice format
        else:
            pass
#            out = ''

#        print("out: " + out)

    return out



python_commands = \
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
    'c=1/b',
    'd = {"a":1,"b":"Two","c":[1,2,3]}',
    'd',
    'import json',
    'j = json.loads(str(d).replace(\"\\\'\",\"\\"\"))',
    'j',
    'import pandas as pd',
    ('df = pd.DataFrame({'
                   '"A": [4, 3, 5, 2, 1, 7, 7, 5, 9],'
                   '"B": [0, 4, 3, 6, 7, 10, 11, 9, 13],'
                   '"C": [1, 2, 3, 1, 2, 3, 1, 2, 3],'
                   '"D": [8, 3, 0, 15, 15, -1, 10, 7, 10]'
                   '})'
    ),
    'df',
    'df.describe()',
    'df["A"].mean()',
    'df.to_csv("data.txt", index=False)'
]

r_commands = \
[
    'a<-5',
    'b<-0',
    'rnorm(5)',
    'b',
    'summary(cars)',
    'y=c(12,15,28,17,18)',
    'x=c(22,39,50,25,18)',
    'mean(y)',
    'mean(x)',
    'print("hello there")',
    'print(a*10)',
    'print(with(PlantGrowth, tapply(weight, group, mean)))',
    'with(PlantGrowth, aov(weight ~ group)) -> aov.out',
    'print(summary.aov(aov.out))',
    'print(summary.lm(aov.out))'
]


bash_commands = \
[
    'ls -al',
    'pwd',
    'echo $(pwd)',
    'echo "hello" | sed \'s/el/99/\'',
    'a=10',
    'echo $a',
    'cat data.txt',
    'awk  \'{FS=","; OFS="\\t";} NR==1{print "A","D","E"} NR>1 && NR%2==0{print $1,$4,($2*$3)}\' data.txt',
    'awk  \'{FS=","; OFS="\\t";} NR==1{print "A","D","E"} NR>1 && NR%2==0{print $1,$4,($2*$3)}\' data.txt > new_data.txt',
    'cat new_data.txt',
    'head -4 new_data.txt'
]



kernel_data = \
{
 'bash': {'kernel_name': 'bash', 'commands': bash_commands},
 'python': {'kernel_name': 'python', 'commands': python_commands},
 'R' : {'kernel_name': 'ir', 'commands': r_commands}
}


def run(language):
    print("running with " + language)
    kernel = kernel_data[language]['kernel_name']
    commands = kernel_data[language]['commands']

    manager, client = startKernel(kernel)

    for command in commands:
        print(">>>" + command)
        out = executeCommand(client, command)
        print(out)

    manager.shutdown_kernel()

#un('bash')


"""
language = 'bash'
kernel = kernel_data[language]['kernel_name']
commands = kernel_data[language]['commands']

manager, client = startKernel(kernel)

for command in commands:
    print(">>>" + command)
    out = executeCommand(client, command)
    print(out)

"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        language = sys.argv[1]
    else:
        language = 'python'

    run(language)

