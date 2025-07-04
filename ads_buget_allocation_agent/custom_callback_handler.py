#!/usr/bin/env python3
"""
自定义回调处理器 - 支持输出到文件
"""

import os
import sys
from datetime import datetime
from strands.handlers.callback_handler import PrintingCallbackHandler

class FileLoggingCallbackHandler:
    """将回调输出写入文件的处理器"""
    
    def __init__(self, log_file=None, also_print=True):
        """
        初始化文件日志回调处理器
        
        Args:
            log_file: 日志文件路径，如果为None则自动生成
            also_print: 是否同时在终端打印
        """
        if log_file is None:
            # 自动生成日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_log_{timestamp}.txt"
        
        self.log_file = log_file
        self.also_print = also_print
        
        # 创建日志文件并写入头部信息
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"日志文件: {self.log_file}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 日志将保存到: {self.log_file}")
    
    def __call__(self, **kwargs):
        """处理回调事件"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 格式化输出内容
        output_lines = []
        
        for key, value in kwargs.items():
            if value:  # 只处理非空值
                output_lines.append(f"[{timestamp}] {key}: {str(value)}")
        
        if output_lines:
            # 写入文件
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for line in output_lines:
                    f.write(line + "\n")
                f.write("\n")  # 添加空行分隔
            
            # 可选：同时在终端打印
            if self.also_print:
                for line in output_lines:
                    print(line)

class DualOutputCallbackHandler:
    """双输出回调处理器 - 同时输出到终端和文件"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_log_{timestamp}.txt"
        
        self.log_file = log_file
        self.original_stdout = sys.stdout
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 日志将保存到: {self.log_file}")
        
        # 创建PrintingCallbackHandler实例
        self.printing_handler = PrintingCallbackHandler()
    
    def __call__(self, **kwargs):
        """处理回调事件 - 同时输出到终端和文件"""
        # 重定向stdout到文件
        class TeeOutput:
            def __init__(self, file_path, original_stdout):
                self.file_path = file_path
                self.original_stdout = original_stdout
            
            def write(self, text):
                # 写入终端
                self.original_stdout.write(text)
                # 写入文件
                with open(self.file_path, 'a', encoding='utf-8') as f:
                    f.write(text)
            
            def flush(self):
                self.original_stdout.flush()
        
        # 临时重定向输出
        sys.stdout = TeeOutput(self.log_file, self.original_stdout)
        
        try:
            # 调用原始的PrintingCallbackHandler
            self.printing_handler(**kwargs)
        finally:
            # 恢复原始输出
            sys.stdout = self.original_stdout

