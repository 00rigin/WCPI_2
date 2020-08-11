import json
with open("pi_jot.json",encoding='utf-16') as f:
        cluster_data = json.load(f)
        #print(cluster_data)
        cluster_f = cluster_data["f_cluster_mat"]
        print(cluster_f)