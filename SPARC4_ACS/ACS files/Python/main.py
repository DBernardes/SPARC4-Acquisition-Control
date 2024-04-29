import os

import astropy.io.fits as fits
import numpy as np
from header import CCD, ICS, S4GUI, TCS, Focuser, General_KWs, Weather_Station
from utils import (fix_image_orientation, format_string, load_json,
                   verify_file_already_exists, write_error_log)


def main(night_dir, file, data, header_json):
    file = format_string(file)
    night_dir = format_string(night_dir)
    file = os.path.join(night_dir, file)

    header_json = load_json(header_json)

    if header_json == None:
        hdr = fits.Header()
        error_str = '[WARNNING] A wrong formatting was found for the header content.'
        write_error_log(error_str, night_dir)
    else:
        for cls in [Focuser, ICS, S4GUI, TCS, Weather_Station, General_KWs, CCD]:
            obj = cls(header_json, night_dir)
            obj.fix_keywords()
            hdr = obj.hdr
        try:
            data = fix_image_orientation(hdr['CHANNEL'], data)
        except:
            error_str = '[WARNNING] The "CHANNEL" keyword was not found.'
            write_error_log(error_str, night_dir)

    file = verify_file_already_exists(file)
    fits.writeto(file, data, hdr, output_verify='ignore')
    return


# data = np.zeros((100, 100))
# main(r'EEE:\images\todayy', '20240213_s4c1_000001_zero.fitss', data, s4gui_json)
