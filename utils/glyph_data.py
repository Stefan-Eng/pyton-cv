# -*- coding: utf-8 -*-

import struct
import json

import Tkinter # TODO: Try to do find out screen resolution without library.

def get_table_metadata(filehandler):
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

def get_hmtx_data(filehandler, data_offset, length, number_of_metrics):

    """ The fields that make up a hmtx longHorMetric are:
    H / USHORT / uFWord -- advanceWidth
    h / SHORT  / FWord  -- lsb (left side bearing)
    """

    filehandler.seek(data_offset)

    glyph_metrics = []
    trash_data = filehandler.read(4)
    for num in range(number_of_metrics):
        data = filehandler.read(4)
        tup = struct.unpack('>Hh',data)
        glyph_metrics.append(tup)

    return glyph_metrics

def get_post_name_array(filehandler, metadata):

    data_offset = metadata['data_offset']
    length = metadata['length']

    filehandler.seek(data_offset)
    data = filehandler.read(32)
    version, italicAngle, underlinePosition, underlineThickness, \
    isFixedPitch, minMemType42, maxMemType42, minMemType1, \
    maxMemType1 = struct.unpack('>4slhhLLLLL', data)

    data_dict = {}
    data_dict["version"] = version
    data_dict["italicAngle"] = italicAngle
    data_dict["underlinePosition"] = underlinePosition
    data_dict["underlineThickness"] = underlineThickness
    data_dict["isFixedPitch"] = isFixedPitch
    data_dict["minMemType42"] = minMemType42
    data_dict["maxMemType42"] = maxMemType42
    data_dict["minMemType1"] = minMemType1
    data_dict["maxMemType1"] = maxMemType1

    name_metadata = filehandler.read(2)
    num_glyphs = struct.unpack('>H', name_metadata)[0]

    glyph_positions = []
    for i in range(num_glyphs):
        pos_data = filehandler.read(2)
        pos_offset = struct.unpack('>H', pos_data)[0]
        glyph_positions.append(pos_offset)

    name_array = []
    for x in range(num_glyphs):
        length_data = filehandler.read(1)
        length = struct.unpack('>B', length_data)[0]
        if length == 0:
            filehandler.seek(-1, 1)
            name_array.append('.null')
        string_data = filehandler.read(length)
        name = struct.unpack('>{}s'.format(length), string_data)[0]
        name_array.append(name)

    glyph_to_name_mapping = []
    for pos in glyph_positions:
        if pos < 256:
            glyph_to_name_mapping.append('.null')
        else:
            pos = pos-256
            glyph_to_name_mapping.append(name_array[pos])

    return glyph_to_name_mapping

def get_head_data(filehandler, metadata):

    data_offset = metadata['data_offset']
    length = metadata['length']

    filehandler.seek(data_offset)
    data = filehandler.read(42)

    version,fontRevision,checkSumAdjustment,magicNumber,flags, \
    unitsPerEm,DateTimecreated,DateTimemodified,xMin,yMin,macStyle, \
    lowestRecPPEM,fontDirectionHint,indexToLocFormat,\
    glyphDataFormat = struct.unpack('>4s4sLLHHllhhHHhhh', data)

    data_dict = {}
    data_dict['version'] = version
    data_dict['fontRevision'] = fontRevision
    data_dict['checkSumAdjustment'] = checkSumAdjustment
    data_dict['magicNumber'] = magicNumber
    data_dict['flags'] = flags
    data_dict['unitsPerEm'] = unitsPerEm
    data_dict['DateTimecreated'] = DateTimecreated
    data_dict['DateTimemodified'] = DateTimemodified
    data_dict['xMin'] = xMin
    data_dict['yMin'] = yMin
    data_dict['macStyle'] = macStyle
    data_dict['lowestRecPPEM'] = lowestRecPPEM
    data_dict['fontDirectionHint'] = fontDirectionHint
    data_dict['indexToLocFormat'] = indexToLocFormat
    data_dict['glyphDataFormat'] = glyphDataFormat

    return data_dict

def b(text):
    return text.encode('string-escape')

def get_alphabet(glyph_dict):
    alphabet = {}
    non_chars = [('space',' '),('period','.'),('comma','.'),
                 ('parenleft','('),('parenright',')'), ('question','?'),
                 ('at','@'), ('one','1'), ('two','2'), ('three','3'),
                 ('four','4'),('five','5'),('six','6'),('seven','7'),
                 ('eight','8'),('nine','9'),('zero','0'),('slash','/'),
                 ('quotesingle',"'"),('O','Ö'),('o','ö'),('A','Ä'),
                 ('a','ä'),('A','Å'),('a','å'),('comma',','),
                 ('exclam','!'),('e','é'),('colon',':'),('hyphen','-'),
                 ('plus','+'),('bar','|'),('semicolon',';')]

    for letter in 'abcdefghijklmnopqrstuvwxyz':
        alphabet[letter] = glyph_dict[letter]
        letter = letter.upper()
        alphabet[letter] = glyph_dict[letter]
    for key, store_as in non_chars:
        alphabet[store_as] = glyph_dict[key]
    return alphabet

def get_glyph_data(font_size):

    with open("data/Georgia.ttf", 'r') as filehandler:

        table_metadata = get_table_metadata(filehandler)

        hhea_metadata = table_metadata['hhea']
        hhea_data_offset = hhea_metadata['data_offset']
        hhea_length = hhea_metadata['length']
        hhea_data= get_hhea_data(filehandler, hhea_data_offset, hhea_length)

        number_of_metrics = hhea_data['numberOfHMetrics']

        hmtx_metadata = table_metadata['hmtx']
        hmtx_data_offset = hmtx_metadata['data_offset']
        hmtx_length = hmtx_metadata['length']
        hmtx_data = get_hmtx_data(filehandler, hmtx_data_offset, hmtx_length,
                                  number_of_metrics)

        post_metadata = table_metadata['post']
        glyph_names = get_post_name_array(filehandler, post_metadata)

        glyph_data = {}
        for name, data in zip(glyph_names, hmtx_data):
            advanceWidth, lsb = data
            glyph_data[name] = {'advanceWidth': advanceWidth,
                                'lsb': lsb}

        #TODO: kerning data?

        head_data = get_head_data(filehandler, table_metadata['head'])
        units_per_em = head_data['unitsPerEm']
        raw_alphabet = get_alphabet(glyph_data)

        tk_app = Tkinter.Tk()
        screen_width = tk_app.winfo_screenwidth()
        screen_height = tk_app.winfo_screenheight()
        dpi = tk_app.winfo_pixels('1i')

        inch_on_cm = 0.394
        dpc = dpi * inch_on_cm

        alphabet = {}
        for letter, data in raw_alphabet.iteritems():
            letter_dict = alphabet.get(letter)
            if not letter_dict:
                letter_dict = alphabet[letter] = {}
            for key, value in data.iteritems():
                # Convert font design units to dots.
                dots  = 1.0 * value * font_size / units_per_em
                letter_dict[key] = dots/dpc # convert to centimeters

        return {"alphabet":alphabet,
                "unitsPerEm":units_per_em,
                "dpc":dpc}

def main():

    font_size = 10
    glyph_data = get_glyph_data(font_size)
    print json.dumps(glyph_data, indent=4, separators=(',',':'))

if __name__ == "__main__":
    main()
