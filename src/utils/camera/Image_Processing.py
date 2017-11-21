import os
import sys

import numpy
import pyfits as fits
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

software_version = "CCD Controller 3 - V 0.9"


def save_fit(img_to_fit, newname, headers):

    newname_fit = newname
    newname_fit += ".fit"

    try:
        binning_fit = int(headers['Binning'])
        binning_fit += 1
    except Exception as e:
        print("Binning Type Error ->" + str(e))
        binning_fit = "???"

    # Criando o arquivo final
    try:
        day_hour = get_date_hour_image_for_headers(str(headers['Start Time']))
        # Abrindo o arquivo
        fits.writeto(newname_fit, img_to_fit)
        with fits.open(newname_fit, mode='update') as fits_file:
            fits_file[0].header["BINNING"] = str(binning_fit) + "x" + str(binning_fit)
            fits_file[0].header["CCD-TEMP"] = str(headers['Set Temperature']) + " Celsius degrees"
            fits_file[0].header["CCDSTEMP"] = str(headers['Temperature']) + " Celsius degrees"
            fits_file[0].header["CCDTYPE"] = str(headers['Name'])
            fits_file[0].header["EXPOSURE"] = str(headers['Exposure'] + "0 ms")
            fits_file[0].header["FLT-LBL"] = str(headers['Filter Label'])
            fits_file[0].header["FLT-POS"] = str(headers['Filter Position'])
            fits_file[0].header["FLT-WAVE"] = str(headers['Filter Wavelength'])
            fits_file[0].header["IMG-TYPE"] = "FIT"
            fits_file[0].header["LATITUDE"] = str(headers['Latitude']) + " degrees"
            fits_file[0].header["LONGITUD"] = str(headers['Longitude']) + " degrees"
            fits_file[0].header["MO-ELE"] = str(headers['Moon Elevation']) + " degrees"
            fits_file[0].header["MO-PHASE"] = str(headers['Moon Phase']) + " %"
            fits_file[0].header["SHTRCCD"] = str(headers['Open or close shutter'])
            fits_file[0].header["SHTRLENZ"] = str(headers['Open or close shutter'])
            fits_file[0].header["SITE-ID"] = str(headers['Observatory'])
            fits_file[0].header["START-T"] = str(day_hour) + " UTC"
            fits_file[0].header["SUN-ELEV"] = str(headers['Sun Elevation']) + " degrees"
            fits_file[0].header["VERS"] = str(software_version)

    except Exception as e:
        # print(newname_fit)
        print("Exception save_fit ->" + str(e))


def save_tif(img, newname):
    print("Opening filename")
    img_tif = img
    newname_tif = newname
    newname_tif += ".tif"
    try:
        print("Tricat of save_tif")
        try:
            if sys.platform.startswith("linux"):
                imgarray = numpy.array(img_tif, dtype='uint16')
            elif sys.platform.startswith("win"):
                imgarray = numpy.array(img_tif, dtype=numpy.uint16)
        except Exception as e:
            print(e)

        im3 = Image.fromarray(imgarray)
        im3.save(newname_tif)

    except Exception as e:
        print("Exception -> {}".format(e))


def save_png(img, newname, headers):
    mantenha_variavel_name(newname)
    # print(type(headers))
    # print("\n\n- HEADERS -")
    # print(type(headers))
    # for keys, values in headers.items():
    #     print(str(keys))
    #     print(str(values) + "\n")
    # print("- END HEADERS -\n\n")

    try:
        binning = int(headers['Binning'])
        binning += 1
    except Exception as e:
        print("Binning Type Error ->" + str(e))
        binning = " ??? "

    newname_png = newname + ".png"
    img_png = img

    print("Opening filename")
    try:
        print("Tricat of save_png")
        imgarray = numpy.asarray(img_png, dtype=numpy.int32)

        info = PngImagePlugin.PngInfo()
        day_hour = get_date_hour_image_for_headers(str(headers['Start Time']))

        try:
            info.add_text('Binning: ', str(binning) + "x" + str(binning))
            info.add_text('CCD SET TEMP: ', str(headers['Set Temperature']) + u"\u00b0C")
            info.add_text('CCD Temperature: ', str(headers['Temperature']) + u"\u00b0C")
            info.add_text('CCD Type: ', str(headers['Imager ID']))
            info.add_text('Exposure: ', str(headers['Exposure']) + "0 ms")
            info.add_text('Filter Label: ', str(headers['Filter Label']))
            info.add_text('Filter Position: ', str(headers['Filter Position']))
            info.add_text('Filter Wavelength: ', str(headers['Filter Wavelength']))
            info.add_text('Filter Wheel Temperature: ', "25" + u"\u00b0C")
            info.add_text('Image Type: ', 'PNG')
            info.add_text('Latitude: ', str(headers['Latitude']) + u"\u00b0")
            info.add_text('Longitude: ', str(headers['Longitude']) + u"\u00b0")
            info.add_text('Moon Elevation: ', str(headers['Moon Elevation']) + u"\u00b0")
            info.add_text('Moon Phase: ', str(headers['Moon Phase']) + " %")
            info.add_text('Shutter CCD: ', str(headers['Open or close shutter']))
            info.add_text('Shutter Lenz: ', str(headers['Open or close shutter']))
            info.add_text('Site ID: ', str(headers['Observatory']))
            info.add_text('Start Time: ', str(day_hour) + " UTC")
            info.add_text('Sun Elevation:', str(headers['Sun Elevation']) + u"\u00b0")
            info.add_text('Version: ', str(software_version))
        except Exception as e:
            print("info.add_text: " + e)

        image = Image.fromarray(imgarray)
        image.save(newname_png, "PNG", pnginfo=info)
        # set_headers_png(newname_png)

    except Exception as e:
        print("Exception save_png -> {}".format(e))
        # finally:
        #     try:
        #         set_headers_png(newname_png)
        #     except Exception as e:
        #         print("Exception set_headers_png -> {}".format(e))


