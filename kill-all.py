import os 
import subprocess as ps
top_info = ps.Popen(["top", "-n", "1"], stdout=ps.PIPE)
out, err = top_info.communicate()
out = out.decode("unicode-escape")
out = out.split("\n")[7:]

for line in out:
    line = line.split()
    if line[2] == "root":
        continue
    if line[-2] == "python3" or line[-2] == "sh":
        print("kill process : {}".format(line[1]))
        os.system("kill -9 {}".format(line[1]))
    
    
