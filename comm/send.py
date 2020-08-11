import json
from collections import OrderedDict
import codecs
import numpy as np
from collections import namedtuple
import comm.mqtt as mp
import paho.mqtt.client as mqtt
from comm.numpy_json_encoder import NumpyEncoder

class SEND:
    def __init__(self):
        self.pi_filepath = "pi_jot.json"
        self.srv_filepath = "srv_jot.json"
        self.client = mp.get_mqtt_client() # why so slow?

    def table_file(self,send_table, flag):
        if(flag == "pi"):
            data = {'id' : send_table[0],
                        'f_cluster_mat': send_table[1].tolist(),
                        'avg_feature': send_table[2].tolist()}
            data = json.dumps(data)
            print("dump sucess")
            mp.publish_msg(self.client,data)
            
        
        elif(flag == "srv"):
            for i in range(len(send_table)):
                send_table[i] = str(send_table[i])

            data={'p_id' : send_table[0],
                        'cam_id' : send_table[1],
                        'start_time1' : send_table[2],
                        'end_time1' : send_table[3],
                        'pic': self.t_pic[int(send_table[0])].tolist()}
            
            data = json.dumps(data)
            mp.publish_msg(self.client,data)


        # 복구용
        """
        obj_text = codecs.open(filepath, 'r', encoding='utf-8').read()
        json_load = json.loads(obj_text)
        pic_restored = np.array(json_load['pic'], dtype=np.uint8)
        p_id_restored = int(json_load['p_id'])
        cam_id_restored = int(json_load['cam_id'])
        s_time_restored = str(json_load['start_time1'])
        e_time_restored = str(json_load['end_time1'])

        print("p_id : ", p_id_restored)
        print("cam_id : ", cam_id_restored)
        print("s_time : ", s_time_restored)
        print("e_time : ", e_time_restored)
        cv.imshow("restored", pic_restored)
        """

        print("send to pi : success")