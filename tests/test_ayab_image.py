# -*- coding: utf-8 -*-
# This file is part of Knitlib. It is based on AYAB.
#
#    Knitlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Knitlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Knitlib.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2015 Shiluka Dharmasena, Sebastian Oliva

import pytest
import unittest
import os
from knitlib.plugins.ayab_plugin.ayab_image import ayabImage
from PIL import Image

class TestImage(unittest.TestCase):
    
    def setUp(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename_text = u"mushroom.png"
        self.conf = {}
        self.conf["filename"] = self.filename_text
        self.pil_image = Image.open(os.path.join(self.script_dir, self.conf["filename"]))
        self.ayab_image = ayabImage(self.pil_image, 2)
    
    def test_knitStartNeedle(self):
        assert self.ayab_image.knitStartNeedle() == 0

    def test_knitStopNeedle(self):
        assert self.ayab_image.knitStopNeedle() == 199

    def test_imgPosition(self):
        assert self.ayab_image.imgPosition() == 'center'

    def test_startLine(self):
        assert self.ayab_image.startLine() == 0
    
    def test_numColors(self):
        assert self.ayab_image.numColors() == 2
        
    def test_setStartLine(self):
        self.startLine = 0
        self.ayab_image.setStartLine(self.startLine)
        assert self.ayab_image.startLine() == 0
