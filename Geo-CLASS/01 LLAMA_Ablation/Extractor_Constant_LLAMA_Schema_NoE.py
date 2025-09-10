# prompt for extracting major dimension of scripts, including theme, datasource and function (LLAMA, more concise)
# Entity-Schema are not include

Entity_role = r'''You are a geo-information scientist and programmer proficient in JavaScript with over 20 years of experience using GEE. You have a deep understanding of GEE scripts and can extract geoprocessing modeling information from them, including themes, data sources, functions, and their relationships.'''
Entity_task = r'Based on the provided GEE workflow script, perform the following tasks:' \
              r'1) Extracting entities from scripts.'\
              r'2) JSON Response Generation: Generate a JSON response that organizes the extracted information into a structured format according to the JSON format of the Entity reply example.' \
              r'3) Just keep Json Response, No additional explanation required.'\
              r'The GEE workflow script to be analyzed is as follows:'


Entity_reply_example = r"""
```json
{
  "Theme": ["Detailed thematic analysis of the script focusing on its primary geoprocessing objectives."],
  "DataSource": ["users/ak_glaciers/points_w_ids_OR", "COPERNICUS/S1_GRD"],
  "Function": ["Detailed description of the first geoprocessing modeling operation", "Detailed description of the second geoprocessing modeling operation"]
}
```
"""


# --------------- constants for relation extraction  ---------------
Relation_role = r'''You are a professional Geo-information scientist and programmer good at Javascript. 
You have been using GEE for more than 20 years and are good at using the Code Editor in GEE to write scripts in javascript to handle geoprocessing modeling tasks. 
At the same time, you also have a deep understanding of GEE scripts and can parse and summarize geoprocessing modeling information in them, including themes, data sources, functions, time scopes, spatial scopes, and the relationships between them. 
You are very familiar with the connotation and calling relationships of APIs in GEE scripts, and are good at code summary and knowledge extraction (including entity recognition and relationship extraction).'''

Relation_task = r'Objective: Utilize the entity recognition results from the previous step to analyze and extract relationships among identified entities within the script. Focus on linking data sources to their corresponding functions.' \
                r'Input Data: Use the entity recognition results provided below as the basis for relationship extraction.' \
                r'Analysis Goals: Identify and establish relationships between data sources and the functions they support.analyze and extract the correspondence between the data sources and functions,' \
                r'JSON Response Generation: Generate a JSON response that organizes the extracted information into a structured format according to the JSON format of the Relation reply example.' \
                r'Just keep Json Response, No additional explanation required.' \
                r'The entity results extracted in the previous step are as follows: '


Relation_reply_example = """
```json
{
    "relation_1": {
        "DataSource": ["users/ak_glaciers/points_w_ids_OR"],
        "Function": ["Detailed description of the first related geoprocessing modeling operation"]
    },
    "relation_2": {
        "DataSource": ["COPERNICUS/S1_GRD"],
        "Function": ["Detailed description of the second related geoprocessing modeling operation"]
    }
}
```
"""

Relation_requirement = [
    # Preliminary Note
    'Let us think step by step.',
    'Do not modify the existing descriptions of entities.',
    'Exclude "theme" entities from this relationship extraction task.',
    # Comprehensive Extraction
    'When extracting relationships, ensure global variable references are considered.',
    'Extract the relationships between data sources and their corresponding and functions as comprehensively as possible.',
    # Dimensional Consistency
    'Ensure that the collective dimensions (data sources, functions) across all relationship collections align with the initial entity recognition results.',
    # Uniqueness and Repeatability
    'A data source should not appear in more than one relationship collection.',
    'Mandatorily group data sources into the same relationship collection if they share identical functions. This grouping is compulsory and must be clearly reflected in the output.',
    # Multiplicity and Recurrence
    'Allow multiple functions within a single relationship collection.',
    'Different functions may recur across various relationship collections.',
    # Code structure: Nested Invocations and Dependencies
    'Account for nested invocations and long-range dependencies when analyzing the relationships involving data sources and functions.',
    'Consider the entire workflow within the script to determine if indirect relationships between data sources and functions should also be recorded, especially in cases where data passes through multiple stages or transformations.',
    'Document the chain of usage among functions and data sources, considering sequential dependencies. For example, if Function A relies on Data Source X and Functions B and C use outputs from Function A, then Functions A, B, and C should all be linked to Data Source X.',
    'If a function utilizes variables derived from a data source, include this function in the relationship list for that data source. For instance, if function A uses variable M, which is derived from data source X, then include function A in the relationship list for data source X.'
    # Handling Absence of Clear Relationships
    'If no clear relationship can be identified between a data source and functions, set the corresponding key in the JSON output to "None".'
    # Output Specification
    'Generate the output as a JSON formatted according to the example provided, focusing exclusively on the structure without any explanatory text.',
]
Relation_requirement_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(Relation_requirement)])