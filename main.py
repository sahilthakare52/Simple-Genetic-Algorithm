import os
import itertools
import time
startTime = time.time()

print ( "Gathering the system resource information........\n ==============#################===============" )

os.system("rm  Next_iteration*.txt >/dev/null 2>&1")

data = os.system(" echo '' > mydata.txt; for i in `cat servers.txt`;do ssh -o StrictHostKeyChecking=no ubuntu@$i 'hostname && sudo sh /etc/update-motd.d/50-landscape-sysinfo' ; echo '====='; done | tee mydata.txt ")

print(" Fetching the current memory utilisation..........\n")

print("==============#################===============")

os.system("cat mydata.txt|grep Memory")

print("==============#################===============")


print("==============#################===============")

print("Starting the algorithm, choosing the population..............\n")

os.system("cat servers.txt")

print("\n==============#################===============")

print("Iteration - 1 ................. Starting\n ")
print("First Generation - Parents...........\n")


count = len(open("servers.txt").readlines())

print("The hosts in the selected population is: {} ".format(count))

print("==============#################===============")

print("Dividing the population into tournament participants ...........\n")

os.system("cat mydata.txt | grep Memory | cut -d 'I' -f1| tee Memory.txt >/dev/null 2>&1")
os.system("cat mydata.txt | grep Memory | tee ip_add.txt >/dev/null 2>&1")

def update_next_iteration(selections, nextiteration):
        fil=open(nextiteration, "a")
        fil.write(selections + "\n")
        fil.close


def tourament_func(n, filename, updatedip, nextiteration):
    for i, j in itertools.zip_longest(range(0, count, 2), range(1,count,2)):
      if i is not None:
       with open(filename) as f:
        firstline = f.readlines()[i].rstrip()
       with open(updatedip) as f:
        firstline_ip_add = f.readlines()[i].rstrip()
      if j is not None:
       with open(filename) as f:
        secondline = f.readlines()[j].rstrip()
       with open(updatedip) as f:
        secondline_ip_add = f.readlines()[j].rstrip()
      print(firstline)
      print(secondline)

      print ("======================")

      print ("Running tournament --> iteration {}".format(n))
      print ("Applying Crossover and selecting new child from available parents.......")
      if firstline>secondline:
          print("Memory  utilisation for server {} is greater than server {}\n Server {} is selected".format(i, j, j))
          update_next_iteration(secondline_ip_add, nextiteration)
      elif firstline<secondline:
          print("Memory  utilisation for server {} is less than server {}\n Server {} is Selected ".format(i, j, i))
          update_next_iteration(firstline_ip_add, nextiteration)
      else:
          print("Memory  utilisation for server {} is equal to server {}\n Server will be selected randomly".format(i, j))
          update_next_iteration(firstline_ip_add, nextiteration)
      print ("==========================================")
 
tourament_func(1, "Memory.txt", "ip_add.txt", "Next_iteration1.txt")

print ("Selected servers for next iteration")
os.system("cat Next_iteration1.txt")

print ("==========================================")

print ("Starting Next iteration..........")

count = len(open("Next_iteration1.txt").readlines())

tourament_func(2, "Next_iteration1.txt", "Next_iteration1.txt", "Next_iteration2.txt")

print ("Selected servers for next iteration")
os.system("cat Next_iteration2.txt")

print ("==========================================")

print ("Starting Next iteration..........")

count = len(open("Next_iteration2.txt").readlines())

tourament_func(3, "Next_iteration2.txt", "Next_iteration2.txt", "Next_iteration3.txt")

print ("Selected servers for next iteration")
os.system("cat Next_iteration3.txt")

print ("==========================================")

print ("Starting Next iteration..........")

count = len(open("Next_iteration3.txt").readlines())

tourament_func(4, "Next_iteration3.txt", "Next_iteration3.txt", "Next_iteration4.txt")

print ("selected server.........")


print("####################################\n#######Final-selected-server################")
os.system("cat Next_iteration4.txt")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
