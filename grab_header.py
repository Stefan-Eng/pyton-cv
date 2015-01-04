import struct

def main():

    with open("Georgia.ttf", 'r') as filehandler:

        tables_info = get_tables_dictionary(filehandler)
        for table in tables_info:
            print table

def get_tables_dictionary(filehandler):
    filehandler.seek(0)
    header_data = filehandler.read(12)
    version, num_tables, search_range, \
    range_shift, padding = struct.unpack(">4sHHHH",header_data)

    ttf_header_data = {}
    ttf_header_data["version"] = version
    ttf_header_data["number_of_tables"] = num_tables
    ttf_header_data["search_range"] = search_range
    ttf_header_data["range_shift"] = range_shift

    table_headers = {}
    table_headers["ttf_header"] = ttf_header_data

    for i in range(num_tables):
        table_data = filehandler.read(16)
        tag, check_sum, data_offset, length = struct.unpack(">4sLLL", table_data)
        table_data_dictionary = {}
        table_data_dictionary["check_sum"] = check_sum
        table_data_dictionary["data_offset"] = data_offset
        table_data_dictionary["length"] = length
        table_headers[tag] = table_data_dictionary

    return table_headers

def b(text):
    return text.encode('string-escape')

def main():

    with open("Georgia.ttf", 'r') as filehandler:

        table_metadata = tables_metadata(filehandler)
        hhea_metadata = table_metadata['hhea']
        data_offset = hhea_metadata['data_offset']
        length = hhea_metadata['length']

        hhea_data= get_hhea_data(filehandler, data_offset, length)
        print hhea_data


if __name__ == "__main__":
    main()
