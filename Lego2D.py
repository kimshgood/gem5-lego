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

class Lego2D(SimpleTopology):
    description='Lego2D'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes
        # Last +1 = Router 6Port
        num_routers = len(nodes)+options.num_clusters +options.num_cacheClusters +1

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis


        # 
        # link_latency increased.
        link_latency = options.link_latency 
        router_latency = options.router_latency # only used by garnet

        l2_latency = options.l2_link_latency 
        dram_latency = options.dram_link_latency 

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

        routers = [Router(router_id=i, latency = router_latency) \
            for i in range(num_routers)]

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
        #print("router_id_DIR  = ",router_id_DIR)

        #print("rounter_id_start L0, L1, L2",router_id_L0,router_id_L1,router_id_L2)

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
                                    latency = link_latency+dram_latency)) ## Add +3 ( 2.2ns)
            print("dir_router number",link_count)
            link_count += 1

        network.ext_links = ext_links

        #########################################################
        int_links = []

        router_id_L0 = 0
        router_id_L1 = options.num_cpus
        ## if num_cpus == 32 ,
        ## router[0~31] = L0 Router    router[31~63] = L1 Router
        ## L0 <--> L1 link 
        print("L0 <--> L1 link start")
        for i in range(options.num_cpus):
            print("src_node = ",router_id_L0+i)
            print("dst_node = ",router_id_L1+i)
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
        ## L1(8)  <--> Cluster Router 1  <--> |r|
        ## L1(16) <--> Cluster Router 0  <--> |o|
        ##           L3<--> cacheCluster <--> |u|
        ##                          DRAM <--> |t|
        ##                                    |6|
        
        start_cpuCluster = len(self.nodes)
        end_cpuCluster = start_cpuCluster + options.num_clusters 
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
            print("cpu_cluster0=",cpu_cluster0)
            print("cpu_cluster1=",cpu_cluster1)
            print("cpu_cluster2=",cpu_cluster2)
            print("cpu_cluster3=",cpu_cluster3)

        for cluster in routers[start_cpuCluster:end_cpuCluster]:  
            print("cluster link start",cluster)
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
                print("src_node = ",routers[router_id_start+i])
                print("dst_node = ",cluster)
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
            for L2node in routers[start_L2:end_L2]:
                print("src ",L2node)
                print("dst ",cluster)
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


        start_r6 = end_cacheCluster
        end_r6 = start_r6+1

        start_dir = len(self.nodes) - options.num_dirs

        for r6 in routers[start_r6:end_r6]:
            for cluster in routers[start_dir:end_cacheCluster]:
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=cluster,
                                 dst_node=r6,
                                 weight=1,
                                 latency = link_latency+l2_latency))  ## Latency Increase +1.2ns
                link_count +=1
                int_links.append(IntLink(link_id=(link_count),
                                 src_node=r6,
                                 dst_node=cluster,
                                 weight=1,
                                 latency = link_latency+l2_latency))  ## Latency Increase
                link_count +=1
            

        network.int_links = int_links
