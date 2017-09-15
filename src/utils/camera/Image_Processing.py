import os
import sys
from datetime import datetime

import numpy
import pyfits as fits
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from numpngw import write_png, _write_text

from src.utils.camera.Image_Headers import set_headers_png


def save_fit(img_to_fit, newname):
    img_fit = img_to_fit
    newname_fit = newname
    newname_fit += ".fit"
    # Criando o arquivo final
    try:
        # Abrindo o arquivo
        fits.writeto(newname_fit, img_fit)
        fits_file = fits.open(newname_fit)
        # Escrevendo o Header
        # Can't get the temperature because have a locker locking shooter process
        # fits_file[0].header["TEMP"] = tuple(get_temperature())[3]
        fits_file[0].header["DATE"] = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
        print("Tricat of save_fit")
        # Fechando e removendo o arquivo temporario
        # fits_file.flush()
        fits_file.close()
    except OSError as e:
        print(newname_fit)
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
    headers[0] = list of get_filter_settings()
    headers[0][0] = Filter Label (prefix)
    headers[0][1] = Wavelength (nm)
    headers[0][2] = Exposure (s)
    headers[0][3] = Binning
    headers[0][4] = Filter Position
    headers[1] = dark_photo
    headers[2] = get_level1
    headers[3] = get_level2
    headers[4] = get_axis_xi
    headers[5] = get_axis_xf
    headers[6] = get_axis_yi
    headers[7] = get_axis_yf
    headers[8] = get_ignore_crop
    headers[9] = get_image_tif
    headers[10] = get_image_fit
    headers[11] = data_hora
    headers[12][0][0] = Latitude
    headers[12][0][1] = Longitude
    headers[12][0][2] = Elevation(m)
    headers[12][0][3] = Pressure(mb)
    headers[12][0][4] = Temperature(?)
    headers[12][1][0] = Solar Elevation
    headers[12][1][1] = Ignore Lunar Position
    headers[12][1][2] = Lunar Elevation
    headers[12][1][3] = Lunar Phase
    headers[12][2][0] = Name
    headers[12][2][1] = Observatory
    headers[12][2][2] = Imager ID
    """
    newname_png = newname + ".png"
    img_png = img
    print("Opening filename")
    try:
        print("Tricat of save_png")
        imgarray = numpy.asarray(img_png, dtype=numpy.int32)

        info = PngImagePlugin.PngInfo()
        day, hour = get_date_hour_image_for_headers(str(headers[11]))

        try:
            info.add_text('dpi', '001')
            info.add_text('Day: ', str(day))
            info.add_text('Hour', str(hour))
            info.add_text('Binning: ', str(headers[0][3]))
            info.add_text('Bit Depth: ', '003')
            info.add_text('CCD Gain: ', '004')
            info.add_text('CCD Temperature: ', '005')
            info.add_text('CCD SET TEMP: ', '??')
            info.add_text('CCD Type: ', str(headers[12][2][2]))
            info.add_text('Exposure: ', str(headers[0][2]) + " seconds")
            info.add_text('Filter Label: ', str(headers[0][0]))
            info.add_text('Filter Position: ', str(headers[0][4]))
            info.add_text('Filter Wavelength: ', str(headers[0][1]))
            info.add_text('Filter Wheel Temperature: ', '013')
            info.add_text('Image Type: ', 'PNG')
            info.add_text('Latitude: ',  str(headers[12][0][0]))
            info.add_text('Longitude: ',  str(headers[12][0][1]))
            info.add_text('Elevation(m): ',  str(headers[12][0][2]))
            info.add_text('Pressure(mb): ',  str(headers[12][0][3]))
            info.add_text('Moon Elevation: ', str(headers[12][1][2]))
            info.add_text('Moon Phase: ', str(headers[12][1][3]))
            info.add_text('Readout Speed: ', '023')
            info.add_text('Shutter CCD: ', '024')
            info.add_text('Shutter Lenz: ', '025')
            info.add_text('Site ID: ', str(headers[12][2][1]))
            info.add_text('Start Time: ', '027')
            info.add_text('Sun Elevation:', str(headers[12][1][0]))
            info.add_text('Version: ', str(headers[12][2][0]))
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
    hora_img = tempo[-6:-4] + ":" + tempo[-4:-2] + ":" + tempo[-2:] + " UT"
    data_img = tempo[:4] + "/" + tempo[4:6] + "/" + tempo[6:8]

    return hora_img, data_img


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