def retorna_imagem(name_png):
    img2 = Image.open(name_png)
    img2.show()


def resize_image_512x512(name_png):
    img = Image.open(name_png)
    resized_img = img.resize((int(512), int(512)))
    # resized_img = ImageOps.autocontrast(resized_img, 2)
    resized_img.save(name_png)


def draw_image(name_png):
    hora_img, data_img = get_date_hour_image(name_png)
    filter_img, observatory_img = get_filter_observatory(name_png)

    img = Image.open(name_png)

    fontsFolder = '/usr/share/fonts/truetype'
    times_nr_Font = ImageFont.truetype(os.path.join(fontsFolder, 'Times_New_Roman_Bold.ttf'), 16)

    draw = ImageDraw.Draw(img)
    draw.text((10, 10), observatory_img, fill='white', font=times_nr_Font)
    draw.text((470, 10), filter_img, fill='white', font=times_nr_Font)
    draw.text((420, 490), hora_img, fill='white', font=times_nr_Font)
    draw.text((10, 490), data_img, fill='white', font=times_nr_Font)
    del draw

    img.save(name_png)
    # mostra imagem
    # img.show()


def bytscl(array, max=None, min=None, nan=0, top=255):
    # see http://star.pst.qub.ac.uk/idl/BYTSCL.html
    # note that IDL uses slightly different formulae for bytscaling floats and ints.
    # here we apply only the FLOAT formula...

    if max is None: max = numpy.nanmax(array)
    if min is None: min = numpy.nanmin(array)

    # return (top+0.9999)*(array-min)/(max-min)
    return numpy.maximum(numpy.minimum(
        ((top + 0.9999) * (array - min) / (max - min)).astype(numpy.int16)
        , top), 0)


def get_level(im2, sref_min, sref_max):
    '''
    :param im2: imagem tipo float
    :param sref_min: nivel de referencia normalizado
    :param sref_max: nivel de referencia normalizado
    :return: limites inferior e superior da imagem para exibição na tela, baseado nos niveis de referencia.
    '''
    #
    x_min, x_max = numpy.min(im2), numpy.max(im2)

    # bin_size precisa ser 1 para analisar ponto à ponto
    bin_size = 1
    x_min = 0.0

    nbins = numpy.floor(((x_max - x_min) / bin_size))

    try:
        hist, bins = numpy.histogram(im2, int(nbins), range=[x_min, x_max])

        sum_histogram = numpy.sum(hist)

        sref = numpy.zeros(2)
        sref[0] = sref_min
        sref[1] = sref_max

        res_sa = numpy.zeros(len(hist))

        sa = 0.
        for i in range(len(hist)):
            sa += hist[i]
            res_sa[i] = sa

        res_sa2 = res_sa.tolist()
        res = res_sa[numpy.where((res_sa > sum_histogram * sref[0]) & (res_sa < sum_histogram * sref[1]))]
        nr = len(res)

        sl0 = res_sa2.index(res[0])
        sl1 = res_sa2.index(res[nr - 1])
        slevel = [sl0, sl1]

    except Exception as e:
        print("Exception get_level ->" + str(e))
        print("slevel = [10, 20]")
        slevel = [10, 20]

    return slevel


def get_date_hour(tempo):
    data = tempo[0:4] + "_" + tempo[4:6] + tempo[6:8]
    hora = tempo[9:11] + ":" + tempo[11:13] + ":" + tempo[13:15]

    return data, hora


def get_date_hour_image(tempo):
    hora_img = tempo[-10:-8] + ":" + tempo[-8:-6] + ":" + tempo[-6:-4] + " UT"
    data_img = tempo[-13:-11] + "/" + tempo[-15:-13] + "/" + tempo[-19:-15]

    return hora_img, data_img


def get_date_hour_image_for_headers(tempo):
    date_hour_header = tempo[:4] + "-" + tempo[4:6] + "-" + tempo[6:8] + " " + tempo[-6:-4] + ":" + tempo[-4:-2] + ":" \
                       + tempo[-2:]

    return date_hour_header


def get_filter_observatory(name):
    name_aux = name.split('/')[-1]
    name_filter = name_aux.split('_')[0]
    name_observatory = name_aux.split('_')[1]

    return name_filter, name_observatory


def get_observatory(name):
    name_aux = str(name).split(',')[1]
    name_aux = name_aux.replace("\'", "")
    name_aux = name_aux.replace(" ", "")

    return name_aux


def mantenha_variavel_name(newname):
    variavel = newname
    return 0

