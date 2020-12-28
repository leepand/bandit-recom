import modelcloud
from modelcloud.data_types import text,number,any,category

from eventnative.bandit_data_model import Bandit_decisions_model,Bandit_rewards_model
from peewee import *
#d = "/Users/leepand/Downloads/github/vue/vue-admin-flask-example/algolink_ui_server/files/localdb/localdb3-v1/model_samples.db"
#db = SqliteDatabase(d)

from back_server.config import remote_path
import bolt4ds.pipe as bolt4dspipe

config_remote_path = remote_path

def get_db_file(project_id,config_remote_path):
    remote_rel_path = 'localdb{}-v{}'.format(project_id, "1")
    bolt4dspipe.api.ConfigManager(profile="localdb",
                                  filecfg=config_remote_path+"/cfg.json").init({'filerepo':config_remote_path})
    pipe = bolt4dspipe.PipeLocal(remote_rel_path,
                                 profile="localdb",
                                 filecfg=config_remote_path+"/cfg.json")
    return os.path.join(pipe.dir,"model_samples.db")

#db = SqliteDatabase(d)
decision_inputs = {
    'dataset_id': text(description="数据ID"),
    'project_id': text(description="项目ID"),
    'experiment_id': text(description="实验ID"),
    'mdp_id': text(description="马尔科夫决策ID"),
    'decision_id': text(description="推荐决策ID"),
    'decision': text(description="决策内容"),
    'ts': number(description="时间戳"),
    'variation_id': text(description="实验用例"),
    'context': text(description="特征内容"),
    'score' :any(description="决策的预期得分")
}
decisions_outputs = {
    'result': text(description="数据入库标识")
}

decision_description = '记录推荐系统的决策信息'

@modelcloud.command('logDecision', 
                    inputs=decision_inputs, 
                    outputs=decisions_outputs,
                    description=decision_description)
def decision_model(model, decisions):
    prefix= decisions["dataset_id"]
    project_id= decisions["project_id"]
    decision_id = decisions["decision_id"]
    db_file = get_db_file(project_id,config_remote_path)
    db = SqliteDatabase(db_file)
    DecisionModel = Bandit_decisions_model(prefix,project_id,db)
    DecisionModel(decision_id =decision_id,
                  context = decisions["context"],
                  experiment_id = decisions["experiment_id"],
                  decision = decisions["decision"],
                  mdp_id = decisions["mdp_id"],
                  variation_id = decisions["variation_id"],
                  ts = decisions["ts"],
                  score = decisions["score"]
                 ).save()
    return {"result":"True"}
    
reward_inputs = {
    'dataset_id': text(description="数据ID"),
    'project_id': text(description="项目ID"),
    'experiment_id': text(description="实验ID"),
    'mdp_id': text(description="马尔科夫决策ID"),
    'decision_id': text(description="推荐决策ID"),
    'decision': text(description="决策内容"),
    'ts': number(description="时间戳"),
    'metrics': text(description="奖励指标的映射")
}
reward_outputs = {
    'result': text(description="数据入库标识")
}

reward_description = '记录推荐系统的用户反馈信息'

@modelcloud.command('logReward', 
                    inputs=reward_inputs, 
                    outputs=reward_outputs,
                    description=reward_description)
def decision_model(model, rewards):
    prefix= rewards["dataset_id"]
    project_id= rewards["project_id"]
    decision_id = rewards["decision_id"]
    db_file = get_db_file(project_id,config_remote_path)
    db = SqliteDatabase(db_file)
    RewardModel = Bandit_rewards_model(prefix,project_id,db)
    if decision_id=="null":
        RewardModel(metrics = rewards["metrics"],
                    experiment_id = rewards["experiment_id"],
                    mdp_id = rewards["mdp_id"],
                    ts = rewards["ts"]
                   ).save()
    else:
        RewardModel(decision_id = rewards["decision_id"],
                    decision = rewards["decision"],
                    metrics = rewards["metrics"],
                    experiment_id = rewards["experiment_id"],
                    mdp_id = rewards["mdp_id"],
                    ts = rewards["ts"]
                   ).save()
    return {"result":"True"}

if __name__ == '__main__':
    modelcloud.run(port=9003,worker_class="gevent",runenv="dev")
