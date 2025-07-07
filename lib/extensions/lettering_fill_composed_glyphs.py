# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import unicodedata
from inkex import NSS, Layer, errormsg, addNS
from copy import deepcopy
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SODIPODI_INSENSITIVE, INKSTITCH_LETTER)
from .base import InkstitchExtension


class LetteringFillComposedGlyphs(InkstitchExtension):
    
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--tabs")
        self.arg_parser.add_argument("-c", "--action", dest="action", type=str, default="none")

        # é, à ,ç are all decomposable while  A or 9 are not decomposable
        self._all_glyphs = []       # all glyphs that may be decomposable
        self._decomposition = {}    # keys are decomposable glyphs, value are the list of pieces in the decomposition
        self._pieces = []           # all the  pieces for all decomposable glyphhs
        self._missing = []          # pieces not already among all_glyphs
        self._substitutions = {}    # substitution of a missing piece
        self._is_substitute_for = {}    # reversed dictionary
        self._used_in_decompositions = {}       # key is a piece, value is the list of all the decomposable glyphs
        # having the key in their decomposition
        self._glyphs_layers =[]  
        
    def _usable_decomposition(self, char):
        # unicodedata.decomposition(char) return a string that mixes keyword (eg <sub>) and int in base 16 , separated by ' '
        # for instance unicodedata.decomposition("é") == "0065 0301"
        # and unicededata.decomposition("₂") == "<sub> 0032"
        # we only want the pieces of the decomposition that corresponds to an hex int, and we don't want pieces that do not
        # render, like for instance SPACE
        usable_decomposition = []
        if unicodedata.decomposition(char) != "":
            for code in unicodedata.decomposition(char).split(' '):
                try:
                    piece = chr(int(code, 16))
                    # we don't need the space separator nor the other separators as pieces, as they
                    # is nothing to render for them
                    if unicodedata.category(piece)[0] != 'Z':
                        usable_decomposition.append(piece)
                except ValueError:  # this will eliminate code like <super> but keep codes like 03bc
                    pass
        return usable_decomposition
    
    def _update_glyphs_layers(self):
         self._glyphs_layers = self.svg.xpath('.//svg:g[starts-with(@inkscape:label, "GlyphLayer-")]', namespaces=NSS)
    
    def _fill_glyphs_list(self):
        # only consider GlyphLayer we  know the unicode they represent, that means there name is a single letter
        # _all_glyphs is the list  of these names
        # if a glyph can be decomposed, it belongs to the list of decomposable_glyphs, the pieces that result of its decompositons
        # go in the pieces list, and a dictionary remembers the list of decomposable_glyphs that are buitl with a given piece
        self._update_glyphs_layers()
        #self._glyphs_layers = self.svg.xpath('.//svg:g[starts-with(@inkscape:label, "GlyphLayer-")]', namespaces=NSS)
        for layer in self._glyphs_layers:
            name = layer.attrib[INKSCAPE_LABEL]
            name = name.replace("GlyphLayer-", "", 1)
      
            if len(name) == 1:
                self._all_glyphs.append(name)
                decomposed = self._usable_decomposition(name)
                if decomposed != []:
                    self._decomposition[name] = []
                    for piece in decomposed:
                        self._decomposition[name].append(piece)
                        self._pieces.append(piece)
                        if piece not in self._used_in_decompositions:
                            self._used_in_decompositions[piece] = [name]
                        else:
                            self._used_in_decompositions[piece].append(name)

        self._pieces = [p for p in set(self._pieces)]
        self._missing = [m for m in self._pieces if m not in self._all_glyphs and len(unicodedata.normalize('NFD',m))== 1]


    def remove_inkstitch_attributes(self, elements):
        param_to_remove = self.options.del_params
        for element in elements:
            for attrib in element.attrib:
                if attrib.startswith(NSS['inkstitch'], 1):
                    if param_to_remove == 'all' or attrib.endswith(param_to_remove):
                        del element.attrib[attrib]


    def _look_for_duplicate(self):
        if len(self._all_glyphs) != len(set(self._all_glyphs)):
            duplicated_glyphs = " ".join(
                [glyph for glyph in set(self._all_glyphs) if self._all_glyphs.count(glyph) > 1]
            )
            errormsg(("Found duplicated glyphs in font file: {duplicated_glyphs}").format(duplicated_glyphs=duplicated_glyphs))

            for letter in duplicated_glyphs:
                errormsg(unicodedata.name(letter))
        else:
            errormsg("no duplicated glyph found")
          

    def _check_for_missing_pieces(self):
        if self._missing != []:
            errormsg(str(len(self._missing)) + " missing  pieces: ")
            for char in self._missing:
                errormsg(' '+char)
                errormsg(unicodedata.name(char) +"\n")
        else:
            errormsg("nothing is missing")
         
    def _try_find_substitute(self, glyph, start_with_word, end_with_word, from_begining=True, from_ending=True):
        new_name = unicodedata.name(glyph)

        if from_begining:
            if unicodedata.name(glyph).startswith(start_with_word):
                new_name = new_name[len(start_with_word)+1:]

        if from_ending:
            if unicodedata.name(glyph).endswith(end_with_word):
                new_name = new_name[:-len(end_with_word)-1]

        try:
            substitute = unicodedata.lookup(new_name)
            if substitute in self._all_glyphs:
                self._substitutions[glyph] = substitute
                # if substitute not in self._is_substitute_for:
                #     self._is_substitute_for[substitute] = [glyph]
                # else:
                #     self._is_substitute_for[substitute].append(glyph)
        except KeyError:
            pass

    def _try_removing_positioning(self, glyph):
        # this will work for many diacritics,for instance this will allow to substitute ACUTE to COMBINING ACUTE BELOW
        self._try_find_substitute(glyph, "COMBINING", "", True, False)
        if glyph not in self._substitutions:
            self._try_find_substitute(glyph, "", "BELOW", False, True)
        if glyph not in self._substitutions:
            self._try_find_substitute(glyph, "", "ABOVE", False, True)
        if glyph not in self._substitutions:
            self._try_find_substitute(glyph, "COMBINING", "BELOW", True, True)
        if glyph not in self._substitutions:
            self._try_find_substitute(glyph, "COMBINING", "ABOVE", True, True)

    def _build_substitution_dict(self):
        for glyph in self._missing:
            self._try_removing_positioning(glyph)
        for c in self._missing:
            if c not in self._substitutions:
                # if removing positioning was not enough, we can try to simplify the name further
                simplified_name = unicodedata.name(c).replace("COMBINING", "").replace("BELOW", "").replace("ABOVE", "").replace("SMALL", "")
                for char in self._all_glyphs:
                    try:
                        if simplified_name in unicodedata.name(char):
                            self._substitutions[c] = char
                            break
                    
                    except ValueError:
                        pass
             # if this did not work,find any glyph that uses this piece
            if c not in self._substitutions:
                if c in self._used_in_decompositions:
                        for name in self._used_in_decompositions[c]:
                            if name in self._all_glyphs:
                                self._substitutions[c] = name
                                break

        for glyph, substitute in self._substitutions.items():
            if substitute not in self._is_substitute_for:
                self._is_substitute_for[substitute] = [glyph]
            else:
                self._is_substitute_for[substitute].append(glyph)

        errormsg(self._substitutions)
        results = [len(value) for value in self._is_substitute_for.values()]
        errormsg(self._is_substitute_for)
        errormsg(results)

    def _min_level_decomposition(self):
        min_level = 1000
        for layer in self._glyphs_layers:
            if INKSTITCH_LETTER in layer.attrib:
                decomposition = layer.get(INKSTITCH_LETTER,"")
                if len(decomposition) < min_level:
                    min_level = len(decomposition)
        return min_level
    

    def _add_attribute_letter(self):
      
        # we want a layer to have the INKSTITCH_LETTER tag if it is too early to digitilize it 
        # for embroidery because we can reuse some pieces for it
        # theINKSTITCH_LETTER tag is set to the string obtained in concataning all glyphs that must be
        # dealt first

        self._update_glyphs_layers()
        # this deal will glyphs originally there: glyph_layers is updated
        # but all_glyphs is still the originally present letters
        for char in self._all_glyphs:
            decomposition_string = ""
       
            if char in  self._decomposition:   
                for piece in self._decomposition[char]:
                    decomposition_string += piece
                layer = self._find_layer(char)
                layer.set(INKSTITCH_LETTER, decomposition_string)
        # now let's deal with the just added glyphs, they are already filled.
        # we don't want to digitize twice the same thing but maybe the same
        # new_layers were created for all keys of self._substitution

        for char  in self._is_substitute_for:
            # if an original char is used as substitute, don't digitilize it now,
            # replace it later by the piece it substitude, as it could be close
            char_layer = self._find_layer(char)
            char_layer.set(INKSTITCH_LETTER, ' '+self._is_substitute_for[char][0])
          
            for  new_char in self._is_substitute_for[char][1:]:
                new_char_layer = self._find_layer(new_char)

               # for everything in new_char_layer.getchildren():
               #     del everything
                #empty new_char_layer
                new_char_layer.set(INKSTITCH_LETTER, self._is_substitute_for[char][0])


        

    def _clean_document(self):
        self._glyphs_groups = self.svg.xpath('.//svg:g', namespaces=NSS)
        for layer in self._glyphs_groups:
            self._clean_layer(layer)

    def _clean_layer(self,layer):
          if INKSTITCH_LETTER in layer.attrib:
            del layer.attrib[INKSTITCH_LETTER]
    
    def _create_empty_glyph(self, char):
        return self.svg.add(Layer.new("GlyphLayer-"+char))

    def _find_layer(self, char, ):
        #glyph_layers = self.svg.xpath('.//svg:g[starts-with(@inkscape:label, "GlyphLayer-")]', namespaces=NSS)
        for layer in self._glyphs_layers:
            label = layer.attrib[INKSCAPE_LABEL]
            label = label.replace("GlyphLayer-", "", 1)
    
            if len(label) == 1 and label == char:
               return layer    

    def _create_glyph_guessing(self, char):
        new_glyph = self._create_empty_glyph(char)
        new_glyph.set("style", "display:none")
      #  new_glyph.set(INKSTITCH_LETTER, char)

        if char in self._substitutions:
            substitution_char = self._substitutions[char]
            layer = self._find_layer(substitution_char)
            node = deepcopy(layer)
            self._clean_layer(node)
            node.attrib[INKSCAPE_LABEL] = " " + substitution_char
            node.attrib.pop(INKSCAPE_GROUPMODE) 
            node.set("style", "display:inline")

            new_glyph.insert(0, node)

            if unicodedata.category(self._substitutions[char])[0] not in ['L']:
                # we probably have lost the position, let's add a letter to 
                # give positional information
                letter_layer = None
                for name in self._used_in_decompositions[char]:
                    if unicodedata.category(name)[0] in ['L']:
                        letter_layer = self._find_layer(name)
                        break
                if letter_layer is not None:
                    letter_node = deepcopy(letter_layer)
                    letter_node.attrib[INKSCAPE_LABEL] = " " + name
                    letter_node.attrib[INKSCAPE_GROUPMODE] = ""
                    letter_node.set("style", "display:inline")
                    self._clean_layer(letter_node)
                    new_glyph.insert(0, letter_node)

    def  _fill_combined_glyph(self, glyph_layer):
 
        label = glyph_layer.attrib[INKSCAPE_LABEL]
        glyph = label.replace("GlyphLayer-", "", 1)
           
     #   glyph_layer = self._find_layer(glyph)
        if not glyph_layer.get(SODIPODI_INSENSITIVE):
            for piece in self._decomposition[glyph]:
                piece_layer = deepcopy(self._find_layer(piece))
                piece_layer.attrib[INKSCAPE_LABEL] = ' ' + piece
                piece_layer.attrib[INKSCAPE_GROUPMODE] = ""
                piece_layer.set("style", "display:inline")
                self._clean_layer(piece_layer)
                glyph_layer.insert(0, piece_layer)

    def _fill_combined_glyphs(self):
        if self._missing != []:
            errormsg(("Some combining glyphs are missing, please create them first"))
        else:
            for layer in self._glyphs_layers:
                if INKSTITCH_LETTER in layer.attrib:
            #for glyph in self._decomposition:
                   # self._fill_combined_glyph(glyph)
                    self._fill_combined_glyph(layer)
                    del layer.attrib[INKSTITCH_LETTER]

    def _lock_non_ready_glyphs(self):
        # lock all glyphs that are combined glyphs or are used to recreate a missing glyph
        min_level = self._min_level_decomposition()
        max_level = self._max_level_decomposition()
        errormsg(str(min_level))
        errormsg(str(max_level))
        errormsg(str(len(self._glyphs_layers)))
        for layer in self._glyphs_layers:
          
            layer.pop(SODIPODI_INSENSITIVE)
            if min_level == 0:
                if INKSTITCH_LETTER in layer.attrib:
                        decomposition =""
                    
                        if layer.get(INKSTITCH_LETTER, "") != "":
                            decomposition = layer.get(INKSTITCH_LETTER, "")
                       # if len(decomposition) != 0:
                            layer.set(SODIPODI_INSENSITIVE, True)

            # if INKSTITCH_LETTER in layer.attrib:
            #     decomposition = ""
            #     try: 
            #         decomposition = str(layer.get(INKSTITCH_LETTER))
            #         if len(decomposition) != min_level:
            #             layer.set(SODIPODI_INSENSITIVE, True)
            #     except KeyError:
            #         pass

                   

    def _create_empty_glyphs(self):
        for char in self._missing:
            self._create_empty_glyph(char)
        

    def _create_glyphs_guessing(self):
        for char in self._substitutions:
            if self._find_layer(self._substitutions[char]) is not None:
                self._create_glyph_guessing(char)


    def effect(self):
        self.svg = self.document.getroot()
        self._fill_glyphs_list()
     #   self._build_substitution_dict()
        
   
        if self.options.action == 'check_missing':
            self._check_for_missing_pieces()
        if self.options.action == 'duplicate':
            self._look_for_duplicate()
     #   if self.options.action == 'create_empty':
     #       self._create_empty_glyphs()
        if self.options.action == 'create_guessing':
            self._build_substitution_dict()
            self._create_glyphs_guessing()
            self._add_attribute_letter()
        if self.options.action == 'lock_combined_glyphs':
            self._lock_non_ready_glyphs()
        if self.options.action == 'fill':
            self._fill_combined_glyphs()
        if self.options.action == 'clean':
            self._clean_document()