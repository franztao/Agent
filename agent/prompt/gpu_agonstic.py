
prompt = """
# 目标，任务描述
***
{goal}
***
# 短期记忆
***
{memory_short}
***
# 长期记忆
***
{memory_long}
***
# 限制
***
{output_demand}
***
# 输出

"""

# import jionlp as jio
task_description = r'当前项目目标是”GPU显卡进行测试，判断是否是有故障的坏卡“。'

requirements = r'当前运行的环境是linux,根据判断条件（长期记忆）和执行的linux命令返回信息（短期记忆），请判断是否是坏卡'


