import time
import pyautogui
import keyboard
from typing import Union, List
from colorama import init, Fore
import random
import win32api
import win32con
import win32gui
import win32clipboard
import ctypes
import re
from collections import Counter
from ctypes import wintypes
import array

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', wintypes.LONG),
        ('dy', wintypes.LONG),
        ('mouseData', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wintypes.WORD),
        ('wScan', wintypes.WORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', wintypes.DWORD),
        ('wParamL', wintypes.WORD),
        ('wParamH', wintypes.WORD)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ('type', wintypes.DWORD),
        ('union', INPUT_UNION)
    ]

class InputSimulator:
    def __init__(self):
        init()  # 初始化colorama
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.running = False
        self.max_retries = 3  # 最大重试次数
        
        # 常量定义
        self.INPUT_MOUSE = 0
        self.INPUT_KEYBOARD = 1
        self.INPUT_HARDWARE = 2
        
        # 按键标志
        self.KEYEVENTF_KEYUP = 0x0002
        self.KEYEVENTF_UNICODE = 0x0004
        # 引号配对字典
        self.quote_pairs = {
            '"': '"',
            "'": "'",
            "\u201c": "\u201d",  # 中文双引号
            "\u2018": "\u2019",  # 中文单引号
            "\u300c": "\u300d",  # 「」
            "\u300e": "\u300f",  # 『』
            "\u300a": "\u300b",  # 《》
            "\u3008": "\u3009",  # 〈〉
            "\uff08": "\uff09",  # （）
            "\u3010": "\u3011",  # 【】
            "[": "]",
            "{": "}",
            "(": ")",
            "<": ">"
        }
        
        # 格式化规则
        self.format_rules = {
            'max_consecutive_chars': 3,  # 最大连续字符数
            'max_consecutive_spaces': 1,  # 最大连续空格数
            'add_space_between_zh_en': True,  # 中英文之间添加空格
            'normalize_ellipsis': True,  # 规范化省略号
            'normalize_punctuation': True,  # 规范化标点符号
            'trim_spaces': True,  # 清理多余空格
            'keep_original_format': False,  # 保持原格式
            'auto_match_quotes': True,  # 自动匹配引号
            'auto_format_paragraphs': True,  # 自动格式化段落
            'preserve_line_breaks': True,  # 保留换行符
            'smart_punctuation': True  # 智能标点处理
        }
        
        print(f"{Fore.GREEN}输入模拟器初始化完成{Fore.RESET}")

    def _get_cursor_pos(self):
        """
        获取当前光标位置
        """
        return win32gui.GetCaretPos()

    def _get_active_window(self):
        """
        获取当前活动窗口
        """
        return win32gui.GetForegroundWindow()

    def _send_char_direct(self, char: str):
        """
        使用win32api直接发送字符（备选方案）
        """
        try:
            if char == '\n':
                win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
                time.sleep(0.001)
                win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif char == ' ':
                win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
                time.sleep(0.001)
                win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif char == '\t':
                win32api.keybd_event(win32con.VK_TAB, 0, 0, 0)
                time.sleep(0.001)
                win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                # 使用SendInput发送Unicode字符
                inputs = [
                    self._create_unicode_input(char, False),
                    self._create_unicode_input(char, True)
                ]
                return self._send_inputs(inputs)
            return True
        except Exception as e:
            print(f"{Fore.RED}直接输入出错: {str(e)}{Fore.RESET}")
            return False

    def _send_text_to_clipboard(self, text: str) -> bool:
        """
        将文本发送到剪贴板，带重试机制
        :return: 是否成功
        """
        for i in range(self.max_retries):
            try:
                # 保存当前剪贴板内容
                win32clipboard.OpenClipboard()
                try:
                    old_clipboard = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                except:
                    old_clipboard = None
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
                return True
            except Exception as e:
                if i < self.max_retries - 1:
                    print(f"{Fore.YELLOW}剪贴板访问失败，正在重试 ({i+1}/{self.max_retries}){Fore.RESET}")
                    time.sleep(0.1)  # 短暂等待后重试
                    continue
                print(f"{Fore.RED}剪贴板访问失败: {str(e)}{Fore.RESET}")
                return False
            finally:
                try:
                    win32clipboard.CloseClipboard()
                except:
                    pass
        return False

    def _paste_at_cursor(self) -> bool:
        """
        在光标位置粘贴，带重试机制
        :return: 是否成功
        """
        try:
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('V'), 0, 0, 0)
            win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return True
        except Exception as e:
            print(f"{Fore.RED}粘贴操作失败: {str(e)}{Fore.RESET}")
            return False

    def _create_unicode_input(self, char: str, up: bool = False) -> INPUT:
        """创建Unicode字符输入事件"""
        input_union = INPUT_UNION()
        input_union.ki.wVk = 0
        input_union.ki.wScan = ord(char)
        input_union.ki.dwFlags = self.KEYEVENTF_UNICODE | (self.KEYEVENTF_KEYUP if up else 0)
        input_union.ki.time = 0
        input_union.ki.dwExtraInfo = ctypes.pointer(wintypes.ULONG(0))

        input_struct = INPUT()
        input_struct.type = self.INPUT_KEYBOARD
        input_struct.union = input_union
        return input_struct

    def _create_virtual_input(self, vk_code: int, up: bool = False) -> INPUT:
        """创建虚拟键码输入事件"""
        input_union = INPUT_UNION()
        input_union.ki.wVk = vk_code
        input_union.ki.wScan = 0
        input_union.ki.dwFlags = self.KEYEVENTF_KEYUP if up else 0
        input_union.ki.time = 0
        input_union.ki.dwExtraInfo = ctypes.pointer(wintypes.ULONG(0))

        input_struct = INPUT()
        input_struct.type = self.INPUT_KEYBOARD
        input_struct.union = input_union
        return input_struct

    def _send_inputs(self, inputs: List[INPUT]) -> bool:
        """批量发送输入事件"""
        try:
            nInputs = len(inputs)
            pInputs = (INPUT * nInputs)(*inputs)
            cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
            return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize) == nInputs
        except Exception as e:
            print(f"{Fore.RED}发送输入事件失败: {str(e)}{Fore.RESET}")
            return False

    def _send_text_fast(self, text: str) -> bool:
        """快速发送文本（批量处理）"""
        try:
            # 为每个字符创建按下和释放事件
            inputs = []
            for char in text:
                if char == '\n':
                    # 回车键
                    inputs.extend([
                        self._create_virtual_input(win32con.VK_RETURN, False),
                        self._create_virtual_input(win32con.VK_RETURN, True)
                    ])
                elif char == ' ':
                    # 空格键
                    inputs.extend([
                        self._create_virtual_input(win32con.VK_SPACE, False),
                        self._create_virtual_input(win32con.VK_SPACE, True)
                    ])
                elif char == '\t':
                    # Tab键
                    inputs.extend([
                        self._create_virtual_input(win32con.VK_TAB, False),
                        self._create_virtual_input(win32con.VK_TAB, True)
                    ])
                else:
                    # 普通字符
                    inputs.extend([
                        self._create_unicode_input(char, False),
                        self._create_unicode_input(char, True)
                    ])
            
            # 批量发送所有输入事件
            if not inputs:
                return True
                
            # 分批发送，每批最多50个事件
            batch_size = 50
            for i in range(0, len(inputs), batch_size):
                batch = inputs[i:i + batch_size]
                if not self._send_inputs(batch):
                    return False
                time.sleep(0.001)  # 微小延迟，避免事件丢失
                
            return True
            
        except Exception as e:
            print(f"{Fore.RED}快速输入失败: {str(e)}{Fore.RESET}")
            return False

    def format_text(self, text: str) -> str:
        """
        格式化文本
        :param text: 要格式化的文本
        :return: 格式化后的文本
        """
        if not text or self.format_rules.get('keep_original_format', False):
            return text

        result = text

        # 处理多余空格和换行
        if self.format_rules.get('trim_spaces', True):
            if self.format_rules.get('auto_format_paragraphs', True):
                # 保留段落格式，将连续多个空行减少为一个空行
                paragraphs = re.split(r'\n\s*\n', result)
                paragraphs = [p.strip() for p in paragraphs if p.strip()]
                result = '\n\n'.join(paragraphs)
            
            # 处理每行的空格
            if self.format_rules.get('preserve_line_breaks', True):
                lines = result.split('\n')
                lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines]
                result = '\n'.join(lines)
            else:
                result = re.sub(r'\s+', ' ', result).strip()

        # 智能处理引号
        if self.format_rules.get('auto_match_quotes', True):
            result = self._match_quotes(result)

        # 处理中英文之间的空格
        if self.format_rules.get('add_space_between_zh_en', True):
            result = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9])', r'\1 \2', result)
            result = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fff])', r'\1 \2', result)

        # 规范化标点符号
        if self.format_rules.get('smart_punctuation', True):
            # 统一中文标点
            punctuation_map = {
                ',': '，',
                '.': '。',
                '?': '？',
                '!': '！',
                ':': '：',
                ';': '；',
                '(': '（',
                ')': '）',
                '[': '【',
                ']': '】'
            }
            for en, zh in punctuation_map.items():
                # 仅在中文上下文中替换英文标点
                result = re.sub(f'(?<=[\\u4e00-\\u9fff]){re.escape(en)}(?=[\\u4e00-\\u9fff])', zh, result)
            
            # 处理重复的标点符号
            result = re.sub(r'([，。！？；：、])\1+', r'\1', result)

        # 处理省略号
        if self.format_rules.get('normalize_ellipsis', True):
            result = re.sub(r'\.{3,}', '...', result)
            result = re.sub(r'。{3,}', '......', result)

        # 处理连续字符
        if self.format_rules.get('max_consecutive_chars', 3) > 0:
            max_chars = self.format_rules['max_consecutive_chars']
            pattern = r'(.)\1{' + str(max_chars) + r',}'
            result = re.sub(pattern, lambda m: m.group(1) * max_chars, result)

        return result

    def _check_quote_pairs(self, text: str) -> list:
        """
        检查文本中的引号配对情况
        :param text: 要检查的文本
        :return: 需要删除的引号位置列表
        """
        stack = []  # 用于存储待匹配的引号
        delete_positions = []  # 需要删除的引号位置
        quote_positions = {}  # 记录每种引号的位置

        # 第一遍扫描：记录所有引号的位置
        for i, char in enumerate(text):
            if char in self.quote_pairs or char in self.quote_pairs.values():
                if char not in quote_positions:
                    quote_positions[char] = []
                quote_positions[char].append(i)

        # 第二遍扫描：检查配对情况
        for i, char in enumerate(text):
            if char in self.quote_pairs:  # 左引号
                stack.append((char, i))
            elif char in self.quote_pairs.values():  # 右引号
                # 找到对应的左引号
                left_quote = None
                for left, right in self.quote_pairs.items():
                    if right == char:
                        left_quote = left
                        break

                if stack and stack[-1][0] == left_quote:
                    stack.pop()  # 匹配成功，弹出左引号
                else:
                    # 检查是否有对应的左引号在后面
                    if left_quote in quote_positions:
                        future_positions = [pos for pos in quote_positions[left_quote] if pos > i]
                        if not future_positions:  # 如果后面没有对应的左引号
                            delete_positions.append(i)  # 标记当前右引号为需要删除

        # 处理未匹配的左引号
        while stack:
            _, pos = stack.pop()
            delete_positions.append(pos)

        return sorted(delete_positions)

    def _send_backspace(self) -> bool:
        """
        发送退格键
        :return: 是否成功
        """
        try:
            inputs = [
                self._create_virtual_input(win32con.VK_BACK, False),
                self._create_virtual_input(win32con.VK_BACK, True)
            ]
            return self._send_inputs(inputs)
        except Exception as e:
            print(f"{Fore.RED}发送退格键失败: {str(e)}{Fore.RESET}")
            return False

    def type_string(self, text: str, interval: Union[float, tuple] = 0.1, 
                   encoding: str = 'utf-8', use_ime: bool = True, fast_mode: bool = False,
                   format_text: bool = True):
        """
        模拟键盘输入文本
        :param text: 要输入的文本
        :param interval: 输入间隔，可以是固定值或者范围元组(min, max)
        :param encoding: 文本编码，默认utf-8
        :param use_ime: 是否使用输入法，默认True
        :param fast_mode: 是否使用快速输入模式，默认False
        :param format_text: 是否格式化文本，默认True
        """
        try:
            # 确保文本编码正确
            if isinstance(text, bytes):
                text = text.decode(encoding)
            elif isinstance(text, str):
                text = text.encode(encoding).decode(encoding)

            # 格式化文本
            if format_text and not self.format_rules.get('keep_original_format', False):
                text = self.format_text(text)

            # 检查引号配对
            delete_positions = []
            if self.format_rules.get('auto_match_quotes', True):
                delete_positions = self._check_quote_pairs(text)

            # 记录当前窗口
            active_window = self._get_active_window()
            
            # 快速模式
            if fast_mode:
                # 分段处理，避免一次性发送太多字符
                chunk_size = 100
                current_pos = 0
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i + chunk_size]
                    if not self._send_text_fast(chunk):
                        raise Exception("快速输入失败")
                    
                    # 处理需要删除的引号
                    chunk_delete_positions = [pos - i for pos in delete_positions if i <= pos < i + chunk_size]
                    for _ in chunk_delete_positions:
                        if not self._send_backspace():
                            raise Exception("退格失败")
                        time.sleep(0.001)  # 短暂延迟确保退格成功
                    
                    if isinstance(interval, tuple):
                        time.sleep(random.uniform(interval[0], interval[1]))
                    elif interval > 0:
                        time.sleep(interval)
                return
            
            # 字符输入模式
            for i, char in enumerate(text):
                if isinstance(interval, tuple):
                    delay = random.uniform(interval[0], interval[1])
                else:
                    delay = interval

                # 检查窗口是否改变
                if active_window != self._get_active_window():
                    print(f"{Fore.YELLOW}窗口已切换，停止输入{Fore.RESET}")
                    break

                if not self._send_char_direct(char):
                    raise Exception("输入失败")

                # 如果当前位置需要删除
                if i in delete_positions:
                    time.sleep(0.001)  # 短暂延迟确保字符输入完成
                    if not self._send_backspace():
                        raise Exception("退格失败")
                    
                if delay > 0:
                    time.sleep(delay)
                    
        except Exception as e:
            print(f"{Fore.RED}输入过程出错: {str(e)}{Fore.RESET}")

    def start_continuous_input(self, text: str, interval: Union[float, tuple] = 0.1, 
                             loop: bool = True, encoding: str = 'utf-8', 
                             use_ime: bool = True, fast_mode: bool = False,
                             format_text: bool = True):
        """
        开始持续输入模式
        :param text: 要重复输入的文本
        :param interval: 输入间隔
        :param loop: 是否循环输入，False则只输入一次
        :param encoding: 文本编码，默认utf-8
        :param use_ime: 是否使用输入法，默认True
        :param fast_mode: 是否使用快速输入模式，默认False
        :param format_text: 是否格式化文本，默认True
        """
        self.running = True
        print(f"{Fore.YELLOW}{'循环' if loop else '单次'}输入模式已启动，按 'Esc' 键停止{Fore.RESET}")
        
        try:
            # 记录初始窗口
            initial_window = self._get_active_window()
            
            # 预处理文本编码
            if isinstance(text, bytes):
                text = text.decode(encoding)
            elif isinstance(text, str):
                text = text.encode(encoding).decode(encoding)
            
            # 格式化文本
            if format_text and not self.format_rules.get('keep_original_format', False):
                text = self.format_text(text)
            
            while self.running:
                if keyboard.is_pressed('esc'):
                    self.running = False
                    print(f"{Fore.YELLOW}输入已停止{Fore.RESET}")
                    break
                
                # 检查窗口是否改变
                if initial_window != self._get_active_window():
                    print(f"{Fore.YELLOW}窗口已切换，停止输入{Fore.RESET}")
                    self.running = False
                    break
                    
                self.type_string(text, interval, encoding, use_ime, fast_mode, False)  # 避免重复格式化
                
                if not loop:  # 如果是单次模式，输入完成后停止
                    self.running = False
                    print(f"{Fore.GREEN}单次输入完成{Fore.RESET}")
                    break
                elif isinstance(interval, tuple):
                    time.sleep(random.uniform(interval[0], interval[1]))
                else:
                    time.sleep(interval)
                    
        except Exception as e:
            print(f"{Fore.RED}输入出错: {str(e)}{Fore.RESET}")
            self.running = False

    def stop(self):
        """停止所有正在进行的输入操作"""
        self.running = False
        print(f"{Fore.YELLOW}已停止所有输入操作{Fore.RESET}")

    def analyze_text(self, text: str) -> dict:
        """
        分析文本，返回统计信息和潜在问题
        :param text: 要分析的文本
        :return: 包含分析结果的字典
        """
        result = {
            'stats': {},
            'issues': []
        }
        
        if not text:
            result['stats'] = {
                'total_chars': 0,
                'chars_no_spaces': 0,
                'chinese_chars': 0,
                'words': 0,
                'lines': 0
            }
            return result

        # 基本统计
        result['stats']['total_chars'] = len(text)  # 包含所有字符的总数
        result['stats']['chars_no_spaces'] = len(''.join(text.split()))  # 不包含空白字符的总数
        
        # 统计中文字符
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        result['stats']['chinese_chars'] = len(chinese_chars)
        
        # 统计行数（包括空行）
        result['stats']['lines'] = text.count('\n') + 1
        
        # 单词统计（VSCode风格）
        # 1. 将文本按空白字符分割
        # 2. 将连续的非空白字符视为一个单词
        # 3. 中文每个字符都算作一个单词
        words = []
        
        # 首先处理所有中文字符，将每个中文字符替换为"中文字符+空格"
        text_with_spaces = re.sub(r'([\u4e00-\u9fff])', r'\1 ', text)
        
        # 分割文本并过滤空字符串
        raw_words = [word.strip() for word in text_with_spaces.split()]
        words = [word for word in raw_words if word]
        
        result['stats']['words'] = len(words)
        
        # 检查问题
        # 1. 检查重复字符
        for i in range(len(text)-2):
            if text[i] == text[i+1] == text[i+2] and text[i].strip():
                result['issues'].append({
                    'type': '重复字符',
                    'position': i,
                    'content': text[i:i+3],
                    'description': f'发现连续重复字符: {text[i]}'
                })
        
        # 2. 检查不规范的空格使用
        spaces = re.finditer(r'\s{2,}', text)
        for space in spaces:
            result['issues'].append({
                'type': '多余空格',
                'position': space.start(),
                'content': space.group(),
                'description': '发现连续多个空格'
            })
        
        # 3. 检查中英文混排的空格问题
        mixed_spaces = re.finditer(r'[\u4e00-\u9fff][a-zA-Z]|[a-zA-Z][\u4e00-\u9fff]', text)
        for mixed in mixed_spaces:
            result['issues'].append({
                'type': '中英文混排',
                'position': mixed.start(),
                'content': mixed.group(),
                'description': '中英文之间建议加空格'
            })
        
        # 4. 检查标点符号使用
        punctuation_issues = re.finditer(r'[，。！？；：、][，。！？；：、]', text)
        for issue in punctuation_issues:
            result['issues'].append({
                'type': '标点符号',
                'position': issue.start(),
                'content': issue.group(),
                'description': '发现连续标点符号'
            })
        
        # 5. 检查特殊字符
        special_chars = re.finditer(r'[^\u4e00-\u9fff\u0020-\u007F\n\t]', text)
        for char in special_chars:
            result['issues'].append({
                'type': '特殊字符',
                'position': char.start(),
                'content': char.group(),
                'description': f'发现特殊字符: {char.group()}'
            })

        # 6. 检查引号配对
        delete_positions = self._check_quote_pairs(text)
        for pos in delete_positions:
            result['issues'].append({
                'type': '引号不匹配',
                'position': pos,
                'content': text[pos],
                'description': f'发现未匹配的引号: {text[pos]}'
            })
        
        return result

    def _match_quotes(self, text: str) -> str:
        """
        智能匹配引号
        :param text: 要处理的文本
        :return: 处理后的文本
        """
        if not text:
            return text

        # 将文本转换为字符列表以便修改
        chars = list(text)
        stack = []  # 存储待匹配的左引号
        to_remove = set()  # 需要删除的引号位置
        to_add = {}  # 需要添加的引号 {位置: 引号}

        # 第一遍扫描：标记不匹配的引号
        for i, char in enumerate(chars):
            if char in self.quote_pairs:  # 左引号
                stack.append((char, i))
            elif char in self.quote_pairs.values():  # 右引号
                # 找到对应的左引号
                left_quote = None
                for left, right in self.quote_pairs.items():
                    if right == char:
                        left_quote = left
                        break

                if stack and stack[-1][0] == left_quote:
                    stack.pop()  # 匹配成功
                else:
                    # 检查是否应该删除这个右引号
                    if not any(pos for q, pos in stack if self.quote_pairs[q] == char):
                        to_remove.add(i)

        # 处理未匹配的左引号
        while stack:
            quote, pos = stack.pop()
            # 在适当位置添加右引号
            next_pos = pos + 1
            while next_pos < len(chars) and chars[next_pos].isspace():
                next_pos += 1
            if next_pos < len(chars):
                to_add[next_pos] = self.quote_pairs[quote]
            else:
                to_remove.add(pos)

        # 应用修改
        # 先处理要添加的引号（从后向前）
        for pos in sorted(to_add.keys(), reverse=True):
            chars.insert(pos, to_add[pos])

        # 再处理要删除的引号（从后向前）
        for pos in sorted(to_remove, reverse=True):
            chars.pop(pos)

        return ''.join(chars)

if __name__ == "__main__":
    # 使用示例
    simulator = InputSimulator()
    
    # 基本输入示例
    print("1. 基本输入示例")
    simulator.type_string("Hello, World!", 0.1)
    
    # 随机间隔输入示例
    print("\n2. 随机间隔输入示例")
    simulator.type_string("Random Typing", (0.1, 0.3))
    
    # 组合键示例
    print("\n3. 组合键示例")
    simulator.simulate_hotkey('ctrl', 'c')
    
    # 持续输入示例
    print("\n4. 持续输入示例（按ESC停止）")
    simulator.start_continuous_input("Test ", (0.5, 1.0))