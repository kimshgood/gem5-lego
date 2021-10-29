
file_name = 'run.exe'
import os
try :
    os.remove("file_name")
except:
    print("fail")

f = open(file_name, 'w')
line=[]

binarys=[]
options=[]

#graphBIG ='/home/kimsh/graphBIG/benchmark/'
##0
#dir=graphBIG + 'bench_DFS/'
#binary =dir+ 'dfs'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##1
#dir=graphBIG + 'bench_BFS/'
#binary =dir+ 'bfs'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##2
#dir=graphBIG + 'bench_TopoMorph/'
#binary =dir+ 'topomorph'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##3
#dir=graphBIG + 'bench_betweennessCentr/'
#binary =dir+ 'bc'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##4
#dir=graphBIG + 'bench_connectedComp/'
#binary =dir+ 'connectedcomponent'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##5
#dir=graphBIG + 'bench_graphColoring/'
#binary =dir+ 'graphcoloring'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##6
#dir=graphBIG + 'bench_graphConstruct/'
#binary =dir+ 'graphconstruct'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
##7
#dir=graphBIG + 'bench_graphUpdate/'
#binary =dir+ 'graphupdate'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)

#dir=graphBIG + 'bench_kCore/'
#binary =dir+ 'kcore'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'bench_pageRank'
#binary =dir+ 'pagerank'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'bench_shortestPath'
#binary =dir+ 'sssp'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'bench_triangleCount'
#binary =dir+ 'tc'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'ubench_add'
#binary =dir+ 'ubench_add'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'ubench_delete'
#binary =dir+ 'ubench_delete'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'ubench_find'
#binary =dir+ 'ubench_find'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)
#
#dir=graphBIG + 'ubench_traverse'
#binary =dir+ 'ubench_traverse'
#option ="\'--dataset /home/kimsh/graphBIG/dataset/small\'"
#binarys.append(binary)
#options.append(option)

cpu2017home ='/home/kimsh/cpu2017/'
ref_suffix = '_r'

dir=cpu2017home + '505.mcf_r/'
binary =dir+ 'mcf' + ref_suffix
option =dir+ 'inp.in'
binarys.append(binary)
options.append(option)

dir =cpu2017home + '507.cactuBSSN_r/' 
binary =dir+ 'cactuBSSN' + ref_suffix
option =dir+ 'spec_ref.par'
binarys.append(binary)
options.append(option)

dir =cpu2017home + '510.parest_r/' 
binary =dir+ 'parest' + ref_suffix
option =dir+ 'ref.prm'
binarys.append(binary)
options.append(option)

dir =cpu2017home + '523.xalancbmk_r/'
binary =dir+ 'xalancbmk' + ref_suffix
option ="\'-v /home/kimsh/cpu2017/523.xalancbmk_r/t5.xml \
      /home/kimsh/cpu2017/523.xalancbmk_r/xalanc.xsl\'"
binarys.append(binary)
options.append(option)

dir =cpu2017home + '531.deepsjeng_r/'
binary =dir+ 'deepsjeng' + ref_suffix
option = dir + 'ref.txt'
binarys.append(binary)
options.append(option)

dir =cpu2017home + '541.leela_r/'
binary =dir+ 'leela' + ref_suffix
option = dir + 'ref.sgf'
binarys.append(binary)
options.append(option)


l1_sizes=['32kB']
l2_sizes=['512B']
l3_sizes=['4096kB']
cachelines=['128']

cpu_clocks=['1GHz']
num_cpus=['6','8','12','16','24','32']
num_dirs=['1']

num_clusters=['4']  ## number of CPU Clusters
num_cacheClusters=['1']

topologys=['Lego2D','Lego3D'] 
tsv_types=['2d','noc','g1','g1l1','g2','g3','g4']
linkWidths=['128']
tsv_len_masters=['2']
tsv_len_slaves=['1']

