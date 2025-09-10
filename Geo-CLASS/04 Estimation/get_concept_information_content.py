# 根据本体结构计算语料库中概念的内容信息量
import json
import math
import copy

# 保存数据到JSON文件的函数
def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 加载本体数据
with open("F:/Knowledge Extraction_v2/03 SLM_Standerlization/GCMD.json", 'r', encoding='utf-8') as file:
    ontology = json.load(file)

# 直接祖先字典
direct_ancestors = {}
# 信息内容字典
concept_information_content = {}


def fill_ancestors(ontology, concept, parent=None, ancestors={}):
    if parent:
        ancestors[concept] = [parent]
    if concept not in ancestors:
        ancestors[concept] = []
    if isinstance(ontology.get(concept, {}), dict):
        for child in ontology[concept]:
            fill_ancestors(ontology[concept], child, concept, ancestors)


root_concept = next(iter(ontology))  # 假设根节点是最上层的键
root_concept_data = {"Root Concept": root_concept}
save_json(root_concept_data, 'root_concept_theme.json')
fill_ancestors(ontology, root_concept, None, direct_ancestors)
save_json(direct_ancestors, 'direct_ancestors_theme.json')


# 计算总节点数
def count_all_nodes(ontology):
    count = 1  # 计算当前节点
    for child in ontology.values():
        if isinstance(child, dict):
            count += count_all_nodes(child)  # 递归计算子节点
    return count

# 获取所有叶子节点
def get_all_leaves_set(ontology):
    leaves = set()
    for concept, children in ontology.items():
        if isinstance(children, dict):
            if not children:  # 如果子字典为空，是叶节点
                leaves.add(concept)
            else:  # 否则递归查找叶节点
                leaves.update(get_all_leaves_set(children))
    return leaves

# 获取概念的最大深度
def get_concept_max_depth(concept, direct_ancestors, ontology_root_concept):
    concept_paths = get_paths_to_root(concept, direct_ancestors, ontology_root_concept)
    return max([len(x) for x in concept_paths])

# 获取最大深度
def get_max_depth(direct_ancestors, ontology, ontology_root_concept):
    all_leaves_list = list(get_all_leaves_set(ontology))
    if not all_leaves_list:  # 如果没有叶节点
        return 0  # 返回默认深度
    all_leaves_max_depth = [get_concept_max_depth(leaf, direct_ancestors, ontology_root_concept) for leaf in all_leaves_list]
    return max(all_leaves_max_depth)

# 获取概念的叶子节点数
def get_concept_leaves_num(concept, ontology):
    def count_leaves(subtree):
        if not subtree:
            return 1
        return sum(count_leaves(child) for child in subtree.values())
    return count_leaves(ontology[concept])

# 获取到根节点的所有路径
def get_paths_to_root(concept, direct_ancestors, ontology_root_concept):
    paths = []
    path = [concept]
    while path[-1] != ontology_root_concept:
        parent = direct_ancestors.get(path[-1], [])
        if not parent:
            break
        path.append(parent[0])
    paths.append(path)
    return paths

# 计算信息内容
def get_information_content(concept_depth, max_depth, hypernyms_num, max_nodes, leaves_num, max_leaves_num):
    f_depth = math.log2(concept_depth) / math.log2(max_depth)
    f_hypernyms = math.log2(hypernyms_num + 1) / math.log2(max_nodes)
    f_leaves = math.log2(leaves_num + 1) / math.log2(max_leaves_num + 1)
    return f_depth * (1 - f_leaves) + f_hypernyms

# 计算所有概念的信息内容
max_nodes = count_all_nodes(ontology)
max_leaves_num = len(get_all_leaves_set(ontology))
max_depth = get_max_depth(direct_ancestors, ontology, root_concept)

# print("Max nodes:", max_nodes)
# print("Max leaves:", max_leaves_num)
# print("Max depth:", max_depth)

if max_nodes == 0 or max_leaves_num == 0:
    raise Exception("Critical error: No nodes or leaves found in ontology. Check the ontology structure.")

# 递归计算信息内容
def calculate_info_content_recursively(ontology, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num):
    for concept, children in ontology.items():
        if isinstance(children, dict):
            # 如果是中间节点，递归计算
            if children:
                calculate_info_content_recursively(children, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num)
            # 计算当前概念的信息内容
            concept_depth = get_concept_max_depth(concept, direct_ancestors, root_concept)
            hypernyms_num = len(direct_ancestors.get(concept, []))
            leaves_num = get_concept_leaves_num(concept, ontology)
            concept_ic = get_information_content(concept_depth, max_depth, hypernyms_num, max_nodes, leaves_num, max_leaves_num)
            concept_information_content[concept] = concept_ic

# 初始化并开始计算
calculate_info_content_recursively(ontology, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num)
save_json(concept_information_content, 'concept_information_content_theme.json')
