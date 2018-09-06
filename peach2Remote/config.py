# -*- coding: utf-8 -*-
from app import application

application.debug=True

application.secret_key = '0pMfZOHyqVwRSYrtmgI89Pc1hs4ezknA'

PORT = 5555
HOST = 'localhost'

sqlusername='root'
sqlpassword='123456'
sqlport='3306'
sqldatabasename='welding_process'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:{}/{}?charset=utf8'.format(sqlusername,sqlpassword,sqlport,sqldatabasename)
SQLALCHEMY_TRACK_MODIFICATIONS = True


#需要进行身份认证的控制器 认证失败则重定向到无权限页面
NEED_AUTH=['ma_index','ma_config']

#存在的设备 ID:状态
DEVICES={}

LOCALHOSTID=''

#焊接方法对照表
WELDINGTABLE={'MIG':'melting_polar_arc_weld','MAG':'melting_polar_arc_weld','PMIG':'melting_polar_arc_weld','PMAG':'melting_polar_arc_weld',
              'DWPMIG':'d_melting_polar_arc_weld','DWCMT':'d_melting_polar_arc_weld','TIG':'non_melting_polar_arc_weld','PAW':'non_melting_polar_arc_weld',
              'DTIG':'non_melting_polar_arc_weld','FSW':'friction_stir_weld','FW':'friction_stud_weld',
              'LBW':'laser_beam_weld','BW':'braze_weld','ERW':'electric_resistance_weld','SMAW':"manual_welding_rod_weld",
              'SAW':'submerge_arc_weld','EBW':'vacuum_electron_beam_weld'}