class EnhancedDualOutputCallbackHandler:
    """增强的双输出回调处理器 - 完全模拟PrintingCallbackHandler的行为"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_log_{timestamp}.txt"
        
        self.log_file = log_file
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 日志将保存到: {self.log_file}")
        
        # 创建PrintingCallbackHandler实例
        self.printing_handler = PrintingCallbackHandler()
    
    def __call__(self, **kwargs):
        """处理回调事件 - 完全捕获PrintingCallbackHandler的输出"""
        
        # 创建一个捕获所有输出的类
        class OutputCapture:
            def __init__(self, file_path, original_stdout, original_stderr):
                self.file_path = file_path
                self.original_stdout = original_stdout
                self.original_stderr = original_stderr
                self.captured_output = []
            
            def write(self, text):
                # 写入终端
                self.original_stdout.write(text)
                # 记录输出用于写入文件
                self.captured_output.append(text)
            
            def flush(self):
                self.original_stdout.flush()
                # 将捕获的输出写入文件
                if self.captured_output:
                    with open(self.file_path, 'a', encoding='utf-8') as f:
                        f.write(''.join(self.captured_output))
                    self.captured_output.clear()
        
        # 创建输出捕获器
        output_capture = OutputCapture(self.log_file, self.original_stdout, self.original_stderr)
        
        # 临时重定向输出
        sys.stdout = output_capture
        sys.stderr = output_capture
        
        try:
            # 调用原始的PrintingCallbackHandler
            self.printing_handler(**kwargs)
            # 确保输出被写入文件
            output_capture.flush()
        finally:
            # 恢复原始输出
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr

class PerfectDualCallbackHandler:
    """完美的双输出回调处理器 - 直接继承PrintingCallbackHandler"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_log_{timestamp}.txt"
        
        self.log_file = log_file
        self.original_stdout = sys.stdout
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 日志将保存到: {self.log_file}")
        
        # 创建PrintingCallbackHandler实例
        self.printing_handler = PrintingCallbackHandler()
    
    def __call__(self, **kwargs):
        """处理回调事件 - 使用Tee方式同时输出"""
        
        class TeeFile:
            """同时写入终端和文件的类"""
            def __init__(self, log_file, original_stdout):
                self.log_file = log_file
                self.original_stdout = original_stdout
                self.buffer = []
            
            def write(self, text):
                # 写入终端
                self.original_stdout.write(text)
                # 缓存内容
                self.buffer.append(text)
            
            def flush(self):
                self.original_stdout.flush()
                # 将缓存内容写入文件
                if self.buffer:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        content = ''.join(self.buffer)
                        f.write(f"[{timestamp}] {content}")
                        if not content.endswith('\n'):
                            f.write('\n')
                    self.buffer.clear()
        
        # 创建Tee输出
        tee_output = TeeFile(self.log_file, self.original_stdout)
        
        # 临时替换stdout
        original_stdout = sys.stdout
        sys.stdout = tee_output
        
        try:
            # 调用原始的PrintingCallbackHandler
            self.printing_handler(**kwargs)
            # 确保输出被写入文件
            tee_output.flush()
        finally:
            # 恢复原始stdout
            sys.stdout = original_stdout

class UltimateDualCallbackHandler:
    """终极双输出回调处理器 - 完全捕获所有输出"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_log_{timestamp}.txt"
        
        self.log_file = log_file
        self.tool_counter = 0
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 日志将保存到: {self.log_file}")
    
    def __call__(self, **kwargs):
        """完全捕获所有回调事件"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 写入文件的内容
        file_content = []
        # 终端输出的内容
        terminal_content = []
        
        # 处理Agent的思考过程
        if 'agent_message' in kwargs and kwargs['agent_message']:
            message = kwargs['agent_message']
            terminal_content.append(str(message))
            file_content.append(f"[{timestamp}] Agent思考: {str(message)}")
        
        # 处理工具使用
        if 'current_tool_use' in kwargs and kwargs['current_tool_use']:
            self.tool_counter += 1
            tool_use = kwargs['current_tool_use']
            
            if isinstance(tool_use, dict):
                tool_name = tool_use.get('name', 'unknown')
                tool_input = tool_use.get('input', {})
                
                # 终端输出
                terminal_content.append(f"Tool #{self.tool_counter}: {tool_name}")
                
                # 文件输出
                file_content.append(f"[{timestamp}] 工具调用 #{self.tool_counter}: {tool_name}")
                
                # 特殊处理python_repl工具
                if tool_name == 'python_repl' and 'code' in tool_input:
                    code = tool_input['code']
                    terminal_content.append(f"执行Python代码:\n{code}")
                    file_content.append(f"[{timestamp}] Python代码:\n{code}")
                
                # 处理其他工具输入
                elif tool_input:
                    for key, value in tool_input.items():
                        if value and key != 'code':  # code已经特殊处理了
                            terminal_content.append(f"{key}: {str(value)}")
                            file_content.append(f"[{timestamp}] {key}: {str(value)}")
        
        # 处理工具结果
        if 'tool_result' in kwargs and kwargs['tool_result']:
            result = kwargs['tool_result']
            result_str = str(result)
            
            terminal_content.append(f"工具执行结果:\n{result_str}")
            file_content.append(f"[{timestamp}] 工具执行结果:\n{result_str}")
        
        # 处理其他所有数据
        for key, value in kwargs.items():
            if key not in ['current_tool_use', 'tool_result', 'agent_message'] and value:
                content = str(value)
                terminal_content.append(f"{key}: {content}")
                file_content.append(f"[{timestamp}] {key}: {content}")
        
        # 输出到终端
        if terminal_content:
            for line in terminal_content:
                print(line)
            print()  # 添加空行分隔
        
        # 写入文件
        if file_content:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for line in file_content:
                    f.write(line + "\n")
                f.write("\n")  # 添加空行分隔

