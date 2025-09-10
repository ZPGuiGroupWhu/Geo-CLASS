# import os
# import csv
#
#
# def process_files(directory, batch_size=500):
#     function_count = 0
#     error_count = 0
#     error_files = []
#     file_counter = 0
#     function_id = 1
#     function_relations = []
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     data = eval(file.read())
#
#                     for relation_key in data.keys():
#                         # Check if 'DataSource' and 'Function' keys exist
#                         if 'DataSource' in data[relation_key] and 'Function' in data[relation_key]:
#                             data_sources = data[relation_key]['DataSource']
#                             functions = data[relation_key]['Function']
#
#                             # Create pairs of Head_Entity and Tail_Entity
#                             for function in functions:
#                                 for data_source in data_sources:
#                                     writer.writerow({
#                                         'Relation_ID': relation_id,
#                                         'Script_ID': script_id,
#                                         'Head_Entity': function,
#                                         'Relation_Type': 'actOn',
#                                         'Tail_Entity': data_source
#                                     })
#                                     relation_id += 1
#                         else:
#                             # Log information about the file and missing keys
#                             missing_keys = []
#                             if 'DataSource' not in data[relation_key]:
#                                 missing_keys.append('DataSource')
#                             if 'Function' not in data[relation_key]:
#                                 missing_keys.append('Function')
#                             print(
#                                 f"File '{filename}' in relation '{relation_key}' is missing keys: {', '.join(missing_keys)}")
#
#                     for key in data:
#                         functions = data[key].get('Function', [])
#                         if isinstance(functions, list):
#                             for func in functions:
#                                 function_relations.append([function_id, filename, key, func])
#                                 function_id += 1
#                             function_count += len(functions)
#                         else:
#                             function_relations.append([function_id, filename, key, functions])
#                             function_id += 1
#                             function_count += 1
#
#             except Exception as e:
#                 error_count += 1
#                 error_files.append((file_path, str(e)))
#
#             file_counter += 1
#             if file_counter % batch_size == 0:
#                 print(f"Processed {file_counter} files so far:")
#                 print(f"Total Function entries: {function_count}")
#                 print(f"Total errors: {error_count}")
#                 if error_count > 0:
#                     print("Error details:")
#                     for error_file, error_message in error_files:
#                         print(f"File: {error_file} - Error: {error_message}")
#
#     return function_count, error_count, error_files, function_relations
#
# def save_function_relations(function_relations, output_file):
#     with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerow(['ID', 'Script_ID', 'Key', 'Function'])
#         csvwriter.writerows(function_relations)
#
# def main():
#     directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_4.0\Relation'
#     output_directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_4.0\Relation2CSV'
#     function_count, error_count, error_files, function_relations = process_files(directory)
#
#     print("Final results after processing all files:")
#     print(f"Total Function entries: {function_count}")
#     print(f"Total errors: {error_count}")
#
#     os.makedirs(output_directory, exist_ok=True)
#
#     if error_files:
#         error_file_path = os.path.join(output_directory, 'error.txt')
#         with open(error_file_path, 'w', encoding='utf-8') as error_file:
#             for error_path, error_message in error_files:
#                 error_file.write(f"File: {error_path} - Error: {error_message}\n")
#
#     function_file_path = os.path.join(output_directory, 'function_relation.csv')
#     save_function_relations(function_relations, function_file_path)
#
# if __name__ == "__main__":
#     main()
# import os
# import csv
#
#
# def process_files(directory, batch_size=500):
#     relation_count = 0
#     error_count = 0
#     error_files = []
#     file_counter = 0
#     relation_id = 1
#     relation_entries = []
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     data = eval(file.read())
#                     for key in data.keys():
#                         if 'DataSource' in data[key] and 'Function' in data[key]:
#                             data_sources = data[key]['DataSource']
#                             functions = data[key]['Function']
#
#                             if not isinstance(data_sources, list):
#                                 data_sources = [data_sources]
#                             if not isinstance(functions, list):
#                                 functions = [functions]
#
#                             for function in functions:
#                                 for data_source in data_sources:
#                                     relation_entries.append([relation_id, filename, data_source, 'Be_Acted_On', function])
#                                     relation_id += 1
#                             relation_count += len(data_sources) * len(functions)
#                         else:
#                             missing_keys = []
#                             if 'DataSource' not in data[key]:
#                                 missing_keys.append('DataSource')
#                             if 'Function' not in data[key]:
#                                 missing_keys.append('Function')
#                             print(f"File '{filename}' in relation '{key}' is missing keys: {', '.join(missing_keys)}")
#
#             except Exception as e:
#                 error_count += 1
#                 error_files.append((file_path, str(e)))
#
#             file_counter += 1
#             if file_counter % batch_size == 0:
#                 print(f"Processed {file_counter} files so far:")
#                 print(f"Total Relation entries: {relation_count}")
#                 print(f"Total errors: {error_count}")
#                 if error_count > 0:
#                     print("Error details:")
#                     for error_file, error_message in error_files:
#                         print(f"File: {error_file} - Error: {error_message}")
#
#     return relation_count, error_count, error_files, relation_entries
#
#
# def save_relation_entries(relation_entries, output_file):
#     with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerow(['Relation_ID', 'Script_ID', 'Head_Entity', 'Relation_Type', 'Tail_Entity'])
#         csvwriter.writerows(relation_entries)
#
#
# def main():
#     directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_4.0\Relation'
#     output_directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_4.0\Relation2CSV'
#
#     # 确保输出目录存在，如果不存在则创建它
#     os.makedirs(output_directory, exist_ok=True)
#
#     relation_count, error_count, error_files, relation_entries = process_files(directory)
#
#     print("Final results after processing all files:")
#     print(f"Total Relation entries: {relation_count}")
#     print(f"Total errors: {error_count}")
#
#     if error_files:
#         error_file_path = os.path.join(output_directory, 'error.txt')
#         with open(error_file_path, 'w', encoding='utf-8') as error_file:
#             for error_path, error_message in error_files:
#                 error_file.write(f"File: {error_path} - Error: {error_message}\n")
#
#     output_file_path = os.path.join(output_directory, 'relation_with_func.csv')
#     save_relation_entries(relation_entries, output_file_path)
#
#
# if __name__ == "__main__":
#     main()
import os
import csv


