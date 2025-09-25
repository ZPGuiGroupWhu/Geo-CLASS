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
                        # Handling the relation between DataSource and Function
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

                        # Handling the relation between DataSource and TimeScope
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

                        # Handling the relation between DataSource and GeoScope
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
    # Modify the input and output paths according to the result directories of different LLMs
    directory = r'.\LLM_Extraction_Result\GPT3.5\Relation'
    output_directory = r'.\LLM_Extraction_Result\GPT3.5\Relation\Relation2CSV'

    # Make sure the output directory exists, create it if it doesn't exist
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
