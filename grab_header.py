import struct

def main():

    with open("Georgia.ttf", 'r') as file_handle:

        version_data = file_handle.read(4)
        version = exunpack(">4s",version_data)

        num_tables_data = file_handle.read(2)
        num_tables = exunpack(">H", num_tables_data)

        search_range_data = file_handle.read(2)
        search_range = exunpack(">H", search_range_data)

        range_shift_data = file_handle.read(2)
        range_shift = exunpack(">H", range_shift_data)

        print "version: {}".format(b(version))
        print "number_of_tables: {}".format(num_tables)
        print "search_range: {}".format(search_range)
        print "range_shift: {}".format(range_shift)

        # Read last 2 buffer bytes.
        last_to_bytes = file_handle.read(2)
        print b(last_to_bytes)

        # Beginning of tables table.

        first_table_tag_data = file_handle.read(4)
        first_table_tag = exunpack(">4s", first_table_tag_data)

        first_table_check_sum_data = file_handle.read(4)
        first_table_check_sum = exunpack(">L", first_table_check_sum_data)

        first_table_offset_data = file_handle.read(4)
        first_table_offset = exunpack(">L", first_table_offset_data)

        first_table_length_data = file_handle.read(4)
        first_table_length = exunpack(">L", first_table_length_data)

        print "first tag: {}".format(first_table_tag)
        print "first checksum: {}".format(first_table_check_sum)
        print "first offset: {}".format(first_table_offset)
        print "first length: {}".format(first_table_length)

        second_table_tag_data = file_handle.read(4)
        second_table_tag = exunpack(">4s", second_table_tag_data)

        second_table_check_sum_data = file_handle.read(4)
        second_table_check_sum = exunpack(">L", second_table_check_sum_data)

        second_table_offset_data = file_handle.read(4)
        second_table_offset = exunpack(">L", second_table_offset_data)

        second_table_length_data = file_handle.read(4)
        second_table_length = exunpack(">L", second_table_length_data)

        print "second tag: {}".format(second_table_tag)
        print "second checksum: {}".format(second_table_check_sum)
        print "second offset: {}".format(second_table_offset)
        print "second length: {}".format(second_table_length)

        third_table_tag_data = file_handle.read(4)
        third_table_tag = exunpack(">4s", third_table_tag_data)

        third_table_check_sum_data = file_handle.read(4)
        third_table_check_sum = exunpack(">L", third_table_check_sum_data)

        third_table_offset_data = file_handle.read(4)
        third_table_offset = exunpack(">L", third_table_offset_data)

        third_table_length_data = file_handle.read(4)
        third_table_length = exunpack(">L", third_table_length_data)

        print "third tag: {}".format(third_table_tag)
        print "third checksum: {}".format(third_table_check_sum)
        print "third offset: {}".format(third_table_offset)
        print "third length: {}".format(third_table_length)

def exunpack(format, string):
    return struct.unpack(format, string)[0]

def b(text):
    return text.encode('string-escape')

if __name__ == "__main__":
    main()
