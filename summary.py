import shutil
import os
import fileinput
import re
try :
    os.mkdir('Summary')
    os.remove('result.txt')
except:
    print("Summary is existed")

outdir ='./M5OUT'
dir_list= os.listdir(outdir)
dir_list.sort()
savefile = open('result.txt',mode='w')
dramSum=0


for i in dir_list :
    num_cpu = 0
    type = ''
    if re.findall('cpu_6',i) :
        num_cpu = 6
    if re.findall('cpu_8',i)  :
        num_cpu = 8
    if re.findall('cpu_12',i)  :
        num_cpu = 12
    if re.findall('cpu_16',i)  :
        num_cpu = 16
    if re.findall('cpu_16',i)  :
        num_cpu = 24
    if re.findall('cpu_16',i)  :
        num_cpu = 32
    #print("num_cpu = ",num_cpu)

    if re.findall('type2d',i):
        type = '2d'
    if re.findall('typeg1l1',i):
        type = 'g1l1'
    if re.findall('typeg1',i):
        type = 'g1'
    if re.findall('typeg2',i):
        type = 'g2'
    if re.findall('typeg3',i):
        type = 'g3'
    if re.findall('typeg4',i):
        type = 'g4'
    if re.findall('typenoc',i):
        type = 'pp'
    #print("type = ",type)

    file_name=outdir+"/"+i+"/stats.txt"
    dst_name='Summary/'+str(i)+'.txt'

    shutil.copy(file_name,dst_name)
    file =  open(dst_name,mode='r')

    datafile = file.readlines()
    simOps=[]
    icache=[]
    dcache=[]
    l1cache=[]
    l2cache=[]
    dramRd=[]
    dramWt=[]
    simOpsSum=0
    icacheSum=0
    dcacheSum=0
    l1cacheSum=0
    l2cacheSum=0
    dramSum=0
    drampowerSum=0

    cpuClust0=[]
    cpuClust1=[]
    cpuClust2=[]
    cpuClust3=[]
    cacheClust=[]
    dir=[]
    router6=[]
    tsv0=[]
    tsv1=[]
    drampower=[]

    cpuClust0Sum=0
    cpuClust1Sum=0
    cpuClust2Sum=0
    cpuClust3Sum=0
    cacheClustSum=0
    dirSum=0
    router6Sum=0
    tsv0Sum=0
    tsv1Sum=0
    drampowerSum=0

    for line in datafile :
         if "simOps" in line :
             simOps.append(re.findall(r'\d+',re.search('simOps(.*)#',line).group(1)))
             for i in simOps:
                simOpsSum += int(i[0])
         if "Icache.m_demand_accesses" in line :
             icache.append(re.findall(r'\d+',re.search('accesses(.*)#',line).group(1)))
             for i in icache:
                icacheSum += int(i[0])
         if "Dcache.m_demand_accesses" in line :
             dcache.append(re.findall(r'\d+',re.search('accesses(.*)#',line).group(1)))
             for i in dcache:
                dcacheSum += int(i[0])
         if ".cache.m_demand_accesses" in line :
             l1cache.append(re.findall(r'\d+',re.search('accesses(.*)#',line).group(1)))
             for i in l1cache:
               l1cacheSum += int(i[0])
         if "L2cache.m_demand_accesses" in line :
            l2cache.append(re.findall(r'\d+',re.search('accesses(.*)#',line).group(1)))
            for i in l2cache:
               l2cacheSum += int(i[0])
         if "readReqs" in line :
            dramRd.append(re.findall(r'\d+',re.search('readReqs(.*)#',line).group(1)))
            for i in dramRd:
               dramSum += int(i[0])
               #print("dramSum is ",dramSum)
         if "writeReqs" in line :
            dramWt.append(re.findall(r'\d+',re.search('writeReqs(.*)#',line).group(1)))
            for i in dramWt:
               dramSum += int(i[0])
               #print("dramSum is ",dramSum)
         if "averagePower" in line :
            drampower.append(re.findall(r'\d+',re.search('averagePower(.*)#',line).group(1)))

         r6_tag ='r6_tag'
         tsv0_tag ='tsv0_tag'
         tsv1_tag ='tsv1_tag'
         ## Router Count
         start = num_cpu*2 + 4 
         dir_tag = str(start)+'.buffer_reads'
         cpu0_tag = str(start+1)+'.buffer_reads'
         cpu1_tag = str(start+2)+'.buffer_reads'
         cpu2_tag = str(start+3)+'.buffer_reads'
         cpu3_tag = str(start+4)+'.buffer_reads'
         cache_tag = str(start+5)+'.buffer_reads'

         if type == '2d' :
            r6_tag = str(start+6)+'.buffer_reads'
         elif type == 'g1' :
            tsv0_tag = str(start+6)+'.buffer_reads'
         elif type == 'g2' :
            tsv0_tag = str(start+6)+'.buffer_reads'
            tsv1_tag = str(start+7)+'.buffer_reads'
         elif type == 'g1l1' :
            tsv0_tag = str(start+6)+'.buffer_reads'
            tsv1_tag = str(start+7)+'.buffer_reads'

         if dir_tag in line :
            dir.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in dir:
               dirSum += int(i[0])
         if cpu0_tag in line :
            cpuClust0.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in cpuClust0:
               cpuClust0Sum += int(i[0])
         if cpu1_tag in line :
            cpuClust1.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in cpuClust1:
               cpuClust1Sum += int(i[0])
         if cpu2_tag in line :
            cpuClust2.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in cpuClust2:
               cpuClust2Sum += int(i[0])
         if cpu3_tag in line :
            cpuClust3.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in cpuClust3:
               cpuClust3Sum += int(i[0])
         if cache_tag in line :
            cacheClust.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in cacheClust:
               cacheClustSum += int(i[0])
         if r6_tag in line :
            router6.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in router6:
               router6Sum += int(i[0])

         if tsv0_tag in line :
            tsv0.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in tsv0:
               tsv0Sum += int(i[0])
         if tsv1_tag in line :
            tsv1.append(re.findall(r'\d+',re.search('reads(.*)\(',line).group(1)))
            for i in tsv1:
               tsv1Sum += int(i[0])

    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" Ops ")
    savefile.write(str(simOpsSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" L1I ")
    savefile.write(str(icacheSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" L1D ")
    savefile.write(str(dcacheSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" L2 ")
    savefile.write(str(l1cacheSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" L3 ")
    savefile.write(str(l2cacheSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" DRAM ")
    savefile.write(str(dramSum))
    savefile.write("\n")


    ## Router Count
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" CpuCluster0 ")
    savefile.write(str(cpuClust0Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" CpuCluster1 ")
    savefile.write(str(cpuClust1Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" CpuCluster2 ")
    savefile.write(str(cpuClust2Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" CpuCluster3 ")
    savefile.write(str(cpuClust3Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" cacheCluster ")
    savefile.write(str(cacheClustSum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" DirRouter ")
    savefile.write(str(dirSum))
    savefile.write("\n")

    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" router6 ")
    savefile.write(str(router6Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" tsv0Sum ")
    savefile.write(str(tsv0Sum))
    savefile.write("\n")
    savefile.write(str(file.name.replace('kB','')))
    savefile.write(" tsv1Sum ")
    savefile.write(str(tsv1Sum))
    savefile.write("\n")
    #savefile.write(str(file.name.replace('kB','')))
    #for i in drampower:
    #   print("drampower=",i)
    #   drampowerSum += int(i[0])
    #   print("drampowerSum is ",drampowerSum)
    #savefile.write(" drampowerSum ")
    #savefile.write(str(drampowerSum))
    #savefile.write("\n")

        
    file.close()
savefile.close()

