import sys

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


if __name__ == '__main__':
    mx_smi_topo__show_mxlk()
    mxvs_p2p__unidirection()
    mxvs_p2p()
