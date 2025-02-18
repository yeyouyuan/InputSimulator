# InputSimulator - 智能输入模拟工具

这是一个用Python编写的智能输入模拟工具，提供文本输入模拟、格式化和分析功能。支持命令行和图形界面两种使用方式。

## 项目背景

本项目最初是为了解决QQ作家助手等写作工具的输入问题而开发的。QQ作家助手等工具虽然提供了很好的写作环境,但在输入方面存在一些限制:

1. 输入速度限制
- 系统默认输入速度较慢
- 无法自定义输入间隔
- 批量输入容易出错

2. 格式化问题
- 中英文混排格式不规范
- 标点符号使用不统一
- 段落格式难以保持

3. 使用不便
- 操作步骤繁琐
- 缺乏快捷键支持
- 无法及时分析文本

InputSimulator通过智能输入模拟和格式化处理,很好地解决了这些问题,让写作过程更加流畅自然。主要优势包括:

- 完全自定义的输入速度和间隔
- 智能的格式化和标点处理
- 便捷的快捷键和操作方式
- 实时的文本分析和反馈
- 稳定可靠的输入体验

通过这些功能,可以让作者将更多精力集中在创作本身,提高写作效率和质量。


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

Yeyouyuan 开源许可协议 v1.0

版权所有 © 2024 yeyouyuan

特此授予任何获得本软件和相关文档文件（以下简称"软件"）副本的个人和机构免费使用的权利，
包括但不限于使用、复制、修改、合并、出版、分发、再授权和/或销售该软件的副本，
但须遵守以下条件：

### 1. 基本条件

1.1 上述版权声明和本许可声明应包含在该软件的所有副本或主要部分中。

1.2 使用者必须在其项目文档中明确标注使用了本软件。

### 2. 使用限制

2.1 本软件仅限于学习、研究和个人使用。

2.2 禁止用于任何违反法律法规的活动。

2.3 在未经原作者书面许可的情况下，禁止用于商业目的。

### 3. 免责声明

本软件按"原样"提供，不提供任何形式的保证，无论是明示或暗示的，
包括但不限于适销性、特定用途的适用性和非侵权性的保证。
在任何情况下，作者或版权持有人均不对任何索赔、损害或其他责任负责，
无论是在合同诉讼、侵权行为或其他方面，由软件或软件的使用或其他交易引起、由软件引起或与之相关。

### 4. 贡献规则

4.1 任何人都可以通过 Pull Request 的方式向本项目贡献代码。

4.2 贡献者同意其贡献的代码采用本许可协议。

4.3 重要变更需要经过原作者审核通过。

### 5. 终止条款

5.1 如果使用者违反本许可的任何条款，本许可及其授予的权利将自动终止。

5.2 终止后，使用者必须立即停止使用本软件。

### 6. 其他条款

6.1 本许可协议的解释、效力及纠纷的解决均适用中华人民共和国法律。

6.2 本许可协议的最终解释权归原作者所有。

6.3 作者保留在不另行通知的情况下修改本许可协议的权利。