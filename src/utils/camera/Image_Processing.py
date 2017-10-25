import os
import sys

import numpy
import pyfits as fits
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


def save_fit(img_to_fit, newname, headers):

    newname_fit = newname
    newname_fit += ".fit"

    try:
        binning_fit = int(headers[1][3])
        binning_fit += 1
    except Exception as e:
        print("Binning Type Error ->" + str(e))
        binning_fit = "???"

    if str(headers[12]) == 1:
        shutter_fit = "CLOSED"
    else:
        shutter_fit = "OPEN"

    # Criando o arquivo final
    try:
        day_hour = get_date_hour_image_for_headers(str(headers[9]))
        # Abrindo o arquivo
        fits.writeto(newname_fit, img_to_fit)
        with fits.open(newname_fit, mode='update') as fits_file:
            fits_file[0].header["BINNING"] = str(binning_fit) + "x" + str(binning_fit)
            fits_file[0].header["CCD-TEMP"] = str(headers[11]) + " Celsius degrees"
            fits_file[0].header["CCDSTEMP"] = str(headers[0][0]) + " Celsius degrees"
            fits_file[0].header["CCDTYPE"] = str(headers[10][2][2])
            fits_file[0].header["EXPOSURE"] = str(headers[1][2]) + "000 ms"
            fits_file[0].header["FLT-LBL"] = str(headers[1][0])
            fits_file[0].header["FLT-POS"] = str(headers[1][4])
            fits_file[0].header["FLT-WAVE"] = str(headers[1][1])
            fits_file[0].header["IMG-TYPE"] = "FIT"
            fits_file[0].header["LATITUDE"] = str(headers[10][0][0]) + " degrees"
            fits_file[0].header["LONGITUD"] = str(headers[10][0][1]) + " degrees"
            fits_file[0].header["MO-ELE"] = str(headers[10][1][2]) + " degrees"
            fits_file[0].header["MO-PHASE"] = str(headers[10][1][3]) + " %"
            fits_file[0].header["SHTRCCD"] = str(shutter_fit)
            fits_file[0].header["SHTRLENZ"] = str(shutter_fit)
            fits_file[0].header["SITE-ID"] = str(headers[10][2][1])
            fits_file[0].header["START-T"] = str(day_hour) + " UTC"
            fits_file[0].header["SUN-ELEV"] = str(headers[10][1][0]) + " degrees"
            fits_file[0].header["VERS"] = str(headers[10][2][0])

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
    """
    headers[0][0] = Set Temperature
    headers[1] = list of get_filter_settings()
    headers[1][0] = Filter Label (prefix)
    headers[1][1] = Wavelength (nm)
    headers[1][2] = Exposure (s)
    headers[1][3] = Binning
    headers[1][4] = Filter Position
    headers[2] = get_level1
    headers[3] = get_level2
    headers[4] = get_axis_xi
    headers[5] = get_axis_xf
    headers[6] = get_axis_yi
    headers[7] = get_axis_yf
    headers[8] = get_ignore_crop
    headers[9] = data_hora
    headers[10][0][0] = Latitude
    headers[10][0][1] = Longitude
    headers[10][0][2] = Elevation(m)
    headers[10][0][3] = Pressure(mb)
    headers[10][0][4] = Temperature(?)
    headers[10][1][0] = Solar Elevation
    headers[10][1][1] = Ignore Lunar Position
    headers[10][1][2] = Lunar Elevation
    headers[10][1][3] = Lunar Phase
    headers[10][2][0] = Name
    headers[10][2][1] = Observatory
    headers[10][2][2] = Imager ID
    headers[11] = CCD Temperature
    """

    try:
        binning = int(headers[1][3])
        binning += 1
    except Exception as e:
        print("Binning Type Error ->" + str(e))
        binning = " ??? "

    print("\n\n- HEADERS -")
    for x in enumerate(headers):
        print(str(x))

    newname_png = newname + ".png"
    img_png = img
    print("Opening filename")
    try:
        print("Tricat of save_png")
        imgarray = numpy.asarray(img_png, dtype=numpy.int32)

        info = PngImagePlugin.PngInfo()
        day_hour = get_date_hour_image_for_headers(str(headers[9]))

        if str(headers[12]) == 1:
            shutter_png = "CLOSED"
        else:
            shutter_png = "OPEN"

        try:
            info.add_text('Binning: ', str(binning) + "x" + str(binning))
            info.add_text('CCD SET TEMP: ', str(headers[0][0]) + u"\u00b0C")
            info.add_text('CCD Temperature: ', str(headers[11]) + u"\u00b0C")
            info.add_text('CCD Type: ', str(headers[10][2][2]))
            info.add_text('Exposure: ', str(headers[1][2]) + "000 ms")
            info.add_text('Filter Label: ', str(headers[1][0]))
            info.add_text('Filter Position: ', str(headers[1][4]))
            info.add_text('Filter Wavelength: ', str(headers[1][1]))
            info.add_text('Filter Wheel Temperature: ', "25" + u"\u00b0C")
            info.add_text('Image Type: ', 'PNG')
            info.add_text('Latitude: ', str(headers[10][0][0]) + u"\u00b0")
            info.add_text('Longitude: ', str(headers[10][0][1]) + u"\u00b0")
            info.add_text('Moon Elevation: ', str(headers[10][1][2]) + u"\u00b0")
            info.add_text('Moon Phase: ', str(headers[10][1][3]) + " %")
            info.add_text('Shutter CCD: ', str(shutter_png))
            info.add_text('Shutter Lenz: ', str(shutter_png))
            info.add_text('Site ID: ', str(headers[10][2][1]))
            info.add_text('Start Time: ', str(day_hour) + " UTC")
            info.add_text('Sun Elevation:', str(headers[10][1][0]) + u"\u00b0")
            info.add_text('Version: ', str(headers[10][2][0]))
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
