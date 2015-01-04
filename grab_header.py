import struct

def tables_metadata(filehandler):
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

def get_hhea_data(filehandler, data_offset, length):

    filehandler.seek(data_offset)

    """ The hhea table consists of the following fields:
    4s - table version number
    h - ascender
    h - decender
    h - lineGap
    H - advaceWidthMax
    h - minLeftSideBearing
    h - minRightSideBearin
    h - xMaxExtend
    h - caretSlopRise
    h - caretSlopeRun
    h - reserved
    h - reserved
    h - reserved
    h - reserved
    h - reserved
    h - metricDataFormat
    H - numberOfHMetrics
    """

    hhea_data = filehandler.read(length)
    version, ascender, decender, lineGap, \
    advanceWidthMax, minLeftSideBearing, minRightSideBearing, \
    xMaxExtend, caretSlopeRise, caretSlopeRun, reserved0, reserved1, \
    reserved2, reserved3, reserved4, metricDataFormat, \
    numberOfHMetrics = struct.unpack('>4shhhHhhhhhhhhhhhH', hhea_data)

    hhea_dict = {}
    hhea_dict["version"] = version
    hhea_dict["ascender"] = ascender
    hhea_dict["decender"] = decender
    hhea_dict["lineGap"] = lineGap
    hhea_dict["advanceWidthMax"] = advanceWidthMax
    hhea_dict["minLeftSideBearing"] = minLeftSideBearing
    hhea_dict["minRightSideBearing"] = minRightSideBearing
    hhea_dict["xMaxExtend"] = xMaxExtend
    hhea_dict["caretSlopeRise"] = caretSlopeRise
    hhea_dict["caretSlopeRun"] = caretSlopeRun
    hhea_dict["reserved0"] = reserved0
    hhea_dict["reserved1"] = reserved1
    hhea_dict["reserved2"] = reserved2
    hhea_dict["reserved3"] = reserved3
    hhea_dict["reserved4"] = reserved4
    hhea_dict["metricDataFormat"] = metricDataFormat
    hhea_dict["numberOfHMetrics"] = numberOfHMetrics

    return hhea_dict

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
