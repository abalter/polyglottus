from my_kernel import MyKernel

kernel = MyKernel()

kernel.run_code('1+1')
kernel.run_code('1+1')
kernel.run_code('a=10')
kernel.run_code('a')
kernel.run_code('b=5')
kernel.run_code('print("hello there")')
kernel.run_code('a*b')
kernel.run_code('print(a+b)')
