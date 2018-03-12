from jupyter_client import KernelManager
km = KernelManager()
km.start_kernel()
kc = km.client()

msg_id = kc.execute("2+2")
reply = kc.get_shell_msg(msg_id)
print(reply)
