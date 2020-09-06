from datetime import datetime
import sys
import logging as log
import cv2 as cv
import numpy as np
import boto3
import json
#from botocore.exceptions import NoCrudentialsError
from collections import namedtuple
from matplotlib import pyplot as plt
from PIL import Image
import json
from collections import OrderedDict
import codecs
#import base64
import math

import comm.mqtt_pub as mp
import comm.mqtt_subs as ms
#from comm.send import SEND
with open('config.json', 'r') as f:
    config = json.load(f)
log.getLogger('boto3').setLevel(log.CRITICAL)
log.getLogger('botocore').setLevel(log.CRITICAL)
log.getLogger('urllib3').setLevel(log.CRITICAL)
ACCESS_KEY = config['DEFAULT']['ACCESS_KEY']
SECRET_KEY = config['DEFAULT']['SECRET_KEY']
region = config['DEFAULT']['REGION']
bucket_name = config['DEFAULT']['BUCKET_NAME']
s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,region_name=region)
class JotTable:
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.t_table = []
        self.t_rect = []
        self.th_hold = 3.0
        self.t_pic = []
        #self.img_file = "test.jpg"
        self.packet_size = 3000
        self.client = mp.initialize_mqtt()
        self.cam_id = config['DEFAULT']['CAM_ID']
    #####func comment

    def check_jot(self, tracked_objects, frames, tracks_data):
        #send = SEND()
        cur_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")#(datetime.today()).strftime("%d-%b-%Y %H%M%S")
        for i, tracks in enumerate(tracked_objects):
            for x, track in enumerate(tracks):
                _id_ = int(track.label.split()[1])
                if(len(self.t_table) <= _id_):
                    # t_table 에 초기화함수
                    # t_rext 초기화 함수
                    _len_ = len(self.t_table)
                    for _ in range(_id_ - _len_ + 1):
                        self.t_table.append([-1,-1,-1,-1,-1])
                        self.t_rect.append([-1,-1,-1,-1])
                        self.t_pic.append([])
                if( self.t_table[_id_][0] == -1 and self.t_table[_id_][1] == -1):
                    self.t_table[_id_] = [_id_, i, 0, 0, 0]
                if(self.t_table[_id_][2] == 0 ): # 처음 들어온 시간
                    self.t_table[_id_][2] = cur_time
                    t_left, t_top, t_right, t_bottom = track.rect
                    self.t_pic[_id_] = frames[i][t_top:t_bottom, t_left:t_right]
                self.t_table[_id_][3] = cur_time #마지막 등장시간 업데이트 계속 영원히 쭉
        for i in range(len(self.t_table)): # [3]이 멈추어도 [4]는 업데이트 해서 나온애인지 판별하기 위해 시간 계속 추가해줌
            self.t_table[i][4] = cur_time
        # send 위한 브루트포스 시작
        for i in range(len(self.t_table)):
            if (self.t_table[i][3] != self.t_table[i][4] and self.t_table[i][3] != -1):
                # 보낼것 저장하는 리스트
                send_table = [self.t_table[i][0], self.t_table[i][1], self.t_table[i][2], self.t_table[i][3]]
                self.t_table[i] = [-1,-1,-1,-1,-1] # if 통과 못하게 초기화 시킴
                #temp_t_1 = float(str(send_table[2]))
                #temp_t_2 = float(str(send_table[3]))

                temp_t_1_b = send_table[2].split(' ')[1].split(':')
                temp_t_2_b = send_table[3].split(' ')[1].split(':')

                temp_t_1 = 120*int(temp_t_1_b[0]) + 60*int(temp_t_1_b[1]) + int(temp_t_1_b[2])
                temp_t_2 = 120*int(temp_t_2_b[0]) + 60*int(temp_t_2_b[1]) + int(temp_t_2_b[2])
             
                if((temp_t_2 - temp_t_1) >= self.th_hold):
                    print("ID "+ str(send_table[0]) + " are detected!!!")
                    #print(temp_t_2 - temp_t_1)
                    self.table_file(send_table,tracks_data)
                    #self.send_to_pi(send, send_table, tracks_data)
                    #self.send_to_srv(send, send_table,frames)
                else:
                    print("ID "+ str(send_table[0]) + " are exist too small time")
    """
    def convertImagetoBase64(self,_img_file):
        with open(_img_file,"rb") as image_file:
            m_encoded = base64.b32encode(image_file.read()).decode('utf-8')
        return m_encoded
    """
    def upload_s3(self,data,name):
        try:
            data_serial = cv.imencode('.png', data)[1].tostring()
            self.s3.Bucket(bucket_name).put_object(Key=name, Body=data_serial, ContentType='image/png', ACL='public-read')
        except Exception as e:
            print(e)
    def upload_img_to_aws(self,data,name):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        try:
            data_serial = cv.imencode('.png', data)[1].tostring()
            s3_resource.Bucket(bucket_name).put_object(Key=name, Body=data_serial, ContentType='image/png', ACL='public-read')
            
            print("upload successful")
            return True
        except Exception as e:
            print(e)
    def table_file(self,send_table,tracks):
        #start = 0
        #end = self.packet_size
        #img_file = "test.jpg"
        for i in range(len(send_table)):
            send_table[i] = str(send_table[i])
        for i, track in enumerate(tracks):
            if track['id'] == int(send_table[0]):
                #f_cluster_mat = track['f_cluster'].get_clusters_matrix() #f_cluster 의 진짜 모습 두둥!!
                avg_feature = track['avg_feature']
                send_time = track['timestamps'] #2020811 for send timestamp -JUN
                #리스트로 저장시
                #print(type(f_cluster_mat), type(avg_feature))
                """
                data = {'p_id' : send_table[0],
                        #'f_cluster_mat' : f_cluster_mat.tolist(),
                        'avg_feature' : avg_feature.tolist(),
                        #'cam_id' : send_table[1],
                        'cam_id' : 1,
                        'start_time1' : send_table[2],
                        'end_time1' : send_table[3],
                        'pic': self.t_pic[int(send_table[0])].tolist(),
                        'timestamps' : send_time}
                """
                data_cluster = {"p_id" : send_table[0],
                                "avg_feature" : avg_feature.tolist(),
                                'timestamps' : send_time}
                #print(type(self.t_pic[int(send_table[0])].tolist()))
                img_file = "Pid_" + str(send_table[0]) + "_cid_" + str(0) + "_" + send_table[2] + ".png"
                #cv.imwrite(img_file, self.t_pic[int(send_table[0])])
                #self.upload_s3(self.t_pic[int(send_table[0])],img_file)
                self.upload_img_to_aws(self.t_pic[int(send_table[0])],img_file)
                #print(data)
                data_pic = {"p_id" : send_table[0],
                            "cam_id" : 2,
                            "start_time" : send_table[2],
                            "end_time" : send_table[3],
                            "pic": img_file
                            }
                #data_pic = json.loads(data_pic)
                #filepath = "./sample.json"
                #with open(filepath, 'w') as f:
                    #data_pic = json.dump(data_pic,f)
                #data = json.dumps(data)
                data_cluster = json.dumps(data_cluster)
                data_pic = json.dumps(data_pic)
                #print(data_pic)
                print("dump success")
                #mp.publish_msg(self.client,data)
                mp.publish_msg_srv(self.client,data_pic)
                mp.publish_msg_pi1(self.client,data_cluster)
            else:
                continue
