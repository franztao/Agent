import sys

import pandas as pd

from agent.prompt.gpu_agonstic import task_description, requirements, prompt

sys.path.append('/home/hengtao/code/diagnostic/metax_gpu_diagnostic_suite')

from agent.tools.libs.shell_tool import shell_tool


def agonstic_mx_smi_topo__show_mxlk(r):
    print(r)
    # 规则
    pass


def reason_mx_smi_topo__show_mxlk(r):
    pass


def mx_smi_topo__show_mxlk():
    "mx-smi topo --show-mxlk"
    tool_input = "mx-smi topo --show-mxlk"
    r = shell_tool(tool_input)
    r_agonstic = agonstic_mx_smi_topo__show_mxlk(r)
    r_reason = reason_mx_smi_topo__show_mxlk(r)

    pass


def mxvs_p2p__unidirection():
    tool_input = "/opt/maca/bin/mxvs p2p --unidirection --dst-devices 0 --src-devices 0"
    tool_input = "/opt/maca/bin/mxvs p2p --unidirection  --src-devices 0,1,2,3,4,5,6,7 --dst-devices 0,1,2,3,4,5,6,7"
    r = shell_tool(tool_input)


def mxvs_p2p():
    tool_input = "/opt/maca/bin/mxvs  p2p --dst-devices 0 --src-devices 0"
    tool_input = "/opt/maca/bin/mxvs  p2p  --src-devices 0,1,2,3,4,5,6,7 --dst-devices 0,1,2,3,4,5,6,7"
    r = shell_tool(tool_input)


def mxvs_ops():
    tool_input = "/opt/maca/bin/mxvs  ops"
    tool_input = "/opt/maca/bin//mxvs p2p --src-devices 0,1,2,3,4,5,6,7 --dst-devices 0,1,2,3,4,5,6,7"
    r = shell_tool(tool_input)


def mx_smi_show_board_power():
    tool_input = "mx-smi  --show-board-power"
    r = shell_tool(tool_input)


def mx_smi_show_temperature():
    tool_input = "mx-smi --show-temperature"
    r = shell_tool(tool_input)


def dmesg_T():
    tool_input = "dmesg -T"
    r = shell_tool(tool_input)


def llm_get_judge_result():
    src = r"C:\Users\m01216.METAX-TECH\Desktop\2025\Apr\agent\操作手册(2).xlsx"
    df = pd.read_excel(src, sheet_name='Sheet1')

    for ind, row in df.iterrows():
        role = row['Item']
        comd = row['操作命令']
        remark = row['备注']
        if pd.isna(comd):
            continue

        goal = f'{task_description}。{role}。{requirements}'

        # 再通过shell工具查看当前环境是否具备运行调试等的条件
        r = shell_tool(comd.replace('\n', ' & '))
        # r=comd.replace('\n', ' & ')
        memory_short = r
        memory_long = remark
        output_demand = '''不管判断是不是坏卡，都需要输出判断的根据和理由"）。
        '''

        requirement = prompt.format(goal=goal, memory_short=memory_short,
                                    memory_long=memory_long, output_demand=output_demand)
        print(requirement)


if __name__ == '__main__':
    llm_get_judge_result()