class StructuredFileCallbackHandler:
    """结构化文件回调处理器 - 更详细的日志格式"""
    
    def __init__(self, log_file=None, also_print=True):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_detailed_{timestamp}.txt"
        
        self.log_file = log_file
        self.also_print = also_print
        self.step_counter = 0
        
        # 初始化日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("           预算分配Agent详细执行日志\n")
            f.write("=" * 60 + "\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"日志文件: {self.log_file}\n")
            f.write("=" * 60 + "\n\n")
        
        print(f"📝 详细日志将保存到: {self.log_file}")
    
    def __call__(self, **kwargs):
        """处理回调事件 - 结构化格式"""
        self.step_counter += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 写入文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n--- 步骤 {self.step_counter} [{timestamp}] ---\n")
            
            for key, value in kwargs.items():
                if value:
                    f.write(f"{key.upper()}:\n")
                    f.write(f"{str(value)}\n")
                    f.write("-" * 40 + "\n")
            
            f.write("\n")
        
        # 可选：终端输出
        if self.also_print:
            print(f"\n🔄 步骤 {self.step_counter} - {timestamp}")
            for key, value in kwargs.items():
                if value:
                    print(f"📋 {key}: {str(value)[:100]}..." if len(str(value)) > 100 else f"📋 {key}: {str(value)}")

class CompleteDualCallbackHandler:
    """完整的双输出回调处理器 - 累积版本，能够组合流式数据"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"budget_analysis_complete_{timestamp}.txt"
        
        self.log_file = log_file
        self.tool_counter = 0
        
        # 用于累积流式数据
        self.current_tool_input = ""
        self.current_tool_name = ""
        self.current_tool_id = ""
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 预算分配Agent完整执行日志 ===\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
        
        print(f"📝 完整日志将保存到: {self.log_file}")
        
        # 创建原始的PrintingCallbackHandler用于终端输出
        from strands.handlers.callback_handler import PrintingCallbackHandler
        self.printing_handler = PrintingCallbackHandler()
    
    def __call__(self, **kwargs):
        """同时处理终端输出和文件记录"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 先调用原始的PrintingCallbackHandler进行终端输出
        self.printing_handler(**kwargs)
        
        # 处理流式工具输入数据
        if 'delta' in kwargs and kwargs['delta']:
            delta = kwargs['delta']
            if 'toolUse' in delta and 'input' in delta['toolUse']:
                # 累积工具输入
                self.current_tool_input += delta['toolUse']['input']
        
        # 处理工具开始事件
        if 'current_tool_use' in kwargs and kwargs['current_tool_use']:
            tool_use = kwargs['current_tool_use']
            if isinstance(tool_use, dict):
                tool_name = tool_use.get('name', 'unknown')
                tool_id = tool_use.get('toolUseId', '')
                
                # 如果是新的工具调用
                if tool_id != self.current_tool_id:
                    self.tool_counter += 1
                    self.current_tool_name = tool_name
                    self.current_tool_id = tool_id
                    self.current_tool_input = ""
                    
                    # 记录工具开始
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n[{timestamp}] 🔧 工具 #{self.tool_counter}: {tool_name}\n")
                        f.write("-" * 40 + "\n")
                
                # 如果工具输入已经完整，记录Python代码
                if isinstance(tool_use.get('input'), dict) and 'code' in tool_use['input']:
                    code = tool_use['input']['code']
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(f"📝 Python代码:\n{code}\n\n")
        
        # 处理工具结果
        if 'tool_result' in kwargs and kwargs['tool_result']:
            result = str(kwargs['tool_result'])
            
            # 记录完整的工具信息
            with open(self.log_file, 'a', encoding='utf-8') as f:
                # 如果还没有记录Python代码，尝试从累积的输入中解析
                if self.current_tool_input and self.current_tool_name == 'python_repl':
                    try:
                        import json
                        input_data = json.loads(self.current_tool_input)
                        if 'code' in input_data:
                            f.write(f"📝 Python代码:\n{input_data['code']}\n\n")
                    except:
                        if self.current_tool_input.strip():
                            f.write(f"📝 工具输入:\n{self.current_tool_input}\n\n")
                
                # 记录工具结果
                f.write(f"📊 工具执行结果:\n{result}\n")
                f.write("=" * 40 + "\n")
        
        # 处理Agent消息
        if 'message' in kwargs and kwargs['message']:
            message_data = kwargs['message']
            if isinstance(message_data, dict) and 'content' in message_data:
                content = message_data['content']
                if isinstance(content, list) and len(content) > 0:
                    # 处理文本内容
                    text_content = ""
                    # 处理工具结果
                    tool_results = []
                    
                    for item in content:
                        if isinstance(item, dict):
                            if 'text' in item:
                                text_content += item['text']
                            elif 'toolResult' in item:
                                tool_result = item['toolResult']
                                if 'content' in tool_result:
                                    for result_item in tool_result['content']:
                                        if 'text' in result_item:
                                            tool_results.append(result_item['text'])
                    
                    # 记录工具执行结果
                    if tool_results:
                        with open(self.log_file, 'a', encoding='utf-8') as f:
                            f.write(f"\n[{timestamp}] 📊 Python执行结果:\n")
                            f.write("-" * 40 + "\n")
                            for result in tool_results:
                                # 清理Windows换行符
                                clean_result = result.replace('\r\n', '\n').replace('\r', '\n')
                                f.write(f"{clean_result}\n")
                            f.write("=" * 40 + "\n")
                    
                    # 记录Agent回复
                    if text_content.strip():
                        with open(self.log_file, 'a', encoding='utf-8') as f:
                            f.write(f"\n[{timestamp}] 🤖 Agent回复:\n")
                            f.write("-" * 40 + "\n")
                            f.write(f"{text_content}\n")
                            f.write("=" * 40 + "\n")
        
        # 可选：记录调试信息（注释掉以保持日志清洁）
        # important_keys = ['tool_result', 'current_tool_use', 'delta', 'message']
        # debug_info = []
        # for key in important_keys:
        #     if key in kwargs and kwargs[key]:
        #         debug_info.append(f"{key}: {str(kwargs[key])[:200]}...")
        # 
        # if debug_info:
        #     with open(self.log_file, 'a', encoding='utf-8') as f:
        #         f.write(f"\n[{timestamp}] 🔍 调试信息:\n")
        #         for info in debug_info:
        #             f.write(f"  {info}\n")

# 使用示例
def create_callback_handler(handler_type="complete", log_file=None, also_print=True):
    """
    创建回调处理器
    
    Args:
        handler_type: 处理器类型 ("simple", "dual", "enhanced", "perfect", "ultimate", "complete", "structured")
        log_file: 日志文件路径
        also_print: 是否同时在终端打印
    
    Returns:
        回调处理器实例
    """
    if handler_type == "simple":
        return FileLoggingCallbackHandler(log_file, also_print)
    elif handler_type == "dual":
        return DualOutputCallbackHandler(log_file)
    elif handler_type == "enhanced":
        return EnhancedDualOutputCallbackHandler(log_file)
    elif handler_type == "perfect":
        return PerfectDualCallbackHandler(log_file)
    elif handler_type == "ultimate":
        return UltimateDualCallbackHandler(log_file)
    elif handler_type == "complete":
        return CompleteDualCallbackHandler(log_file)
    elif handler_type == "structured":
        return StructuredFileCallbackHandler(log_file, also_print)
    else:
        raise ValueError(f"未知的处理器类型: {handler_type}")

if __name__ == "__main__":
    # 测试示例
    print("测试自定义回调处理器...")
    
    # 测试简单文件处理器
    handler = FileLoggingCallbackHandler("test_log.txt", also_print=True)
    handler(test_data="这是一个测试", step="初始化")
    
    print("测试完成，请查看生成的日志文件。")