for i in range(6):  # number of bench marks
 for l1_size in l1_sizes :
  for l2_size in l2_sizes :
   for num_cpu in num_cpus :
    for num_dir in num_dirs :
     for l3_size in l3_sizes :
      for linkWidth in linkWidths:
       for num_dir in num_dirs:
        for topology in topologys:
         for num_cluster in num_clusters:
          for num_cacheCluster in num_cacheClusters:
           for tsv_len_master in tsv_len_masters:
            for tsv_len_slave in tsv_len_slaves:
             for tsv_type in tsv_types:
              for cacheline in cachelines:
               for cpu_clock in cpu_clocks:
                  noc=''
                  num_tsv=''
                  tsv_local=''

                  if tsv_type == 'noc':
                      noc = 'nocOn'
                      num_tsv='0'
                      tsv_local='0'
                      topology='Lego3D'

                  elif tsv_type == '2d':
                      noc = 'nocOff'
                      num_tsv='0'
                      tsv_local='0'
                      topology='Lego2D'

                  elif tsv_type == 'g1':
                      noc = 'nocOff'
                      num_tsv='1'
                      tsv_local='0'
                      topology='Lego3D'
                  elif tsv_type == 'g1l1':
                      noc = 'nocOff'
                      num_tsv='1'
                      tsv_local='1'
                      topology='Lego3D'
                  elif tsv_type == 'g2':
                      noc = 'nocOff'
                      num_tsv='2'
                      tsv_local='0'
                      topology='Lego3D'
                  elif tsv_type == 'g3':
                      noc = 'nocOff'
                      num_tsv='3'
                      tsv_local='0'
                      topology='Lego3D'
                  elif tsv_type == 'g4':
                      noc = 'nocOff'
                      num_tsv='4'
                      tsv_local='0'
                      topology='Lego3D'


                #for num_tsv in num_tsvs:
                 #for tsv_local in tsv_locals:

                  dir_name = \
                           "bin_"+str(i) +"_l1_"+l1_size \
                          + "_l2_"+l2_size + "_l3_"+l3_size  \
                          + "_cpu_"+num_cpu +"_clk"+ cpu_clock\
                          + "_numdir"+num_dir +"_numtsv"+num_tsv\
                          + "_tsvlocal"+tsv_local\
                          + "_len_m"+tsv_len_master\
                          + "_len_s"+tsv_len_slave\
                          + "_topo"+topology\
                          + "_cluster"+num_cluster\
                          + "cachecluster"+num_cacheCluster\
                          + "_cacheline"+cacheline\
                          + "_type"+tsv_type\
                          + "_linkWidth"+linkWidth\

                  #line.append(' ./build/X86_MESI_Two_Level/gem5.opt')
                  ## Three Level
                  line.append(' ./build/X86_MESI_Three_Level/gem5.opt')

                  #line.append(' --debug-flag=RubyQueue')
                  #line.append(' --debug-flag=RubyNetwork')
                  #line.append(' --debug-flag=Ruby')
                  line.append(' --outdir=M5OUT_%s/'%file_name)
                  line.append('%s'%dir_name)
                  line.append(' configs/example/se_lego.py ')
                  line.append(' --caches')

                  #line.append(' --l1i_size=%s'%l1i_size)
                  #line.append(' --l1d_size=%s'%l1d_size)
                  #line.append(' --l2_size=%s'%l2_size)

                  # Three Level
                  line.append(' --l0i_size=%s'%l1_size)
                  line.append(' --l0d_size=%s'%l1_size)
                  line.append(' --l1d_size=%s'%l2_size)
                  line.append(' --l2_size=%s'%l3_size)
                  line.append(' --num-clusters=%s'%num_cluster)
                  #line.append(' --cpu-cluster0=%s'%cpu_cluster0[0])

                  line.append(' --cmd=%s'%binarys[i])
                  line.append(' --options=%s'%options[i])
                  line.append(' --ruby')
                  # num-cpus(2) + num-dirs(2) = 2
                  line.append(' --num-cpus=%s'%num_cpu)

                  #line.append(' --mesh-rows=%s'%mesh_row)
                  #mesh_row=str(int(num_cpu)+int(num_dir)+int(num_l2cache))
                  if topology == 'Lego3D':
                      if int(num_cluster) > 1 :
                          mesh_row=str(int(num_cluster)+int(num_dir))
                  if topology == 'Mesh_XY':
                      if int(num_cluster) > 1 :
                          mesh_row=str(int(num_cluster))

                  #line.append(' --mesh-rows=%s'%mesh_row)
                  #line.append(' --num-l2caches=%s'%num_l2cache)
                  line.append(' --num-l2caches=%s'%num_cluster)

                  line.append(' --num-dirs=%s'%num_dir)
                  line.append(' --num-tsvs=%s'%num_tsv)
                  line.append(' --tsv-local=%s'%tsv_local)
                  line.append(' --topology=%s'%topology)
                  line.append(' --rel-max-tick=100000000') 
                  line.append(' --network=garnet')
                  line.append(' --link-latency=1')
                  line.append(' --router-latency=1')
                  line.append(' --tsv-latency=1')
                  line.append(' --enable-prefetch')
                  line.append(' --num-cacheClusters=%s'%num_cacheCluster)
                  if noc == 'nocOn' :
                      line.append(' --noc-tsv')
                  line.append(' --tsv-len-master=%s'%tsv_len_master)
                  line.append(' --tsv-len-slave=%s'%tsv_len_slave)
                  line.append(' --cacheline_size=%s'%cacheline)
                  line.append(' --cpu-clock=%s'%cpu_clock)
                  line.append(' --link-width-bits=%s'%linkWidth)
                  line.append('\n')

for l in line :
    f.write(l)
    #print(l)

f.close()
os.chmod(file_name,777)
