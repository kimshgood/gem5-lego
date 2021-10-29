# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

#  Add NOC TSV.

class Lego3D(SimpleTopology):
    description='Lego3D'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        num_routers = len(nodes) + options.num_tsvs  + options.tsv_local \
            + options.num_clusters +options.num_cacheClusters

        num_rows = options.mesh_rows
        num_tsvs = options.num_tsvs

        tsv_local = options.tsv_local
        tsv_len_master = options.tsv_len_master
        tsv_len_slave = options.tsv_len_slave

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency # used by simple and garnet
        router_latency = options.router_latency # only used by garnet
        tsv_latency = options.tsv_latency

        cache_nodes = []
        dir_nodes = []
        for node in nodes:
            ##print("node is",node.type)
            if node.type == 'L0Cache_Controller' or \
               node.type == 'L1Cache_Controller' or \
               node.type == 'L2Cache_Controller' :
                #print("cache_node.type =",node)
                cache_nodes.append(node)
            elif node.type == 'Directory_Controller':
                #print("dir_node.type =",node)
                dir_nodes.append(node)

        #print("shokim number of cache nod is = ",len(cache_nodes))
        #print("shokim number of dir nod is = ",len(dir_nodes))

        # Obviously the number or rows must be <= the number of routers
        # and evenly divisible.  Also the number of caches must be a
        # multiple of the number of routers and the number of directories
        # must be four.
        #assert(num_rows > 0 and num_rows <= num_routers)
        #num_columns = int(num_routers / num_rows)
        #assert(num_columns * num_rows == num_routers)
        #caches_per_router, remainder = divmod(len(cache_nodes), num_routers)

        # Create the routers in the mesh

        routers = [Router(router_id=i, latency = router_latency) \
            for i in range(num_routers)]

        for i in range(num_tsvs):
            exec('tsv%d = routers[len(self.nodes) +  %d]'\
                %(i,i))
            exec('tsv%d.latency = tsv_latency'\
                %i)

        total_clusters = options.num_clusters + options.num_cacheClusters
        for i in range(total_clusters) :
            exec('cluster%d = routers[len(self.nodes) + options.num_tsvs + %d]'\
                %(i,i))


        network.routers = routers

        # link counter to set unique link ids
        link_count = 0

        # Connect each cache controller to the appropriate router
        ext_links = []

        # number of L0/L1 node  is num_cpus 
        router_id_L0 = 0
        router_id_L1 = options.num_cpus
        router_id_L2 = options.num_cpus*2 # L0 + L1
        router_id_DIR = options.num_cpus*2 + options.num_l2caches

        count_L0 = 0 
        count_L1 = 0 
        count_L2 = 0 

        for (i, n) in enumerate(cache_nodes):
            cntrl_level, router_id = divmod(i, len(cache_nodes))
            if(n.type == 'L0Cache_Controller'):
                #print("shokim L0Cache Selected",router_id_L0+count_L0)
                ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                        int_node=routers[router_id_L0+count_L0],
                                        latency = link_latency))
                count_L0 +=1
            if(n.type == 'L1Cache_Controller'):
                #print("shokim L1Cache Selected",router_id_L1+count_L1)
                ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                        int_node=routers[router_id_L1+count_L1],
                                        latency = link_latency))
                count_L1 +=1
            if(n.type == 'L2Cache_Controller'):
                #print("shokim L2Cache Selected",router_id_L2+count_L2)
                #print("shokim L2Cache link_count",link_count)
                ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                        int_node=routers[router_id_L2+count_L2],
                                        latency = link_latency))
                count_L2 +=1
            link_count += 1

        # Connect the dir nodes 
        for (i,n) in enumerate(dir_nodes):
            #print('shokim dir link_counter =',link_count)
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[link_count],
                                    latency = link_latency))
            #print("dir_router number",link_count)
            link_count += 1
        network.ext_links = ext_links

        ################Internal Link ####################################
        int_links = []

        router_id_L0 = 0
        router_id_L1 = options.num_cpus
        ## if num_cpus == 32 ,
        ## router[0~31] = L0 Router    router[31~63] = L1 Router
        ## L0 <--> L1 link 
        #print("L0 <--> L1 link start")
        for i in range(options.num_cpus):
            #print("src_node = ",router_id_L0+i)
            #print("dst_node = ",router_id_L1+i)
            int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[router_id_L0+i],
                                     dst_node=routers[router_id_L1+i],
                                     weight=1,
                                     latency = link_latency))
            link_count +=1
        for i in range(options.num_cpus):
            #print("src_node = ",router_id_L1+i)
            #print("dst_node = ",router_id_L0+i)
            int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[router_id_L1+i],
                                     dst_node=routers[router_id_L0+i],
                                     weight=1,
                                     latency = link_latency))
            link_count +=1
        ##                                     _
        ## L1(8)  <--> Cluster Router 2  <--> | |
        ## L1(8)  <--> Cluster Router 1  <--> |t|
        ## L1(16) <--> Cluster Router 0  <--> |s|
        ##                            L3 <--> |v|
        ##                          DRAM <--> |_|

        ## L0 =32, L1=32, L2 = 4, num_tsvs = 2  ==> Total 70
        #print("self.nodes # = ", len(self.nodes))
        ##0827 start_cpuCluster = len(self.nodes)+options.num_tsvs+options.tsv_local
        start_cpuCluster = len(self.nodes)
        end_cpuCluster = start_cpuCluster + options.num_clusters 

        #print("shokim start_cpuCluster = ",start_cpuCluster)
        if options.num_clusters == 3 :
            cluster0 = routers[start_cpuCluster]
            cluster1 = routers[start_cpuCluster+1]
            cluster2 = routers[start_cpuCluster+2]

        if options.num_clusters == 4 :
            cluster0 = routers[start_cpuCluster]
            cluster1 = routers[start_cpuCluster+1]
            cluster2 = routers[start_cpuCluster+2]
            cluster3 = routers[start_cpuCluster+3]

        #print("start_cluster is ",start_cpuCluster)
        #print("end_cluster is ",end_cpuCluster)
        ## our base architecture :  master 3 , slave 2(L3, DRAM)
        ## Cluster Router 0 has half  of CPUs. 
        ## Connection : L1  <--> cpu_Cluster_router
        cluster_count=0

        ## Add portion parameter 
        ## Master Rate & Slave Rate
        #master_rate = 50 [%]
        cpu_cluster0 =0
        cpu_cluster1 =0
        cpu_cluster2 =0
        cpu_cluster3 =0
        if options.num_clusters == 3:
            cpu_cluster0 = int(options.num_cpus * options.master_rate/100)
            cpu_cluster1 = int((options.num_cpus - cpu_cluster0 ) / 2)
            cpu_cluster2 = int(options.num_cpus - cpu_cluster0-cpu_cluster1)

        if options.num_clusters == 4:
            cpu_cluster0 = int(options.num_cpus * options.master_rate/100)
            cpu_cluster1 = int((options.num_cpus - cpu_cluster0 ) / 3)
            cpu_cluster2 = cpu_cluster1
            cpu_cluster3 = int(options.num_cpus - cpu_cluster0 -cpu_cluster1*2)
            #print("cpu_cluster0=",cpu_cluster0)
            #print("cpu_cluster1=",cpu_cluster1)
            #print("cpu_cluster2=",cpu_cluster2)
            #print("cpu_cluster3=",cpu_cluster3)
