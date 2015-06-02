# -*- coding: utf-8 -*-
#This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2013 Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

from PIL import Image

class ayabImage(object):
  def __init__(self, pil_image, pNumColors = 2):
    self.__numColors      = pNumColors

    self.__imgPosition    = 'center'
    self.__imgStartNeedle = '0'
    self.__imgStopNeedle  = '0'

    self.__knitStartNeedle = 0
    self.__knitStopNeedle  = 199

    self.__startLine  = 0

    self.__image = pil_image

    self.__image = self.__image.convert('L') # convert to 1 byte depth
    self.__updateImageData()

  def imageIntern(self):
    return self.__imageIntern

  def imageExpanded(self):
    return self.__imageExpanded

  def imgWidth(self):
    return self.__imgWidth

  def imgHeight(self):
    return self.__imgHeight

  def knitStartNeedle(self):
    return self.__knitStartNeedle

  def knitStopNeedle(self):
    return self.__knitStopNeedle

  def imgStartNeedle(self):
    return self.__imgStartNeedle

  def imgStopNeedle(self):
    return self.__imgStopNeedle

  def imgPosition(self):
    return self.__imgPosition

  def startLine(self):
    return self.__startLine

  def numColors(self):
    return self.__numColors


  def __updateImageData(self):
    self.__imgWidth   = self.__image.size[0]
    self.__imgHeight  = self.__image.size[1]

    self.__convertImgToIntern()
    self.__calcImgStartStopNeedles()


  def __convertImgToIntern(self):
    num_colors = self.__numColors
    clr_range  = float(256)/num_colors

    imgWidth   = self.__imgWidth
    imgHeight  = self.__imgHeight

    self.__imageIntern = \
      [[0 for i in range(imgWidth)] \
      for j in range(imgHeight)]
    self.__imageColors = \
      [[0 for i in range(num_colors)] \
      for j in range(imgHeight)]
    self.__imageExpanded = \
      [[0 for i in range(imgWidth)] \
      for j in range(num_colors*imgHeight)]

    # Distill image to x colors
    for row in range(0, imgHeight):
      for col in range(0, imgWidth):
        pxl = self.__image.getpixel((col, row))

        for color in range(0, num_colors):
          lowerBound = int(color*clr_range)
          upperBound = int((color+1)*clr_range)
          if pxl>=lowerBound and pxl<upperBound:
            # color map
            self.__imageIntern[row][col]    = color
            # amount of bits per color per line
            self.__imageColors[row][color]  += 1
            # colors separated per line
            self.__imageExpanded[(num_colors*row)+color][col] = 1

    #print(self.__imageIntern)
    #print(self.__imageColors)
    #print(self.__imageExpanded)


  def __calcImgStartStopNeedles(self):
    if self.__imgPosition == 'center':
        needleWidth = (self.__knitStopNeedle - self.__knitStartNeedle) +1
        self.__imgStartNeedle = (self.__knitStartNeedle + needleWidth/2) - self.__imgWidth/2
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__imgWidth -1

    elif self.__imgPosition == 'left':
        self.__imgStartNeedle = self.__knitStartNeedle
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__imgWidth

    elif self.__imgPosition == 'right':
        self.__imgStopNeedle  = self.__knitStopNeedle
        self.__imgStartNeedle = self.__imgStopNeedle - self.__imgWidth

    elif int(self.__imgPosition) > 0 and int(self.__imgPosition) < 200:
        self.__imgStartNeedle = int(self.__imgPosition)
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__imgWidth

    else:
        return False
    return True

  def setNumColors(self, pNumColors):
      """
      sets the number of colors the be used for knitting
      """
      if pNumColors > 1 and pNumColors < 7:
        self.__numColors      = pNumColors
        self.__updateImageData()
      return

  def invertImage(self):
      """
      invert the pixels of the image
      """
      for y in range(0, self.__image.size[1]):
        for x in range(0, self.__image.size[0]):
          pxl = self.__image.getpixel((x, y))
          self.__image.putpixel((x,y),255-pxl)
      self.__updateImageData()
      return


  def rotateImage(self):
      """
      rotate the image 90 degrees clockwise
      """
      self.__image = self.__image.rotate(-90)

      self.__updateImageData()
      return


  def resizeImage(self, pNewWidth):
      """
      resize the image to a given width, keeping the aspect ratio
      """
      wpercent = (pNewWidth/float(self.__image.size[0]))
      hsize = int((float(self.__image.size[1])*float(wpercent)))
      self.__image = self.__image.resize((pNewWidth,hsize), Image.ANTIALIAS)

      self.__updateImageData()
      return


  def setKnitNeedles(self, pKnitStart, pKnitStop):
      """
      set the start and stop needle
      """
      if (pKnitStart < pKnitStop) \
          and pKnitStart >= 0 \
          and pKnitStop < 200:
        self.__knitStartNeedle = pKnitStart
        self.__knitStopNeedle  = pKnitStop

      self.__updateImageData()
      return


  def setImagePosition(self, pImgPosition):
      """
      set the position of the pattern
      """
      ok = False
      if pImgPosition == 'left' \
            or pImgPosition == 'center' \
            or pImgPosition == 'right':
        ok = True
      elif (int(pImgPosition) >= 0 and int(pImgPosition) < 200):
        ok = True

      if ok:
        self.__imgPosition = pImgPosition
        self.__updateImageData()
      return

  def setStartLine(self, pStartLine):
      """
      set the line where to start knitting
      """
      #Check if StartLine is in valid range (picture height)
      if pStartLine >= 0 \
            and pStartLine < self.__image.size[1]:
        self.__startLine = pStartLine
      return
