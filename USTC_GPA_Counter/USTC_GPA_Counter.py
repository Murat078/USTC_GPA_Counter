import pandas as pd

def score_to_gpa(score):
    """
    中科大本科4.3分制成绩转绩点
    返回值说明：
    - 数字：对应单科绩点，参与GPA计算
    - None：二等级制/无效成绩，不参与GPA计算
    """
    # 二等级制识别：直接返回None，不参与计算
    if isinstance(score, str):
        score_str = score.strip()
        # 覆盖常见的二等级表述
        pass_list = ['通过', '不通过', '合格', '不合格', 'P', 'F', 'NP']
        if score_str in pass_list:
            return None
        score_str = score_str.upper()
    else:
        score_str = str(score).strip()

    # 五等级制映射表
    grade_map = {
        'A+': 4.3, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.5, 'D': 1.3, 'D-': 1.0,
        'F': 0.0
    }

    # 处理等级制输入
    if isinstance(score, str):
        if score_str in grade_map:
            return grade_map[score_str]
        # 尝试转为百分制数字
        try:
            score_num = float(score_str)
        except ValueError:
            return None
    else:
        score_num = float(score)

    # 百分制区间转绩点
    if score_num > 100 or score_num < 0:
        return None
    elif score_num >= 95:
        return 4.3
    elif score_num >= 90:
        return 4.0
    elif score_num >= 85:
        return 3.7
    elif score_num >= 82:
        return 3.3
    elif score_num >= 78:
        return 3.0
    elif score_num >= 75:
        return 2.7
    elif score_num >= 72:
        return 2.3
    elif score_num >= 68:
        return 2.0
    elif score_num >= 65:
        return 1.7
    elif score_num >= 64:
        return 1.5
    elif score_num >= 61:
        return 1.3
    elif score_num >= 60:
        return 1.0
    else:
        return 0.0


def calculate_gpa_from_excel(input_path, output_path):
    # 读取Excel第一个工作表
    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"读取Excel失败：{e}")
        return

    # 校验必要列
    required_cols = ['学分', '成绩']
    for col in required_cols:
        if col not in df.columns:
            print(f"Excel缺少核心列：{col}，请检查列名")
            return

    # 计算单科绩点，新增标记列
    df['对应绩点'] = df['成绩'].apply(score_to_gpa)
    df['是否计入GPA'] = df['对应绩点'].apply(lambda x: '是' if x is not None else '否（二等级制）')

    # 筛选计入GPA的有效课程
    valid_df = df.dropna(subset=['对应绩点'])
    valid_df = valid_df[valid_df['学分'] > 0]

    # 统计二等级制课程
    pass_courses = df[df['对应绩点'].isna()]
    pass_credit = pass_courses['学分'].sum()

    if len(valid_df) == 0:
        print("没有找到可计入GPA的有效课程")
        return

    # 加权计算总GPA
    total_weighted = (valid_df['学分'] * valid_df['对应绩点']).sum()
    total_credit = valid_df['学分'].sum()
    final_gpa = total_weighted / total_credit

    # 输出结果
    print("=" * 50)
    print("      中国科学技术大学 GPA 计算结果")
    print("=" * 50)
    print(f"总课程数：{len(df)} 门")
    print(f"计入GPA课程数：{len(valid_df)} 门")
    print(f"不计入GPA课程数：{len(pass_courses)} 门（二等级制：军事理论/技能等）")
    print(f"不计入GPA的总学分：{pass_credit:.1f}")
    print(f"参与计算总学分：{total_credit:.1f}")
    print(f"最终 GPA：{final_gpa:.3f}")
    print("=" * 50)

    # 保存结果文件
    df.to_excel(output_path, index=False)
    print(f"\n详细计算结果已保存到：{output_path}")
    print("（文件中包含每门课的对应绩点和是否计入GPA的标记）")


if __name__ == "__main__":
    # 修改为你的文件路径
    INPUT_FILE = "成绩.xlsx"    # 你的成绩表路径
    OUTPUT_FILE = "GPA计算结果.xlsx"  # 输出结果路径

    calculate_gpa_from_excel(INPUT_FILE, OUTPUT_FILE)