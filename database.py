from peewee import *
from playhouse.postgres_ext import *
from playhouse.pool import PooledPostgresqlDatabase
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from multiprocessing import cpu_count as cpuCount

import os

db = PooledPostgresqlDatabase('shinycolors', max_connections=3*cpuCount(), **{'host': os.environ.get('SERVER'), 'user': os.environ.get('USERNAME'), 'password': os.environ.get('PASSWORD')})

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db
        schema = 'shinycolors'
        model_metadata_class = ThreadSafeDatabaseMetadata
        print("Database connected")


class ScdbAssetVersion(BaseModel):
    asset_encrypted_path = TextField(column_name='assetencryptedpath')
    asset_exist = IntegerField(column_name='assetexist')
    asset_index = AutoField(column_name='assetindex')
    asset_path = TextField(column_name='assetpath')
    asset_chunk = IntegerField(column_name='assetchunk')
    asset_version = IntegerField(column_name='assetversion')

    class Meta:
        table_name = 'scdb_assetversion'
        schema = 'shinycolors'


class ScdbUnits(BaseModel):
    color1 = TextField(column_name='color1')
    color2 = TextField(column_name='color2')
    unit_hiragana = TextField(column_name='unithiragana')
    unit_id = AutoField(column_name='unitid')
    unit_name = TextField(column_name='unitname')
    unit_pv = TextField(column_name='unitpv')

    class Meta:
        table_name = 'scdb_units'
        schema = 'shinycolors'


class ScdbIdols(BaseModel):
    age = IntegerField(column_name='age')
    birth_place = TextField(column_name='birthplace')
    birthday = TextField(column_name='birthday')
    blood_type = TextField(column_name='bloodtype')
    cv = TextField(column_name='cv')
    color1 = TextField(column_name='color1')
    color2 = TextField(column_name='color2')
    height = IntegerField(column_name='height')
    hiragana = TextField(column_name='hiragana')
    hirameki = TextField(column_name='hirameki')
    idol_hash = TextField(column_name='idolhash')
    idol_id = AutoField(column_name='idolid')
    idol_name = CharField(column_name='idolname', index=True)
    interest = TextField(column_name='interest')
    nick_name = TextField(column_name='nickname')
    pre_cv = TextField(column_name='precv', null=True)
    special_skill = TextField(column_name='specialskill')
    star_sign = TextField(column_name='starsign')
    three_size = TextField(column_name='threesize')
    unit = ForeignKeyField(column_name='unitid', field='unit_id', model=ScdbUnits)
    used_hand = TextField(column_name='usedhand')
    weight = IntegerField(column_name='weight')

    class Meta:
        table_name = 'scdb_idols'
        schema = 'shinycolors'


class ScdbCardList(BaseModel):
    big_pic1 = TextField(column_name='bigpic1', null=True)
    big_pic2 = TextField(column_name='bigpic2', null=True)
    card_hash = TextField(column_name='cardhash', null=True)
    card_index = AutoField(column_name='cardindex')
    card_name = TextField(column_name='cardname')
    card_type = TextField(column_name='cardtype')
    card_uuid = TextField(column_name='carduuid')
    enza_id = BigIntegerField(column_name='enzaid', index=True)
    get_method = TextField(column_name='getmethod', null=True)
    idea_mark = TextField(column_name='ideamark', null=True)
    idol = ForeignKeyField(column_name='idolid', field='idol_id', model=ScdbIdols)
    release_date = DateField(column_name='releasedate', null=True)
    last_modified = DateField(column_name='lastmodified', null=True)
    panel_sp_offset = IntegerField(column_name='panelspoffset', constraints=[SQL("DEFAULT 0")])
    sml_pic = TextField(column_name='smlpic', null=True)

    class Meta:
        table_name = 'scdb_cardlist'
        schema = 'shinycolors'

class ScdbSeiyuu(BaseModel):
    seiyuu_index = AutoField(column_name='seiyuuindex')
    seiyuu_name = TextField(column_name='seiyuuname')
    seiyuu_photo = TextField(column_name='seiyuuphoto')
    seiyuu_birth_year = TextField(column_name='seiyuubirthyear', null=True)
    seiyuu_birth_date = TextField(column_name='seiyuubirthdate', null=True)
    belonging_firm = TextField(column_name='belongingfirm')
    seiyuu_twitter = TextField(column_name='seiyuutwitter', null=True)
    seiyuu_chokume = TextField(column_name='seiyuuchokume', null=True)

    class Meta:
        table_name = 'scdb_seiyuu'
        schema = 'shinycolors'
