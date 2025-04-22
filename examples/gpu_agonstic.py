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


if __name__ == '__main__':
    mx_smi_topo__show_mxlk()
