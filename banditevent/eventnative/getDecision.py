from peewee import *
import datetime

def Bandit_decisions_model(project_id,db):
    table_name = 'bandit_%s_decisions' % str(project_id)

    class BanditMetaclass(Model):
        def __new__(cls, name, bases, attrs):
            name += '_' + prefix  # 这是Model的name.
            return Model.__new__(cls, name, bases, attrs)

    class Decision(Model):
        __metaclass__ = BanditMetaclass
        experiment_id = CharField()
        mdp_id = CharField()
        decision_id = CharField()
        decision = CharField()
        ts = IntegerField(null=True,verbose_name='时间戳')
        created_date = DateTimeField(default=datetime.datetime.now)
        variation_id = IntegerField(null=True,verbose_name='变异ID')
        context = TextField()
        score = FloatField()

    
        @staticmethod
        def is_exists():
            return db.table_exists(table_name)#table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name
            database=db
            
    #db.connect()
    db.create_tables([Decision])
    #db.close()
    return Decision

def Bandit_rewards_model(project_id,db):
    table_name = 'bandit_%s_rewards' % str(project_id)

    class BanditMetaclass(Model):
        def __new__(cls, name, bases, attrs):
            name += '_' + prefix  # 这是Model的name.
            return Model.__new__(cls, name, bases, attrs)

    class Reward(Model):
        __metaclass__ = BanditMetaclass
        experiment_id = CharField()
        mdp_id = CharField(null=True)
        decision_id = CharField(null=True)
        decision = CharField(null=True)
        ts = IntegerField(null=True,verbose_name='时间戳')
        created_date = DateTimeField(default=datetime.datetime.now)
        metrics = TextField()
    
        @staticmethod
        def is_exists():
            return db.table_exists(table_name)#table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name
            database=db
            
    #db.connect()
    db.create_tables([Reward])
    #db.close()
    return Reward