def process_files(directory, batch_size=500):
    relation_count = 0
    error_count = 0
    error_files = []
    file_counter = 0
    relation_id = 1
    function_relations = []
    time_relations = []
    geo_relations = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = eval(file.read())
                    for key in data.keys():
                        # 处理 DataSource 和 Function 的关系
                        if 'DataSource' in data[key] and 'Function' in data[key]:
                            data_sources = data[key]['DataSource']
                            functions = data[key]['Function']

                            if not isinstance(data_sources, list):
                                data_sources = [data_sources]
                            if not isinstance(functions, list):
                                functions = [functions]

                            for function in functions:
                                for data_source in data_sources:
                                    function_relations.append([relation_id, filename, data_source, 'ActOn', function])
                                    relation_id += 1
                            relation_count += len(data_sources) * len(functions)

                        # 处理 DataSource 和 TimeScope 的关系
                        if 'DataSource' in data[key] and 'TimeScope' in data[key]:
                            data_sources = data[key]['DataSource']
                            timescopes = data[key]['TimeScope']

                            if not isinstance(data_sources, list):
                                data_sources = [data_sources]
                            if not isinstance(timescopes, list):
                                timescopes = [timescopes]

                            for timescope in timescopes:
                                for data_source in data_sources:
                                    time_relations.append([relation_id, filename, data_source, 'RelatesTo', timescope])
                                    relation_id += 1
                            relation_count += len(data_sources) * len(timescopes)

                        # 处理 DataSource 和 GeoScope 的关系
                        if 'DataSource' in data[key] and 'GeoScope' in data[key]:
                            data_sources = data[key]['DataSource']
                            geoscopes = data[key]['GeoScope']

                            if not isinstance(data_sources, list):
                                data_sources = [data_sources]
                            if not isinstance(geoscopes, list):
                                geoscopes = [geoscopes]

                            for geoscope in geoscopes:
                                for data_source in data_sources:
                                    geo_relations.append([relation_id, filename, data_source, 'Covers', geoscope])
                                    relation_id += 1
                            relation_count += len(data_sources) * len(geoscopes)

            except Exception as e:
                error_count += 1
                error_files.append((file_path, str(e)))

            file_counter += 1
            if file_counter % batch_size == 0:
                print(f"Processed {file_counter} files so far:")
                print(f"Total Relation entries: {relation_count}")
                print(f"Total errors: {error_count}")
                if error_count > 0:
                    print("Error details:")
                    for error_file, error_message in error_files:
                        print(f"File: {error_file} - Error: {error_message}")

    return relation_count, error_count, error_files, function_relations, time_relations, geo_relations


def save_relation_entries(relation_entries, output_file, headers):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(relation_entries)


def main():
    directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Relation'
    output_directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Relation\Relation2CSV'

    # 确保输出目录存在，如果不存在则创建它
    os.makedirs(output_directory, exist_ok=True)

    relation_count, error_count, error_files, function_relations, time_relations, geo_relations = process_files(
        directory)

    print("Final results after processing all files:")
    print(f"Total Relation entries: {relation_count}")
    print(f"Total errors: {error_count}")

    if error_files:
        error_file_path = os.path.join(output_directory, 'error.txt')
        with open(error_file_path, 'w', encoding='utf-8') as error_file:
            for error_path, error_message in error_files:
                error_file.write(f"File: {error_path} - Error: {error_message}\n")

    function_output_file = os.path.join(output_directory, 'relation_with_function.csv')
    save_relation_entries(function_relations, function_output_file,
                          ['Relation_ID', 'Script_ID', 'Head_Entity', 'Relation_Type', 'Tail_Entity'])

    time_output_file = os.path.join(output_directory, 'relation_with_time.csv')
    save_relation_entries(time_relations, time_output_file,
                          ['Relation_ID', 'Script_ID', 'Head_Entity', 'Relation_Type', 'Tail_Entity'])

    geo_output_file = os.path.join(output_directory, 'relation_with_geo.csv')
    save_relation_entries(geo_relations, geo_output_file,
                          ['Relation_ID', 'Script_ID', 'Head_Entity', 'Relation_Type', 'Tail_Entity'])


if __name__ == "__main__":
    main()
