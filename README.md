# InputSimulator - 输入模拟工具

这是一个用Python编写的输入模拟工具，可以模拟键盘输入、组合键操作等功能。提供命令行和图形界面两种使用方式。

## 功能特点

- 支持固定间隔输入文本
- 支持随机间隔输入文本
- 支持模拟组合键操作
- 支持单次/循环输入模式
- 支持多种文本编码
- 支持直接输入模式（不使用输入法）
- 支持自定义快捷键
- 支持光标位置保持
- 支持窗口切换检测
- 内置安全机制，可随时停止
- 提供命令行和图形界面
- 现代化主题界面

## 文本格式化功能

### 1. 智能引号处理
- 自动检测和匹配引号配对
- 支持中英文各类引号
- 自动删除多余引号
- 智能补充缺失引号

### 2. 空格优化
- 自动清理多余空格
- 智能处理中英文之间的空格
- 保持段落格式
- 可选择保留换行符

### 3. 标点符号规范化
- 智能转换中英文标点
- 处理重复的标点符号
- 规范化省略号
- 统一标点样式

### 4. 段落格式化
- 自动格式化段落
- 规范段落间距
- 保持原有段落结构
- 智能处理空行

### 5. 文本分析
- 字符统计（总数、不含空格）
- 中文字符统计
- 单词统计（VSCode风格）
- 行数统计
- 格式问题检测

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行图形界面版本：

```bash
python gui_tk.py
```

2. 运行命令行版本：

```bash
python example.py
```

3. 在代码中使用：

```python
from input_simulator import InputSimulator

# 创建实例
simulator = InputSimulator()

# 基本输入（带格式化）
simulator.type_string("这是一个'测试'文本", 0.1, format_text=True)

# 自定义格式化规则
simulator.format_rules.update({
    'auto_match_quotes': True,  # 启用智能引号匹配
    'smart_punctuation': True,  # 启用智能标点处理
    'add_space_between_zh_en': True,  # 中英文之间添加空格
    'auto_format_paragraphs': True  # 启用段落格式化
})

# 分析文本
text = "这是一个测试文本...   Hello  world！"
analysis = simulator.analyze_text(text)
print(f"总字符数：{analysis['stats']['total_chars']}")
print(f"中文字符数：{analysis['stats']['chinese_chars']}")
print(f"发现的问题：{len(analysis['issues'])}")
```

## 格式化规则说明

```python
format_rules = {
    'max_consecutive_chars': 3,      # 最大连续字符数
    'max_consecutive_spaces': 1,     # 最大连续空格数
    'add_space_between_zh_en': True, # 中英文之间添加空格
    'normalize_ellipsis': True,      # 规范化省略号
    'normalize_punctuation': True,   # 规范化标点符号
    'trim_spaces': True,            # 清理多余空格
    'keep_original_format': False,   # 保持原格式
    'auto_match_quotes': True,      # 自动匹配引号
    'auto_format_paragraphs': True,  # 自动格式化段落
    'preserve_line_breaks': True,    # 保留换行符
    'smart_punctuation': True       # 智能标点处理
}
```

## 图形界面功能

- 文本输入区：输入要模拟的文本
- 格式控制：选择是否保持原文格式（换行、空格等）
- 输入模式：
  - 系统输入法：使用系统默认输入法
  - 直接输入：绕过输入法直接输入文本
- 编码设置：支持 utf-8、gbk、gb2312、ascii 等编码
- 输入类型：
  - 单次输入：输入完成后自动停止
  - 循环输入：持续重复输入直到手动停止
- 间隔设置：
  - 固定间隔：设置固定的输入间隔时间
  - 随机间隔：设置最小和最大间隔范围
- 快捷键控制：
  - 可自定义开始/暂停快捷键
  - 可自定义停止快捷键
  - 快捷键配置自动保存
- 控制面板：开始/暂停/停止输入
- 状态栏：显示当前状态
- 现代主题：清爽美观的界面设计

## 高级特性

1. 光标位置保持：
   - 自动检测并保持光标位置
   - 支持跨窗口输入
   - 智能窗口切换检测

2. 安全机制：
   - 窗口切换自动停止
   - ESC键紧急停止
   - 鼠标角落停止
   - 异常自动处理

3. 性能优化：
   - 使用剪贴板优化输入
   - 智能字符处理
   - 低延迟响应

## 注意事项

1. 使用pyautogui的FAILSAFE功能，将鼠标快速移动到屏幕角落可以强制停止程序
2. 持续输入模式可以通过快捷键或按钮停止
3. 建议在使用前先在安全的环境中测试
4. 使用时请遵守相关法律法规和使用政策
5. 快捷键设置会保存在config.json文件中
6. 直接输入模式可能不支持某些特殊字符
7. 某些应用程序可能会限制直接输入模式
8. 窗口切换时会自动停止输入以保护安全

## 开发环境

- Python 3.6+
- pyautogui 0.9.54
- keyboard 0.13.5
- colorama 0.4.6
- ttkthemes 3.2.2
- pywin32 306

## 许可证

MIT License