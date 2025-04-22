from __future__ import annotations

import uuid
import warnings
from typing import (
    Any,
    Optional,
    Union,
)

from langchain_core.callbacks import (
    Callbacks,
)
from langchain_core.runnables import (
    RunnableConfig,
)

# from metagpt.tools.tool_registry import register_tool

# from metagpt.logs import logger


# @register_tool(tags=["shell_tool"])
def shell_tool(tool_input: Union[str, dict[str, Any]],
               verbose: Optional[bool] = None,
               start_color: Optional[str] = "green",
               color: Optional[str] = "green",
               callbacks: Callbacks = None,
               *,
               tags: Optional[list[str]] = None,
               metadata: Optional[dict[str, Any]] = None,
               run_name: Optional[str] = None,
               run_id: Optional[uuid.UUID] = None,
               config: Optional[RunnableConfig] = None,
               tool_call_id: Optional[str] = None,
               **kwargs: Any,
               ) -> Any:
    """Run the tool.

        Args:
            tool_input: The input to the tool.
            verbose: Whether to log the tool's progress. Defaults to None.
            start_color: The color to use when starting the tool. Defaults to 'green'.
            color: The color to use when ending the tool. Defaults to 'green'.
            callbacks: Callbacks to be called during tool execution. Defaults to None.
            tags: Optional list of tags associated with the tool. Defaults to None.
            metadata: Optional metadata associated with the tool. Defaults to None.
            run_name: The name of the run. Defaults to None.
            run_id: The id of the run. Defaults to None.
            config: The configuration for the tool. Defaults to None.
            tool_call_id: The id of the tool call. Defaults to None.
            kwargs: Keyword arguments to be passed to tool callbacks

        Returns:
            The output of the tool.

        Raises:
            ToolException: If an error occurs during tool execution.
    """
    from langchain_community.tools import ShellTool
    # pip install  langchain-community  -i https://pypi.doubanio.com/simple
    # pip install  langchain-experimental -i https://pypi.doubanio.com/simple
    st = ShellTool()
    from langchain_core.globals import set_verbose, set_debug


    # Ignore all warnings
    warnings.filterwarnings("ignore")


    set_verbose(False)
    set_debug(False)
    try:
        result = st.run(tool_input, verbose, start_color, color, callbacks, tags=tags, metadata=metadata,
                        run_name=run_name,
                        run_id=run_id, config=config,
                        tool_call_id=tool_call_id, kwargs=kwargs)
        # result="success"
    except Exception as e:
        print(e)
        result = "call  error"
    result='```工具调用结果如下：\n'+result+'\n```'
    print(f"shell run is {result}")

    return result

# if __name__ == '__main__':
#     from langchain_community.tools import ShellTool
#
#     st = ShellTool()
#     print(st.description)
