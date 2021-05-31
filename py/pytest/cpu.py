#! python3.4
# @ guliping
import psutil

def getProcByCmdline(name):
    # attrs = ['pid', 'memory_percent', 'name', 'cpu_times', 'create_time','memory_info']
    procRet = None
    attrs = ['pid', 'memory_percent', 'name',
             'cpu_times', 'memory_info', 'cmdline']
    for proc in psutil.process_iter(attrs=attrs):
        # print(proc.info)
        # print(proc)
        try:
            cmdline = proc.cmdline()
            # print(cmdline)
            if cmdline and len(cmdline) > 0 and cmdline[0] == name:
                procRet = proc
                # procRet = psutil.Process(proc.pid)
                # print(procRet == proc)
                break
        except psutil.AccessDenied as e:
            print(e)
            pass
    return procRet

if __name__ == '__main__':
    text = ""
    names = ["/opt/fish/skynet/skynet"]
    procs = []
    for i in range(len(names)):
        procs.append(getProcByCmdline(names[i]))

    cpu = psutil.cpu_percent(interval=1, percpu=True)
    cpu2 = psutil.cpu_percent(interval=1, percpu=False)
    # 测试发现简单所有的cpu没有的，要检查主要的程序的cpu
    print("*"*60)
    print("cpu=", cpu,"cpu2=",cpu2, "cpucnt=", psutil.cpu_count())

    # 检查单个cpu运行状况
    for i in range(len(procs)):
        if procs[i] :
            exeCpu = procs[i].cpu_percent(0.5)
            print("cpu["+names[i]+"]="+str(exeCpu)+"\n")

    print(text)