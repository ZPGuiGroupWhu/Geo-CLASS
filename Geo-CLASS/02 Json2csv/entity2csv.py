import os
import csv


def clean_dict_content(content):
    last_bracket_index = content.rfind(']')
    last_brace_index = content.rfind('}')
    
    if last_bracket_index != -1 and last_brace_index != -1 and last_bracket_index < last_brace_index:
        comma_index = content.rfind(',', last_bracket_index, last_brace_index)
        if comma_index != -1:
            content = content[:comma_index] + ' ' + content[comma_index + 1:]
    
    return content


def process_files(directory, batch_size=500):
    theme_count = 0
    function_count = 0
    datasource_count = 0
    geoscope_count = 0
    timescope_count = 0
    error_count = 0
    error_files = []
    file_counter = 0
    theme_entries = []
    function_entries = []
    datasource_entries = []
    geoscope_entries = []
    timescope_entries = []

    theme_id = 1
    function_id = 1
    datasource_id = 1
    geoscope_id = 1
    timescope_id = 1

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    content = clean_dict_content(content)
                    data = eval(content)  # Assuming the content is in Python dictionary format
                    
                    for theme in data.get('Theme', []):
                        theme_entries.append([theme_id, filename, theme])
                        theme_id += 1

                    for function in data.get('Function', []):
                        function_entries.append([function_id, filename, function])
                        function_id += 1

                    for datasource in data.get('DataSource', []):
                        datasource_entries.append([datasource_id, filename, datasource])
                        datasource_id += 1

                    for geoscope in data.get('GeoScope', []):
                        geoscope_entries.append([geoscope_id, filename, geoscope])
                        geoscope_id += 1

                    for timescope in data.get('TimeScope', []):
                        timescope_entries.append([timescope_id, filename, timescope])
                        timescope_id += 1

                    theme_count += len(data.get('Theme', []))
                    function_count += len(data.get('Function', []))
                    datasource_count += len(data.get('Datasource', []))
                    geoscope_count += len(data.get('Geoscope', []))
                    timescope_count += len(data.get('Timescope', []))
            except Exception as e:
                error_count += 1
                error_files.append((file_path, str(e)))

            file_counter += 1
            if file_counter % batch_size == 0:
                print(f"Processed {file_counter} files so far:")
                print(f"Total Theme entries: {theme_count}")
                print(f"Total Function entries: {function_count}")
                print(f"Total Datasource entries: {datasource_count}")
                print(f"Total Geoscope entries: {geoscope_count}")
                print(f"Total Timescope entries: {timescope_count}")
                print(f"Total errors: {error_count}")
                if error_count > 0:
                    print("Error details:")
                    for error_file, error_message in error_files:
                        print(f"File: {error_file} - Error: {error_message}")

    return theme_entries, function_entries, datasource_entries, geoscope_entries, timescope_entries, error_files

def main():
    directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Entity'
    output_directory = r'F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Entity\Entity2CSV'
    theme_entries, function_entries, datasource_entries, geoscope_entries, timescope_entries, error_files = process_files(directory)
    
    print("Final results after processing all files:")
    print(f"Total Theme entries: {len(theme_entries)}")
    print(f"Total Function entries: {len(function_entries)}")
    print(f"Total Datasource entries: {len(datasource_entries)}")
    print(f"Total Geoscope entries: {len(geoscope_entries)}")
    print(f"Total Timescope entries: {len(timescope_entries)}")
    print(f"Total errors: {len(error_files)}")

    os.makedirs(output_directory, exist_ok=True)

    if error_files:
        error_file_path = os.path.join(output_directory, 'error.txt')
        with open(error_file_path, 'w', encoding='utf-8') as error_file:
            for error_path, error_message in error_files:
                error_file.write(f"File: {error_path} - Error: {error_message}\n")

    theme_file_path = os.path.join(output_directory, 'theme_sample.csv')
    with open(theme_file_path, 'w', newline='', encoding='utf-8') as theme_csv:
        writer = csv.writer(theme_csv)
        writer.writerow(['ID', 'Script_ID', 'Entity_Type', 'Value'])
        for entry in theme_entries:
            writer.writerow([entry[0], entry[1], 'Theme', entry[2]])

    function_file_path = os.path.join(output_directory, 'function_sample.csv')
    with open(function_file_path, 'w', newline='', encoding='utf-8') as function_csv:
        writer = csv.writer(function_csv)
        writer.writerow(['ID', 'Script_ID', 'Entity_Type', 'Value'])
        for entry in function_entries:
            writer.writerow([entry[0], entry[1], 'Function', entry[2]])

    datasource_file_path = os.path.join(output_directory, 'datasource_sample.csv')
    with open(datasource_file_path, 'w', newline='', encoding='utf-8') as datasource_csv:
        writer = csv.writer(datasource_csv)
        writer.writerow(['ID', 'Script_ID', 'Entity_Type', 'Value'])
        for entry in datasource_entries:
            writer.writerow([entry[0], entry[1], 'Datasource', entry[2]])

    geoscope_file_path = os.path.join(output_directory, 'geoscope_sample.csv')
    with open(geoscope_file_path, 'w', newline='', encoding='utf-8') as geoscope_csv:
        writer = csv.writer(geoscope_csv)
        writer.writerow(['ID', 'Script_ID', 'Entity_Type', 'Value'])
        for entry in geoscope_entries:
            writer.writerow([entry[0], entry[1], 'Geoscope', entry[2]])

    timescope_file_path = os.path.join(output_directory, 'timescope_sample.csv')
    with open(timescope_file_path, 'w', newline='', encoding='utf-8') as timescope_csv:
        writer = csv.writer(timescope_csv)
        writer.writerow(['ID', 'Script_ID', 'Entity_Type', 'Value'])
        for entry in timescope_entries:
            writer.writerow([entry[0], entry[1], 'Timescope', entry[2]])


if __name__ == "__main__":
    main()
