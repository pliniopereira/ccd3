import os

from PIL import Image


def str_to_raw(s):
    raw_map = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}
    return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)


def set_headers_png(image_path):
    print("\n\n")
    print("OKOKOKOK")
    image_path = r'image_path'
    print(image_path)
    print(type(image_path))
    print("\n\n")
    # png_name = str(image_path).split('/')[-1]
    # str_image = str(image_path)
    # str_png_name = str(png_name)
    # x = len(png_name)
    # path = str_image[:-x]
    # print(str(png_name))
    # print(str(path))
    #
    # print("\n\n")
    #
    # image = Image.open(png_name)
    #
    # print("\n\n")
    # print(image)
    # print(type(image))
    # print(png_name)
    # print(path)
    # print("\n\n")


    scriptDir = os.path.dirname(image_path)
    # impath = os.path.join(scriptDir, png_name)

    # f = io.StringIO(image_path)
    # print(sys.argv[1:])
    # for image_path in sys.argv[1:]:
    #     try:
    #         with Image.open(image_path) as image:
    #             print(image_path, image.format, "%dx%d" % image.size, image.mode)
    #     except Exception as e:
    #         print("Exception for image_path in sys.argv[1:]: -> {}".format(e))

    try:
        # teste = open(image_path, 'r+')
        image = Image.open(image_path)
        image.info['dpi'] = '001'
        image.info['Binning'] = '002'
        image.info['Bit Depth'] = '003'
        image.info['CCD Gain'] = '004'
        image.info['CCD Temperature'] = '005'
        image.info['CCD SET TEMP'] = '006'
        image.info['CCD Type'] = '007'
        image.info['Exposure'] = '008'
        image.info['Filter Description'] = '009'
        image.info['Filter Label'] = '010'
        image.info['Filter Position'] = '011'
        image.info['Filter Wavelength'] = '012'
        image.info['Filter Wheel Temperature'] = '013'
        image.info['Image Type'] = '014'
        image.info['Latitude'] = '015'
        image.info['Latitude'] = '016'
        image.info['Longitude'] = '017'
        image.info['Moon Elevation'] = '021'
        image.info['Moon Phase'] = '022'
        image.info['Readout Speed'] = '023'
        image.info['Shutter CCD'] = '024'
        image.info['Shutter Lenz'] = '025'
        image.info['Site ID'] = '026'
        image.info['Start Time'] = '027'
        image.info['Sun Elevation'] = '028'
        image.info['Version'] = '028'
        image.save(image_path)
    except Exception as e:
        print("Exception Image.open(image_path) -> {}".format(e))

    print("\n\n")
    print("22222222222")
    print(image_path)
    print(type(image_path))
    print("\n\n")


def return_info_png(file_name):
    file_name = str(file_name)
    try:
        image = Image.open(file_name)
        dictionary = image.info
        for keys, values in dictionary.items():
            print(str(keys) + ": " + str(values))
        image.show
        print("\n\n")
    except Exception as e:
        print("Exception return_info_png -> {}".format(e))
