"""
我的音乐数据分析项目 - 修复版
作者：[你的名字]
日期：2024年
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def 创建示例数据():
    """如果CSV文件不存在，创建示例数据"""
    数据 = {
        '歌曲名称': ['孤勇者', '起风了', '月光', '泡沫', '平凡之路', 
                  '七里香', '后来', '成都', '野狼disco', '晴天'],
        '歌手': ['陈奕迅', '买辣椒也用券', '胡彦斌', '邓紫棋', '朴树', 
                '周杰伦', '刘若英', '赵雷', '宝石Gem', '周杰伦'],
        '流派': ['流行', '流行', '古风', '流行', '民谣', 
                '流行', '流行', '民谣', '说唱', '流行'],
        '播放次数': [156, 89, 120, 200, 145, 180, 95, 110, 75, 220],
        '发行年份': [2021, 2017, 2007, 2012, 2014, 2004, 1999, 2016, 2019, 2003]
    }
    
    df = pd.DataFrame(数据)
    # 保存为UTF-8编码
    df.to_csv('我的歌单.csv', index=False, encoding='utf-8-sig')
    print("已创建示例CSV文件：我的歌单.csv")
    return df

def 加载数据(文件名='我的歌单.csv'):
    """从CSV文件加载音乐数据，自动检测编码"""
    if not os.path.exists(文件名):
        print(f"文件 {文件名} 不存在，创建示例数据...")
        return 创建示例数据()
    
    # 尝试不同的编码
    编码列表 = ['utf-8-sig', 'gbk', 'gb2312', 'utf-8', 'latin1']
    
    for 编码 in 编码列表:
        try:
            print(f"尝试使用 {编码} 编码加载...")
            df = pd.read_csv(文件名, encoding=编码)
            print(f"✓ 成功使用 {编码} 编码加载数据")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"编码 {编码} 失败: {e}")
    
    # 如果所有编码都失败，创建新文件
    print("所有编码尝试失败，创建新CSV文件...")
    return 创建示例数据()

def 数据分析(df):
    """对音乐数据进行基本分析"""
    print("=" * 40)
    print("🎵 音乐数据分析报告 🎵")
    print("=" * 40)
    print(f"📊 歌单歌曲总数: {len(df)}")
    print(f"🏆 播放最多的歌曲: {df.loc[df['播放次数'].idxmax(), '歌曲名称']} "
          f"(播放 {df['播放次数'].max()} 次)")
    print(f"📈 平均播放次数: {df['播放次数'].mean():.1f}")
    print(f"🎭 音乐流派种类: {df['流派'].nunique()}")
    print(f"📅 最早发行年份: {df['发行年份'].min()}")
    print(f"📅 最晚发行年份: {df['发行年份'].max()}")
    print("=" * 40)
    
    return df

def 创建可视化(df):
    """创建两个可视化图表"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 图表1：各歌曲播放次数（柱状图）
    颜色列表 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
               '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
    
    bars = axes[0].bar(range(len(df)), df['播放次数'], 
                      color=颜色列表[:len(df)],
                      edgecolor='black', linewidth=1.5)
    axes[0].set_title('歌曲播放次数对比', fontsize=16, fontweight='bold', pad=20)
    axes[0].set_ylabel('播放次数', fontsize=14)
    axes[0].set_xlabel('歌曲名称', fontsize=14)
    axes[0].set_xticks(range(len(df)))
    axes[0].set_xticklabels(df['歌曲名称'], rotation=30, ha='right', fontsize=11)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    
    # 在柱子上添加数值
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold')
    
    # 图表2：流派分布（饼图）
    流派统计 = df['流派'].value_counts()
    饼图颜色 = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#C5E1A5']
    
    wedges, texts, autotexts = axes[1].pie(
        流派统计.values, 
        labels=流派统计.index,
        autopct='%1.1f%%',
        colors=饼图颜色[:len(流派统计)],
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # 美化百分比文本
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    axes[1].set_title('音乐流派分布', fontsize=16, fontweight='bold', pad=20)
    
    plt.suptitle('我的音乐听歌习惯分析', fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    # 保存图表
    图表文件名 = '音乐分析结果.png'
    plt.savefig(图表文件名, dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print(f"✅ 可视化图表已保存为 '{图表文件名}'")
    return 图表文件名

def 保存分析报告(df, 文件名='分析报告.txt'):
    """将分析结果保存到文本文件"""
    with open(文件名, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write(" " * 15 + "🎵 音乐数据分析报告 🎵\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"📊 歌单歌曲总数: {len(df)} 首\n")
        f.write(f"🏆 播放最多的歌曲: {df.loc[df['播放次数'].idxmax(), '歌曲名称']} ")
        f.write(f"(播放 {df['播放次数'].max()} 次)\n")
        f.write(f"📈 平均播放次数: {df['播放次数'].mean():.1f} 次\n")
        f.write(f"🎭 音乐流派种类: {df['流派'].nunique()} 种\n")
        f.write(f"📅 年份范围: {df['发行年份'].min()} - {df['发行年份'].max()}\n\n")
        
        f.write("-" * 50 + "\n")
        f.write("详细歌曲列表:\n")
        f.write("-" * 50 + "\n")
        
        for index, row in df.sort_values('播放次数', ascending=False).iterrows():
            f.write(f"{index+1:2d}. {row['歌曲名称']:10s} - {row['歌手']:12s} ")
            f.write(f"({row['流派']:5s}, 发行:{row['发行年份']}, ")
            f.write(f"播放:{row['播放次数']:3d}次)\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("生成时间: 2024年\n")
        f.write("=" * 50 + "\n")
    
    print(f"✅ 分析报告已保存为 '{文件名}'")

def 主函数():
    """主函数，运行整个分析流程"""
    print("=" * 50)
    print("开始音乐数据分析项目...")
    print("=" * 50 + "\n")
    
    try:
        # 1. 加载数据
        print("📁 步骤1: 加载数据...")
        数据 = 加载数据()
        print(f"✅ 成功加载 {len(数据)} 条记录\n")
        
        # 2. 数据分析
        print("📊 步骤2: 数据分析...")
        数据分析(数据)
        print()
        
        # 3. 创建可视化
        print("📈 步骤3: 创建可视化图表...")
        创建可视化(数据)
        print()
        
        # 4. 保存报告
        print("💾 步骤4: 生成分析报告...")
        保存分析报告(数据)
        print()
        
        print("=" * 50)
        print("🎉 项目完成！生成的文件：")
        print("   1. 音乐分析结果.png (可视化图表)")
        print("   2. 分析报告.txt (详细分析报告)")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 出现错误: {e}")
        print("请检查：1. 文件是否存在 2. 文件编码是否正确")

if __name__ == "__main__":
    主函数()
