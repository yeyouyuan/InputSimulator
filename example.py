from input_simulator import InputSimulator
import time

def main():
    # 创建模拟器实例
    simulator = InputSimulator()
    
    print("输入模拟器示例程序")
    print("==================")
    
    while True:
        print("\n请选择要测试的功能：")
        print("1. 固定间隔输入文本")
        print("2. 随机间隔输入文本")
        print("3. 模拟组合键")
        print("4. 持续输入模式")
        print("0. 退出程序")
        
        choice = input("\n请输入选项（0-4）: ")
        
        if choice == "1":
            text = input("请输入要模拟输入的文本: ")
            print("3秒后开始输入...")
            time.sleep(3)
            simulator.type_string(text, 0.1)
            
        elif choice == "2":
            text = input("请输入要模拟输入的文本: ")
            print("3秒后开始输入...")
            time.sleep(3)
            simulator.type_string(text, (0.1, 0.3))
            
        elif choice == "3":
            print("可用的组合键示例：ctrl+c, ctrl+v, alt+tab")
            keys = input("请输入组合键（用+号分隔，如ctrl+c）: ").split("+")
            print("3秒后执行...")
            time.sleep(3)
            simulator.simulate_hotkey(*keys)
            
        elif choice == "4":
            text = input("请输入要持续输入的文本: ")
            print("3秒后开始持续输入，按ESC键停止...")
            time.sleep(3)
            simulator.start_continuous_input(text, (0.5, 1.0))
            
        elif choice == "0":
            print("程序已退出")
            break
            
        else:
            print("无效的选项，请重新选择")

if __name__ == "__main__":
    main()