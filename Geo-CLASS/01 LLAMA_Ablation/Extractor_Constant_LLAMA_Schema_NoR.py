# prompt for extracting major dimension of scripts, including theme, datasource and function (LLAMA, more concise)
# Relation-Schema are not include

Entity_role = r'''You are a geo-information scientist and programmer proficient in JavaScript with over 20 years of experience using GEE. You have a deep understanding of GEE scripts and can extract geoprocessing modeling information from them, including themes, data sources, functions, and their relationships.'''
Entity_task = r'Based on the provided GEE workflow script, perform the following tasks:' \
              r'1) Script Summary: Provide an overall summary of the script, including details about "what topic"(themes), "what data" (data sources), and "what did" (actions and processes described in the script).' \
              r'2) Theme Analysis: Summarize the central themes of the script, focusing on the main geoprocessing modeling purposes and application topics.' \
              r'3) Data Sources Extraction: Identify and list all the data sources referenced in the script.' \
              r'4) Function Summary: List and describe the geoprocessing modeling and geoanalysis operations used in the script, explaining their role and usage within the workflow.' \
              r'5) JSON Response Generation: Generate a JSON response that organizes the extracted information into a structured format according to the JSON format of the Entity reply example.' \
              r'6) Just keep Json Response, No additional explanation required.'\
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

Entity_requirement = [
    'Let us think step by step.',
    # Initial Setup
    'Begin by thoroughly examining both the code content and the annotations within the script to gather comprehensive knowledge.',
    # Theme Specification
    'Define "theme" as the specific research or analysis focus field. Aim to identify and mention the most specific category possible, such as "corn" rather than generalizing to "vegetation".',
    'Summarize script themes clearly and concretely, ensuring each description does not exceed 10 words.',
    'If no theme is discernible, set the “Theme” key in the output to “None”.'
    # Function Analysis
    'Define "function" as a specific operation within geoprocessing modeling, such as "image collection filter."',
    'List and describe the actions (referred to as "functions") within the script that perform geoprocessing tasks. Keep each description concise, not exceeding 10 words.',
    'When summarizing functions, avoid using the code language in the script, including APIs or function names. Instead, use natural language for descriptions. Ensure that the explanations translate technical operations into easily understandable terms.',
    'If no function is identifiable, set the “Function” key in the output to “None”.',
    # Data Source Analysis
    'Analyze the data source paths within the script to extract and record any critical information they contain. Specifically, look for details related to the theme, function, time scope, or spatial scope of the geoprocessing tasks. When such information is identified, document it under the corresponding keys in the output, ensuring all relevant connections between data sources and these aspects are captured and clearly presented.',
    'Retain the original form of data source paths in the output.',
    'Paths beginning with "users/" or "projects/" are highly likely to be data sources and should be specifically considered for inclusion.',
    'Exclude data source paths that appear only in comments from the output.',
    'Omit data sources prefixed with "ft:" from the "DataSource" key in the output.',
    'Record only those data sources in the output that are directly engaged in executing geoprocessing functions within the script.',
    'If there are no identifiable data sources in the script, set the “DataSource” key in the output to “None”.',
    # Output Specification:
    'Generate a JSON response structured exactly as shown in the reply example. Exclude all explanatory or reasoning text from the output, formatting only the results as JSON.',
]
Entity_requirement_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(Entity_requirement)])


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