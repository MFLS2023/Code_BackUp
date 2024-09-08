
import kaiwu as kw
# 初始化SDK授权（替换为有效的user_id和sdk_code）
kw.license.init(user_id="39876919071617026", sdk_code="AE2byG82bksgdel2YRJN0ajlRfARWK")

import numpy as np
import kaiwu.cim as kc
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['SimHei']

# 定义问题参数
months = 5 * 12  # 5年
hours_per_month = 20 * 8  # 每月20天，每天8小时
fuel_price = 7  # 升/元
ore_price = 20  # 立方米/元
required_types = 5  # 至少需要的挖掘机类型数
penalty_type_count = 1e9  # 不满足挖掘机类型数的惩罚
budget = 4000 * 1e4  # 预算4000万元
penalty_budget = 1e2  # 超出预算的惩罚

# 插入实际的挖掘机参数
excavator_params = {
    "bucket_capacity": np.array([0.9, 1.2, 1.8, 2.1, 2.6, 3.5, 5, 6, 8, 10]),  #挖掘机斗容
    "efficiency": np.array([190, 175, 165, 150, 140, 130, 120, 110, 105, 100]),  #作业效率
    "fuel_consumption": np.array([28, 30, 34, 38, 42, 50, 60, 75, 90, 100]),  #油耗
    "purchase_price": np.array([100, 140, 200, 320, 440, 500, 640, 760, 860, 1000]) * 1e4,  #采购价格（万元）
    "labor_cost": np.array([7000, 7500, 8500, 9000, 10000, 12000, 13000, 16000, 18000, 20000]),  #人工成本（元）
    "maintenance_cost": np.array([1000, 1500, 2000, 3000, 5000, 8000, 10000, 13000, 15000, 18000])  #维护成本（元）
}

# 计算每个挖掘机的总运营成本和收入，并收集数据用于绘图
costs = []
revenues = []
def calculate_costs_and_revenue(excavator_idx):
    fuel_cost = excavator_params["fuel_consumption"][excavator_idx] * fuel_price * hours_per_month * months
    labor_cost = excavator_params["labor_cost"][excavator_idx] * months
    maintenance_cost = excavator_params["maintenance_cost"][excavator_idx] * months
    purchase_cost = excavator_params["purchase_price"][excavator_idx]

    total_cost = fuel_cost + labor_cost + maintenance_cost + purchase_cost
    total_revenue = (excavator_params["bucket_capacity"][excavator_idx] *
                     excavator_params["efficiency"][excavator_idx] *
                     ore_price * hours_per_month * months)

    costs.append(total_cost)
    revenues.append(total_revenue)
    return total_cost, total_revenue

# 初始化QUBO矩阵以设置问题
num_variables = len(excavator_params["bucket_capacity"])
Q = np.zeros((num_variables, num_variables))

# 设置QUBO问题
for i in range(num_variables):
    calculate_costs_and_revenue(i)  # 更新：在此调用同时收集成本和收益数据
    Q[i, i] = costs[i] - revenues[i]
# 添加类型数量的约束
for i in range(num_variables):
    for j in range(i + 1, num_variables):
        Q[i, j] = penalty_type_count
        Q[j, i] = penalty_type_count  # 确保矩阵是对称的

# 添加预算约束
total_purchase_cost = np.sum(excavator_params["purchase_price"])
if total_purchase_cost > budget:
    for i in range(num_variables):
        Q[i, i] += penalty_budget * (total_purchase_cost - budget) / budget

matching_matrix = np.array([
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],  # 挖掘机1
    [3, 3, 3, 2, 0, 0, 0, 0, 0, 0],  # 挖掘机2
    [4, 3, 3, 3, 2, 0, 0, 0, 0, 0],  # 挖掘机3
    [5, 4, 3, 3, 3, 2, 0, 0, 0, 0],  # 挖掘机4
    [0, 5, 4, 3, 3, 3, 2, 2, 0, 0],  # 挖掘机5
    [0, 0, 5, 4, 3, 3, 3, 2, 2, 0],  # 挖掘机6
    [0, 0, 5, 5, 4, 3, 3, 3, 3, 2],  # 挖掘机7
    [0, 0, 0, 5, 5, 4, 3, 3, 3, 3],  # 挖掘机8
    [0, 0, 0, 0, 5, 5, 4, 3, 3, 3],  # 挖掘机9
    [0, 0, 0, 0, 0, 5, 5, 4, 3, 3]   # 挖掘机10
])

# 惩罚系数，如果不满足挖掘机与矿车的匹配条件
penalty_matching = 1e9

# 填充 QUBO 矩阵以添加匹配约束
for i in range(num_variables):
    for j in range(num_variables):
        # 添加不满足匹配条件的惩罚
        if matching_matrix[i, j] > 0:
            Q[i, i] += penalty_matching


# 输出矩阵Q
print("QUBO矩阵:")
print(Q)

# 使用 Kaiwu 的优化器解决问题
solver = kc.SimulatedCIMOptimizer(pump=1.5, noise=0.1, laps=100, delta_time=0.01, normalization=0.5, iterations=10)

# 解决QUBO问题
solution = solver.solve(Q)  # 直接获取解向量

# 分析解决方案
purchased_excavators = [idx for idx, value in enumerate(solution[0]) if value == 1]
excavator_count = {idx: purchased_excavators.count(idx) for idx in set(purchased_excavators)}
total_cost = sum(costs[idx] for idx in purchased_excavators)
total_revenue = sum(revenues[idx] for idx in purchased_excavators)
total_profit = total_revenue - total_cost

# 绘制成本和收入变化图
plt.figure(figsize=(10, 6))
plt.plot(costs, label='总成本（元）')
plt.plot(revenues, label='总收入（元）')
plt.title('五年内挖掘机的成本与收入变化')
plt.xlabel('挖掘机索引')
plt.ylabel('金额（元）')
plt.legend()
plt.show()

# 输出购买的挖掘机种类及数量
print(f"购买的挖掘机类型及数量: {excavator_count}")
print(f"总利润: {total_profit}")

# 检查至少拥有5种类型的挖掘机的约束
if len(excavator_count) < required_types:
    print("违反约束：购买的挖掘机类型少于5种。")
else:
    print("满足挖掘机种类数量要求。")