#
        for cluster in routers[start_cpuCluster:end_cpuCluster]:  
            #print("cluster link start",cluster)
            router_id_start = router_id_L1
            if cluster == cluster0 :
                num_cpu_cluster = cpu_cluster0
                router_id_start = router_id_L1
            elif cluster == cluster1 :
                num_cpu_cluster = cpu_cluster1
                router_id_start = router_id_L1 + cpu_cluster0
            elif cluster == cluster2 :
                num_cpu_cluster = cpu_cluster2
                router_id_start = router_id_L1 + cpu_cluster0 + cpu_cluster1
            elif cluster == cluster3 :
                num_cpu_cluster = cpu_cluster3
                router_id_start = router_id_L1 + cpu_cluster0 + cpu_cluster1\
                                 + cpu_cluster2

            for i in range(num_cpu_cluster):
                #print("src_node = ",routers[router_id_start+i])
                #print("dst_node = ",cluster)
                int_links.append(IntLink(link_id=(link_count),
                                         src_node=routers[router_id_start + i],
                                         dst_node=cluster,
                                         weight=1,
                                         latency = link_latency))
                link_count +=1
            for i in range(num_cpu_cluster):
                int_links.append(IntLink(link_id=(link_count),
                                         src_node=cluster,
                                         dst_node=routers[router_id_start + i],
                                         weight=1,
                                         latency = link_latency))
                link_count +=1


        #  Connection :  L2(L3cache) <--> cache_Cluster_router
        start_L2 = len(self.nodes) - (options.num_l2caches + options.num_dirs)
        end_L2 = start_L2 + options.num_l2caches 

        start_cacheCluster = len(self.nodes) +options.num_clusters
        end_cacheCluster = start_cacheCluster + options.num_cacheClusters 
        for cluster in routers[start_cacheCluster : end_cacheCluster]:
            ##print("cache cluster link start",cluster)
            for L2node in routers[start_L2:end_L2]:
                #print("src_node = ", L2node)
                #print("dst_node = ",cluster)
                int_links.append(IntLink(link_id=(link_count),
                                         src_node=L2node,
                                         dst_node=cluster,
                                         weight=1,
                                         latency = link_latency))
                link_count +=1
                int_links.append(IntLink(link_id=(link_count),
                                         src_node=cluster,
                                         dst_node=L2node,
                                         weight=1,
                                         latency = link_latency))
                link_count +=1

        # Global TSV Link  & Local TSV Link generation
        ## We have to link these router.
        ##L1(L2), L2(L3), DIR(DRAM)
        ## CPU<--> L1 <-->router# <---> TSV
        ##         L2 <-->router# <---> TSV
        ##        DIR <-->router# <---> TSV 
        start_tsv = len(self.nodes)+ options.num_clusters + options.num_cacheClusters
        #print("star_tsv = ", start_tsv)
        end_tsv = start_tsv+options.num_tsvs 
        #print("end_tsv is ",end_tsv)

        ## start is Dir
        start_dir = len(self.nodes) - options.num_dirs
        end_Cluster = start_tsv 

        if options.num_tsvs > 0 :
            for tsv in routers[start_tsv:end_tsv]:
                #print("tsv link start ",tsv)
                for cluster in routers[start_dir:end_Cluster]:
                    #print("src_node",cluster)
                    #print("dst_node",tsv)
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=cluster,
                                     dst_node=tsv,
                                     weight=1,
                                     latency = link_latency))
                    link_count +=1
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=tsv,
                                     dst_node=cluster,
                                     weight=1,
                                     latency = link_latency))
                    link_count +=1
            
        #tsv_local = options.tsv_local
        #tsv_len_master = options.tsv_len_master
        #tsv_len_slave = options.tsv_len_slave
        start_tsv_local = end_tsv
        end_tsv_local = start_tsv_local + options.tsv_local
        #print("start_tsv_local is ",start_tsv_local)
        #print("end_tsv_local is ",end_tsv_local)

        end_master=start_cpuCluster + options.tsv_len_master
        end_slave=start_cacheCluster + options.tsv_len_slave

        if tsv_local > 0 :
            for tsv in routers[start_tsv_local:end_tsv_local]:
                #print("tsv local is",tsv)
                #Master Cluster Router Length
                for master in routers[start_cpuCluster:end_master]:
                    #print("master is ",master)
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=master,
                                     dst_node=tsv,
                                     weight=1,
                                     latency = link_latency))
                    link_count +=1
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=tsv,
                                     dst_node=master,
                                     weight=1,
                                     latency = link_latency))
                    link_count +=1
                #Slave Cluster Router Length
                for slave in routers[start_cacheCluster:end_slave]:
                    #print("slave is ",slave)
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=slave,
                                     dst_node=tsv,
                                     weight=1,
                                     latency = link_latency))
                    link_count +=1
                    int_links.append(IntLink(link_id=(link_count),
                                     src_node=tsv,
                                     dst_node=slave,
                                     weight=1,
                                     latency = link_latency))
        
        if options.noc_tsv  :
            print("shokim noc tsv enable ")
            # master link example :  master<0:2> 
            # 0<->1, 1<->2, 2<->3
            i = 1
            for master in routers[start_cpuCluster:end_cpuCluster-1]:
                master_near = routers[start_cpuCluster +i]
                #print("src ",master)
                #print("dest ",master_near)
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=master,
                                 dst_node=master_near,
                                 weight=1,
                                 latency = link_latency))
                link_count +=1
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=master_near,
                                 dst_node=master,
                                 weight=1,
                                 latency = link_latency))
                link_count +=1
                i += 1

            #print(" Slave Noc Link Example start0")
            #Slave NoC Link Example :  slave<0:2>
            # s0(cacheCluster) <-->s1(cacheCluster) 
            j = 1
            #print("start_cacheCluster = ",start_cacheCluster)
            #print("end_cacheCluster = ",end_cacheCluster)
            for slave in routers[start_cacheCluster:end_cacheCluster-1]:
                slave_near = routers[start_cacheCluster +j]

                #print("slave is ",slave)
                #print("slave near is ",slave_near)
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=slave,
                                 dst_node=slave_near,
                                 weight=1,
                                 latency = link_latency))
                link_count +=1
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=slave_near,
                                 dst_node=slave,
                                 weight=1,
                                 latency = link_latency))
                link_count +=1
                j+=1

            #print("Share cache <--> Dir ")
            dir_router=routers[len(self.nodes)-options.num_dirs]
            #print("dir_router = ", dir_router)
            cache_router=routers[end_cacheCluster-1]
            #print("cache_router = ", cache_router)

            int_links.append(IntLink(link_id=(link_count),
                             src_node=dir_router,
                             dst_node=cache_router,
                             weight=1,
                             latency = link_latency))
            link_count +=1
            int_links.append(IntLink(link_id=(link_count),
                             src_node=cache_router,
                             dst_node=dir_router,
                             weight=1,
                             latency = link_latency))

            #print("## Master0 <--> Slave0 Link")
            master0 = routers[start_cpuCluster]
            #slave0 = routers[start_cacheCluster]
            slave0 = dir_router
            int_links.append(IntLink(link_id=(link_count),
                             src_node=master0,
                             dst_node=slave0,
                             weight=1,
                             latency = link_latency))
            link_count +=1
            int_links.append(IntLink(link_id=(link_count),
                             src_node=slave0,
                             dst_node=master0,
                             weight=1,
                             latency = link_latency))
            link_count +=1

        network.int_links = int_links
