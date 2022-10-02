import os
import sys

# get path to default docker file
proto_yml = os.environ['DOCKER_YML']


# get args
args = sys.argv
args.pop(0)
    
command = args[0]
print("command is " + command)
args.pop(0)
args = ["      " + command] + args
#read the dockerfile prototype
f =  open(proto_yml)
headstring = f.read()
f.close()

yml_head = headstring +  "    command: >\n"

yml_tail = '*'.join(' '.join(args).split('--'))
yml_tail = '\n      -'.join(' '.join(args).split(' -'))
yml_tail = '\n      --'.join(' '.join(args).split('*'))

#generate the docker file
if os.path.exists("./docker-compose.yml"):
    os.remove("./docker-compose.yml")

fout = open("docker-compose.yml", 'w')
fout.write(yml_head)
fout.write(yml_tail)
fout.close()


