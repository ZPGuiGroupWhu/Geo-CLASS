# Calculate the content information of concepts in the corpus based on the ontology structure
import json
import math
import copy

# Function to save data to JSON file
def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Loading ontology data
# with open("./03 SLM_Standerlization/Function_Dictionary.txt", 'r', encoding='utf-8') as file:
with open("./03 SLM_Standerlization/GCMD.json", 'r', encoding='utf-8') as file:
    ontology = json.load(file)

# Direct Ancestor Dictionary
direct_ancestors = {}
# Information Content Dictionary
concept_information_content = {}


def fill_ancestors(ontology, concept, parent=None, ancestors={}):
    if parent:
        ancestors[concept] = [parent]
    if concept not in ancestors:
        ancestors[concept] = []
    if isinstance(ontology.get(concept, {}), dict):
        for child in ontology[concept]:
            fill_ancestors(ontology[concept], child, concept, ancestors)


root_concept = next(iter(ontology))  # Assume the root node is the top-level key
root_concept_data = {"Root Concept": root_concept}
# save_json(root_concept_data, 'root_concept_function.json')
save_json(root_concept_data, 'root_concept_theme.json')
fill_ancestors(ontology, root_concept, None, direct_ancestors)
# save_json(direct_ancestors, 'direct_ancestors_function.json')
save_json(direct_ancestors, 'direct_ancestors_theme.json')


# Calculate the total number of nodes
def count_all_nodes(ontology):
    count = 1  # Calculate the current node
    for child in ontology.values():
        if isinstance(child, dict):
            count += count_all_nodes(child)  # Recursively evaluate child nodes
    return count

# Get all leaf nodes
def get_all_leaves_set(ontology):
    leaves = set()
    for concept, children in ontology.items():
        if isinstance(children, dict):
            if not children:  # If the sub-dictionary is empty, it is a leaf node
                leaves.add(concept)
            else:  # Otherwise, recursively search for leaf nodes
                leaves.update(get_all_leaves_set(children))
    return leaves

# Get the maximum depth of concepts
def get_concept_max_depth(concept, direct_ancestors, ontology_root_concept):
    concept_paths = get_paths_to_root(concept, direct_ancestors, ontology_root_concept)
    return max([len(x) for x in concept_paths])

# Get the maximum depth
def get_max_depth(direct_ancestors, ontology, ontology_root_concept):
    all_leaves_list = list(get_all_leaves_set(ontology))
    if not all_leaves_list:  # If there is no leaf node
        return 0  # Return to default depth
    all_leaves_max_depth = [get_concept_max_depth(leaf, direct_ancestors, ontology_root_concept) for leaf in all_leaves_list]
    return max(all_leaves_max_depth)

# Get the number of leaf nodes of a concept
def get_concept_leaves_num(concept, ontology):
    def count_leaves(subtree):
        if not subtree:
            return 1
        return sum(count_leaves(child) for child in subtree.values())
    return count_leaves(ontology[concept])

# Get all paths to the root node
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

# Computing information content
def get_information_content(concept_depth, max_depth, hypernyms_num, max_nodes, leaves_num, max_leaves_num):
    f_depth = math.log2(concept_depth) / math.log2(max_depth)
    f_hypernyms = math.log2(hypernyms_num + 1) / math.log2(max_nodes)
    f_leaves = math.log2(leaves_num + 1) / math.log2(max_leaves_num + 1)
    return f_depth * (1 - f_leaves) + f_hypernyms

# Compute the information content of all concepts
max_nodes = count_all_nodes(ontology)
max_leaves_num = len(get_all_leaves_set(ontology))
max_depth = get_max_depth(direct_ancestors, ontology, root_concept)

# print("Max nodes:", max_nodes)
# print("Max leaves:", max_leaves_num)
# print("Max depth:", max_depth)

if max_nodes == 0 or max_leaves_num == 0:
    raise Exception("Critical error: No nodes or leaves found in ontology. Check the ontology structure.")

# Recursively calculate information content
def calculate_info_content_recursively(ontology, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num):
    for concept, children in ontology.items():
        if isinstance(children, dict):
            # If it is an intermediate node, recursively calculate
            if children:
                calculate_info_content_recursively(children, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num)
            # Calculate the information content of the current concept
            concept_depth = get_concept_max_depth(concept, direct_ancestors, root_concept)
            hypernyms_num = len(direct_ancestors.get(concept, []))
            leaves_num = get_concept_leaves_num(concept, ontology)
            concept_ic = get_information_content(concept_depth, max_depth, hypernyms_num, max_nodes, leaves_num, max_leaves_num)
            concept_information_content[concept] = concept_ic

# Initialize and start calculation
calculate_info_content_recursively(ontology, direct_ancestors, root_concept, max_depth, max_nodes, max_leaves_num)
# save_json(concept_information_content, 'concept_information_content_function.json')
save_json(concept_information_content, 'concept_information_content_theme.json')
