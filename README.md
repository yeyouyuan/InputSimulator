# InputSimulator - 智能输入模拟工具

这是一个用Python编写的智能输入模拟工具，提供文本输入模拟、格式化和分析功能。支持命令行和图形界面两种使用方式。

## 主要功能

### 1. 基础输入功能
- 支持固定/随机间隔输入
- 支持单次/循环输入模式
- 支持多种文本编码
- 支持直接输入和输入法模式
- 支持自定义快捷键
- 支持光标位置保持
- 支持窗口切换检测

### 2. 智能格式化功能
- 自动引号匹配和修正
- 智能空格优化
- 标点符号规范化
- 段落格式化
- 中英文混排优化

### 3. 文本分析功能
- 字符统计（总数、有效字符）
- 中英文分别统计
- 格式问题检测
- 实时分析反馈

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 图形界面版本

```bash
python gui_tk.py
```

### 2. 命令行版本

```bash
python example.py
```

### 3. 代码调用示例

```python
from input_simulator import InputSimulator

# 创建实例
simulator = InputSimulator()

# 基本输入示例
simulator.type_string("Hello, World!", 0.1)

# 格式化输入示例
text = "这是一个'测试'文本...   Hello  world！"
simulator.type_string(text, 0.1, format_text=True)

# 自定义格式化规则
simulator.format_rules.update({
    'auto_match_quotes': True,      # 自动匹配引号
    'smart_punctuation': True,      # 智能标点处理
    'add_space_between_zh_en': True,# 中英文间添加空格
    'auto_format_paragraphs': True  # 自动格式化段落
})

# 文本分析示例
analysis = simulator.analyze_text(text)
print(f"总字符数：{analysis['stats']['total_chars']}")
print(f"中文字符数：{analysis['stats']['chinese_chars']}")
print(f"发现的问题：{len(analysis['issues'])}")
```

## 格式化规则说明

### 1. 引号处理
```python
quote_rules = {
    'auto_match_quotes': True,    # 自动匹配引号
    'quote_style': 'smart',       # 引号样式：smart/chinese/english
    'fix_unmatched': True         # 修复未匹配引号
}
```

### 2. 空格处理
```python
space_rules = {
    'max_consecutive_spaces': 1,   # 最大连续空格数
    'trim_spaces': True,          # 清理多余空格
    'preserve_line_breaks': True,  # 保留换行符
    'add_space_between_zh_en': True # 中英文之间添加空格
}
```

### 3. 标点处理
```python
punctuation_rules = {
    'smart_punctuation': True,     # 智能标点处理
    'normalize_ellipsis': True,    # 规范化省略号
    'normalize_punctuation': True,  # 规范化标点符号
    'fix_duplicates': True         # 修复重复标点
}
```

### 4. 段落格式化
```python
paragraph_rules = {
    'auto_format_paragraphs': True,  # 自动格式化段落
    'keep_original_format': False,   # 保持原格式
    'max_consecutive_newlines': 2,   # 最大连续换行数
    'indent_paragraphs': False       # 段落缩进
}
```

## 文本分析功能

### 1. 基础统计
- 总字符数（含/不含空格）
- 中文字符数
- 英文单词数
- 标点符号数
- 行数统计

### 2. 格式检查
- 重复字符检测
- 多余空格检测
- 中英文混排问题
- 标点符号使用
- 引号匹配检查

### 3. 问题报告
```python
{
    'type': '问题类型',
    'position': 问题位置,
    'content': '问题内容',
    'description': '问题描述'
}
```

## 高级特性

### 1. 输入优化
- 批量输入处理
- 智能字符处理
- 低延迟响应
- 自动错误恢复

### 2. 安全机制
- 窗口切换检测
- ESC紧急停止
- 异常自动处理
- 状态实时反馈

### 3. 性能优化
- 批量事件处理
- 智能缓冲机制
- 资源占用优化
- 内存使用优化

## 注意事项

1. 使用前请在安全环境中测试
2. 注意保存重要文档
3. 遵守使用政策
4. 建议先进行小规模测试
5. 定期检查更新
6. 注意系统兼容性
7. 合理设置输入速度
8. 保持良好使用习惯

## 开发环境

- Python 3.6+
- pyautogui 0.9.54
- keyboard 0.13.5
- colorama 0.4.6
- ttkthemes 3.2.2
- pywin32 306

## 许可证

MIT License