# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import unicodedata
from inkex import NSS, Group, Layer, errormsg
from copy import deepcopy
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SODIPODI_INSENSITIVE, SVG_GROUP_TAG)
from .base import InkstitchExtension
from ..i18n import _


class LetteringFillComposedGlyphs(InkstitchExtension):
    """_summary_
    The goal of this extension is to help the font digitizer with steps to organize its work.
    At each step a group of glyphs are brought to the top of the font file, and the font
    digitizer should digitize these glyphs before going to next step.
    
    Steps are organized so has to break the work into smaller chunks and 
    maximize reuse of already digitized letters.
    
    unicodedata is used to decomposed letters into pieces
    furthermore the extension use some  additional information , such as "i" and "j" usually reuse
    the digitalization of "."
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--tabs")
        self.arg_parser.add_argument("-c", "--action", dest="action", type=str, default="none")

        
        self._glyphs_layers = []  # list of all Layers ()
        self._all_glyphs = []       # list of chr,   (one per layer)

        self._decomposition = {}    # keys are glyphs, value are the list of pieces in the decomposition
                                    # constructed using unicodedata.decomposition
        self._used_in_decompositions = {}  # reverse dictionary
        self._normalization ={}  # constructed using unicodedata.normalize('NFD', glyph)

        self._pieces = []           # all the  pieces for all decomposable glyphs
        self._missing = []          # pieces not already among _all_glyphs

       # self._substitutions = {}   substitution of a missing piece
        # self._is_substitute_for = {}    # reversed dictionary
        self._category_name = self._category_name()
    
    def _remove_empty_groups(self):
        for group in self.svg.iterdescendants(SVG_GROUP_TAG):
                if len(group.getchildren()) == 0:
                    group.delete()
        
    def _update_glyphs_layers(self):
            self._glyphs_layers = self.svg.xpath('.//svg:g[starts-with(@inkscape:label, "GlyphLayer-")]', namespaces=NSS)

    def _category_name(self):
        category_name = {}
        category_name["Lu"] = _("Upper Case Letters")
        category_name["Ll"] = _('Lower Case Letters')
        category_name["Lo"] = _('Other Letters')
        category_name["Nd"] = _("Digits")
        category_name["Sc"] = _('Symbols')
        category_name["Pc"] = _('Punctuation')
        category_name["Pe"] = _('Closing Punctuation')

        return category_name
    
    def _update_all_glyphs(self):
        # only consider GlyphLayer we  know the unicode they represent, that means there name is a single letter
        self._update_glyphs_layers()
        for layer in self._glyphs_layers:
            name = layer.attrib[INKSCAPE_LABEL]
            name = name.replace("GlyphLayer-", "", 1)

            if len(name) == 1:
                self._all_glyphs.append(name)

    def _fill_decompose_lists(self):
        # NFD normalization decomposes 'Ṓ' into three characters, letter O,  macron  accent and acute accent,
        # unicodedata.decomposition(Ṓ) splits into two entry points, one for 'Ō' and one for the acute accent
        # NFD normalization of 'a' is simply 'a', while unicodedata.decomposition('a') is an empty string.

        pieces = []
        for glyph in self._all_glyphs:
            normalization = [ char for char in unicodedata.normalize('NFD', glyph)]
            decomposition =[]

            for code  in unicodedata.decomposition(glyph).split(' '):
                try:
                    piece = chr(int(code, 16))
                    # we don't need the space separator nor the other separators as pieces, as they
                    # is nothing to render for them
                    if unicodedata.category(piece)[0] != 'Z':
                        decomposition.append(piece)
                except ValueError:  # this will eliminate code like <super> but keep codes like 03bc
                    pass
            if decomposition != []:
                self._decomposition[glyph] = decomposition
            if unicodedata.decomposition(glyph) == "":
                decomposition = [glyph]
            self._normalization[glyph] = normalization
            for piece in decomposition:
                if piece not in self._used_in_decompositions:
                    self._used_in_decompositions[piece] = [glyph]
                else:
                    self._used_in_decompositions[piece].append(glyph)
        self._pieces = [piece for piece in self._used_in_decompositions]
        self._missing = [piece for piece in self._pieces if piece not in self._all_glyphs and len(self._used_in_decompositions[piece])>1]

         

    def _find_layer(self, char):
        for layer in self._glyphs_layers:
            label = layer.attrib[INKSCAPE_LABEL]
            label = label.replace("GlyphLayer-", "", 1)
            if len(label) == 1 and label == char:
                return layer
        return None

    def _remove(self, char):
        char_layer = self._find_layer(char)
        if char_layer is not None:
            char_layer.delete()

    def _create_empty_glyph(self, char):
        new_layer = self.svg.add(Layer.new("GlyphLayer-" + char))
        new_layer.set("style", "display:none")
        return new_layer

    # Step 0: check for duplicate and remove unwanted layer

    def _look_for_duplicate(self, verbose=False):
        if len(self._all_glyphs) != len(set(self._all_glyphs)):
            duplicated_glyphs = " ".join(
                [glyph for glyph in set(self._all_glyphs) if self._all_glyphs.count(glyph) > 1]
            )
            errormsg(_("Found duplicated glyphs in font file: {duplicated_glyphs}").format(duplicated_glyphs=duplicated_glyphs))

            for letter in duplicated_glyphs:
                errormsg((unicodedata.name(letter)))
        else:
            if verbose:
                errormsg(_("No duplicated glyph found"))

    def _is_valid(self, char):
        # sometimes one grabs a non rendering char in the ttf file, and it results in
        # an invalid glyph (d='')
        if char == "":
            return True
        category = unicodedata.category(char)
        if category[0] in ['Z', 'C'] and category != 'Co':
            return False
        return True

    def _remove_invalid_glyphs(self):
        for layer in self._glyphs_layers:
            name = layer.attrib[INKSCAPE_LABEL]
            name = name.replace("GlyphLayer-", "", 1)
            if name == "" or name == ".null" or (len(name)==1 and not self._is_valid(name)):
                layer.delete()

        

    # Step1 time to digitize comma, hyphen and period:
    # move comma , hyphen and period on top
    # Lock all other glyhs

    def _lock_and_hide_all_layers(self):
        self._update_glyphs_layers()
        for layer in self._glyphs_layers:
            layer.set(SODIPODI_INSENSITIVE, True)
            layer.set("style", "display:none")

    def _move_on_top(self, layer):
        if SODIPODI_INSENSITIVE in layer.attrib:
            layer.pop(SODIPODI_INSENSITIVE)
        copy_layer = deepcopy(layer)
        layer.delete()
        self.svg.append(copy_layer)

    def _move_char_on_top(self, char):
        warning = False
        layer_char = self._find_layer(char)
        if layer_char is None:
            warning  = True
            self._create_empty_glyph(char)
        else:
            self._move_on_top(layer_char)
        return warning
    
    def _add_chars(self,char_list):
        self._lock_and_hide_all_layers()
        added =""
        for char in char_list:
            if self._move_char_on_top(char):
                added = added + char+ " "
        if added != "":
            added_char__warning = _(
            "This or these glyphs have been added:\n"
            "{added_char}\n"
            "Either  fill them or delete them" ).format(added_char = added)
            errormsg(added_char__warning)


        
    # Step 2
    # Find all non composed letters
    # Group them by category, all upper cases, lower cases, with group on top of the file

    def _create_empty_group(self, group_name):
        new_group = Group()
        new_group.label = group_name
        return new_group
    
    def _do_in_first_steps(self,glyph):
        # no decomposition for this glyph
        if unicodedata.decomposition(glyph) == "":
            return True
    
        # There is a decomposition,  but the decomposition is in only one piece, and this piece
        # is not used for anything else (this occurs for in the symbol for MICRO µ  is in the font, and the letter )
        # not sure here

        if len(self._decomposition[glyph]) == 1:
            piece = self._decomposition[glyph][0]
            if len(self._used_in_decompositions[piece]) == 1:
                return True
        return False

        
  
    def _fill_group(self, unicode_categories, excepting=[], adding=[], non_composed_only=True):
       # we want only the glyphs that can not be decomposed, it is not exactly the same thing
       # as having only one element in the NFD normalization 
       # (for instance a subscript is normalized to itself) but its decomposition is not "", but the 
       # non subscripted character 
        group_name = self._category_name[unicode_categories[0]]
        new_group = self._create_empty_group(group_name)
        glyphs = self._all_glyphs
     
        for glyph in glyphs:
            if not glyph in excepting:
                if unicodedata.category(glyph) in unicode_categories:
                    if not non_composed_only  or self._do_in_first_steps(glyph): 
                        ## traiter les subscript et mu
                        glyph_layer = self._find_layer(glyph)
                        if glyph_layer is not None:
                            if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                                glyph_layer.pop(SODIPODI_INSENSITIVE)
                            new_group.add(glyph_layer)
        for glyph in adding:
            if not non_composed_only or  self._do_in_first_steps(glyph):
                glyph_layer = self._find_layer(glyph)
                if glyph_layer is not None:
                    if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                        glyph_layer.pop(SODIPODI_INSENSITIVE)
                    new_group.add(glyph_layer)

        if len(new_group) > 0:
            self.svg.append(new_group)

    def _add_first_in_second(self, glyph_one, glyph_two):
        layer_one = self._find_layer(glyph_one)
        layer_two = self._find_layer(glyph_two)
        if layer_one is not None and layer_two is not None:
            layer_to_insert = deepcopy(layer_one)
            layer_to_insert.attrib[INKSCAPE_LABEL] = ' ' + glyph_one
            layer_to_insert.pop(INKSCAPE_GROUPMODE)
            layer_to_insert.set("style", "display:inline")
            if SODIPODI_INSENSITIVE in layer_to_insert:
                layer_to_insert.pop(SODIPODI_INSENSITIVE)
         #   layer_two.insert(0, layer_to_insert)
            layer_two.append(layer_to_insert)

    def _all_non_composed_letters_by_category(self):
       
        self._fill_group(['Lo', 'Lt', 'Lm'])
    
        self._add_first_in_second('.', 'i')
        self._add_first_in_second('.', 'j')
        self._fill_group(['Ll'])
        self._fill_group(['Lu'])
        
       

    # Step 3
    # Find all non composed digits and symbols
    # Group them as digits and symbols

    def _add_usually_used(self, usually_use):
        for B in usually_use:
            for A in usually_use[B]:
                self._add_first_in_second(A,B)


    def _digit_symbols_non_closing_punctuation(self):
    
        usually_use={}  
        usually_use[";"] = [",","."]
        usually_use[":"] = [".","."]
        usually_use["!"] = ["."]
        usually_use["?"] = ["."]
        usually_use["!"] = ["."]
        usually_use["_"] = ["-"]
        usually_use["¨"] = [".","."]
        usually_use["÷"] = [".","."]
        usually_use["%"] = [".","."]
        usually_use['0'] = ['O']
        usually_use['1'] = ['l', 'I']
        usually_use['÷'] = ['.', '.']
        usually_use['='] = ['-','-']
        usually_use['±'] = ['-']
        usually_use['$'] = ['S']
        usually_use["'"] = [',']

        self._add_usually_used(usually_use)
        self._fill_group(['Nd', 'Nl', 'No'])
        self._fill_group(['Sc', 'Sm', 'Sk', 'So'], excepting = [">"])
        self._fill_group(['Pc', 'Pd', 'Ps', 'Pi', 'Po'], excepting= ["¿", "¡", "/"])
        
    # Step 4
    # Punctuation 
    def _closing_punctuation(self):
        usually_use={}  
        usually_use["¿"] = ["?"]
        usually_use["¡"] = ["!"]
        usually_use[">"] = ["<"]
        usually_use[")"] = ["("]
        usually_use["}"] = ["{"]
        usually_use["]"] = ["["]
        usually_use["»"] = ["«"]
        usually_use['”'] = ['“']
        usually_use["’"] = ["‘"]
        usually_use["/"] = ["\\"]

        self._add_usually_used(usually_use)
        self._fill_group(['Pe', 'Pf'], excepting=[], adding=["¿", "¡", ">", "/"])


    # Step 5
    # There are several sorts of apostrophes and quotes depending of the used language. 
    # If there is at least one, now that it is supposedly digitalized, let us make sure that we have all those in ["'","’", "ʼ"]
    # Same for quotes

   

    def _deal_with_equivalences(self):
    
        apostrophes =["'", "’", "ʼ"]
        quotes_opening =['"', "«", '“']
        quotes_closing=['"', "»", '”']
        equivalences = [apostrophes, quotes_opening, quotes_closing]
        use_A_in_B = {}
        group_name = _("Additional Punctuation")
        new_group = self._create_empty_group(group_name)
        for equivalence in equivalences:
            use_to_represent = None
            for item in equivalence:
                if item in self._all_glyphs:
                    use_to_represent = item
                    break
            if use_to_represent is not None:
                for item in equivalence: 
                    if item not in self._all_glyphs:
                        item_layer = self._create_empty_glyph(item)
                        new_group.add(item_layer)
                        if use_to_represent  not in use_A_in_B:
                            use_A_in_B[use_to_represent] = [item]
                        else:
                            use_A_in_B[use_to_represent].append(item)
            
        if len(new_group) > 0:
            self.svg.append(new_group)
            self._update_glyphs_layers()
            for  use_to_represent in use_A_in_B:
                for char in use_A_in_B[use_to_represent]:
                    self._add_first_in_second(use_to_represent,char)
                   
    # To fill the composed glyphs we need diacritics (COMBINING ACCENT mostly) 
    # We may already have some of them already digitized , as a COMBINING ACCENT (Mark category) somemtimes 
    # has ann homoglyph MODIFIER LETTER ACCENT in the letter category and or an homoglyph ACCENT in the 
    # symmbol category.
    # 
    # At this step we want only diacritics without positioning  or doubling info. For instance, we  want the font digitizer
    # to create COMBINING ACUTE ACCENT, but to wait till next step for COMBININIG ACUTE ACCENT BELOW 
    # COMBINIG ACCENT ABOVE and COMBINING DOUBLE ACUTE ACCENT, not to do the same work several times.

    
    # create the missing diacritics. If the same drawing letter is here, we will fill the diacritic 
    # with it. Many diacritics are the samme, except for the positioning. For instance, for COMBINING ACUTE ACCENT 
    # has a corresponding letter MODIFIER LETTER ACUTE ACCENT

    # If(for instance) COMBINING ACUTE ACCENT is in the glyphs,we simply brinng it to the new group
    # of letters to be digitized.
    # If it is not here but we have the  corresponding MODIFIER LETTER, we create an empty glyph that 
    # contains the already digitized letter. If there is no such corresponding LETTER or SYMBol, we fill 
    # the empty glyph with a letter that uses the accent, so that the font digitizer knows what this
    # diacritics is supposed to look like   
    def _simplyfy_name(self,glyph):
        name = unicodedata.name(glyph)
        words = ["DOUBLE", "BELOW", "ABOVE", "INVERTED", "TURNED", "REVERSED"]
        simplified_name = name
        for word  in words:
            simplified_name = simplified_name.replace(word, "")

        return simplified_name

    def _has_simple_name(self, glyph):
       
        words = ["DOUBLE", "BELOW", "ABOVE", "INVERTED", "TURNED", "REVERSED"]
        for word in words:
            if word  in  unicodedata.name(glyph):
                return False
        return True

    def _use_modifier_letter_instead(self, missing_char):
        substitute = None
        if unicodedata.name(missing_char).startswith("COMBINING"):
            letter_name  = unicodedata.name(missing_char).replace("COMBINING", "MODIFIER LETTER")
            symbol_name = unicodedata.name(missing_char).replace("COMBINING ","")
            for glyph in self._all_glyphs:
                if unicodedata.name(glyph) == letter_name or unicodedata.name(glyph)== symbol_name:
                    substitute = glyph
                    break
        return substitute
    
    def _add_simple_diacritics(self):
        if self._missing == []:
            errormsg(_("nothing to do, you are ready for next step"))
        missing_group_name = _("Simple Diacritics")
        new_group = self._create_empty_group(missing_group_name)
        for glyph in self._missing:
            if self._has_simple_name(glyph):
                glyph_layer = self._create_empty_glyph(glyph)
                new_group.add(glyph_layer)
        self.svg.append(new_group)
        self._update_glyphs_layers()
        for glyph in self._missing:
            if self._has_simple_name(glyph):
                substitute = self._use_modifier_letter_instead(glyph)
                if substitute is not None:
                    self._add_first_in_second(substitute, glyph)
        
       
            
    #Step 6
    # at this step we deal with other diacritics.
    # if the diacritic is not present, we prefill the created layer with  one copy or two of the
    # corresponding simple diacritic, and additonaly one letter that does use the diacritics so that the font 
    # digitizer can move the simple diacritics t its rght position (and then delete the additional letter)
    
    def _add_other_diacritics(self):
        if self._missing == []:
            errormsg(_("nothing to do, you are ready for next step"))
        else :
            missing_group_name = _("Other Diacritics")
            new_group = self._create_empty_group(missing_group_name)
            for glyph in self._missing:
                glyph_layer = self._create_empty_glyph(glyph)
                new_group.add(glyph_layer)
            self.svg.append(new_group)
            self._update_glyphs_layers()
            for glyph in self._missing:
                simplified_name = self._simplyfy_name(glyph)
                substitute = None
                for candidate in self._all_glyphs:
                    if simplified_name.replace(" ","") == unicodedata.name(candidate).replace(" ",""):
                        substitute = candidate
                        break
                if substitute is None:
                    if "COMMA" in unicodedata.name(glyph):
                        substitute =','
                    if "DOT" in unicodedata.name(glyph):
                        substitute = "."
                
                if substitute is not None:
                        self._add_first_in_second(substitute, glyph)
                        if "DOUBLE" in unicodedata.name(glyph):
                                self._add_first_in_second(substitute, glyph)

                for char in self._used_in_decompositions[glyph]:
                    if unicodedata.category(char)[0] == 'L':
                        self._add_first_in_second (char, glyph)
                    break
            
        

    
    
    # Step 7 
    # Proceed with letters with decomposition of length 2

    def _fill_two_pieces_letters(self):
        glyphs_to_add = [glyph for glyph in self._all_glyphs if len(self._normalization[glyph]) == 2]
        also_take = [glyph for glyph in self._decomposition 
                     if len(self._normalization[glyph]) == 1]

        if glyphs_to_add == [] and also_take == []:
            errormsg(_("nothing to do, you are ready for next step"))
        else :
            group_name = _("Two pieces letters")
            new_group = self._create_empty_group(group_name)
            for glyph in glyphs_to_add:
                glyph_layer = self._find_layer(glyph)
                if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                    glyph_layer.pop(SODIPODI_INSENSITIVE)

                new_group.add(glyph_layer)
                for piece in self._normalization[glyph]:
                    self._add_first_in_second(piece, glyph)
               
            for glyph in also_take:
                glyph_layer = self._find_layer(glyph)
                if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                    glyph_layer.pop(SODIPODI_INSENSITIVE)

                new_group.add(glyph_layer)
                for piece in self._decomposition[glyph]:
                    self._add_first_in_second(piece, glyph)     
            self.svg.append(new_group)

    # Step 8
    # Proceed with letters with decomposition of length 3
    def _fill_other_letters(self):
        glyphs_to_add = [glyph for glyph in self._all_glyphs if len(self._normalization[glyph]) == 3]
        also_take = [glyph for glyph in self._all_glyphs
                     if len(self._normalization[glyph]) > 3]
       # errormsg(str(len(glyphs_to_add)))
      #  also_take =[]


        if glyphs_to_add == [] and also_take == []:
            errormsg(_("nothing to do, you are ready for next step"))
        else :
            group_name = _("Other composed letters")
            new_group = self._create_empty_group(group_name)
            for glyph in glyphs_to_add:
                glyph_layer = self._find_layer(glyph)
                if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                    glyph_layer.pop(SODIPODI_INSENSITIVE)

                new_group.add(glyph_layer)
                for piece in self._decomposition[glyph]:
                    self._add_first_in_second(piece, glyph)     
            for glyph in also_take:
                glyph_layer = self._find_layer(glyph)
                if SODIPODI_INSENSITIVE in glyph_layer.attrib:
                    glyph_layer.pop(SODIPODI_INSENSITIVE)
                new_group.add(glyph_layer)
                for piece in self._normalization[glyph]:
                    self._add_first_in_second(piece, glyph)
     
            self.svg.append(new_group)
    
    def effect(self):
        self.svg = self.document.getroot()
        self._update_glyphs_layers()
        self._update_all_glyphs()
        self._fill_decompose_lists()
         
           
        
        if self.options.action == 'step1':
            self._remove_invalid_glyphs()
            self._look_for_duplicate()
            self._add_chars([',','.','-'])
    
        if  self.options.action == 'step2':
            self._all_non_composed_letters_by_category()
            self._remove_empty_groups()

        if self.options.action == 'step3':
            self._digit_symbols_non_closing_punctuation()
            self._remove_empty_groups()

        if self.options.action == 'step4':
            self._closing_punctuation()
            self._remove_empty_groups()
        
        if self.options.action == 'step5':
            self._deal_with_equivalences()
            self._add_simple_diacritics()
            self._remove_empty_groups()
          
        if self.options.action == 'step6':
            self._add_other_diacritics()
            self._remove_empty_groups()
        
        if self.options.action == 'step7':
            self._fill_two_pieces_letters()
            self._remove_empty_groups()

        if self.options.action == 'step8':
            self._fill_other_letters()
            self._remove_empty_groups()

        #deal with decomposable in two pieces 

        #if self.options.action == 'step7':
        #deal with decomposable in three pieces 


            
        if self.options.action == 'duplicate':
            self._look_for_duplicate(verbose = True)
    
        if self.options.action == 'fill':
            self._fill_combined_glyphs()
        # if self.options.action == 'clean':
        #     self._clean_document()
        


# def _add_missing_pieces(self):

        
#         missing_group_name = _("Missing pieces")
#         new_group = self._create_empty_group(missing_group_name)
#         for char in self._missing:
#             char_layer =self._create_empty_glyph(char)
#             new_group.add(char_layer)
#         if len(new_group) > 0:
#             self.svg.append(new_group)
#             self._update_glyphs_layers() # but not yet the other lists
       
#             (is_substitution_for,also_add_in) = self._find_substitutions()
          
#             for char in is_substitution_for:
#                 self._add_first_in_second(is_substitution_for[char], char)
#             for char in also_add_in:
#                 self._add_first_in_second(also_add_in[char], char)



#     def _find_substitutions(self):
#         is_substitution_for =  {}
#         also_add_in = {}
#         missing_pieces = self._missing
#    #     self._fill_glyphs_lists() # now self._missing is empty
        
#         for piece in missing_pieces:
#             substitute = self._use_modifier_letter_instead(piece)
#             if substitute is not None:
#                 is_substitution_for[piece] = substitute
#                 missing_pieces.remove(piece)

#         for piece in missing_pieces:
#             substitute = self._try_without_position(piece)
#             if substitute is not None:
#                 is_substitution_for[piece] = substitute
#                 also_add_in[piece]  = self._find_letter_using(piece)
#                 missing_pieces.remove(piece)

#         for piece in missing_pieces:
#             substitute = self._try_using_other_position(piece)
#             if substitute is not None:
#                 is_substitution_for[piece] = substitute
#                 missing_pieces.remove(piece)

#             for char in self._used_in_decompositions[piece]:
#                 if unicodedata.category(char)[0] == 'L':
#                     also_add_in[piece] = char

#         return (is_substitution_for,also_add_in)
    
#     def _find_letter_using(self, piece):
#         letter = None
#         errormsg("used in decomposition")
#         for char in self._used_in_decompositions[piece]:
#             if unicodedata.category(char)[0] == 'L':
#                 letter = char
#                 break
#         return letter


#     def _try_without_position(self, missing_char):
#         substitute = None
#         if unicodedata.name(missing_char).endswith("BELOW") or unicodedata.name(missing_char).endswith("ABOVE"):
#             letter_name  = unicodedata.name(missing_char)[:-6]
#             for char in self._all_glyphs:
#                 if unicodedata.name(char) == letter_name:
#                     substitute = char
#                     break
#         return substitute
    
#     def _try_using_other_position(self, missing_char):
#         substitute = None
#         if unicodedata.name(missing_char).endswith("BELOW"):
#             letter_name  = unicodedata.name(missing_char).replace("BELOW", "ABOVE")
#             for char in self._all_glyphs:
#                 if unicodedata.name(char) == letter_name:
#                     substitute = char
#                     break
#         if unicodedata.name(missing_char).endswith("ABOVE"):
#             letter_name  = unicodedata.name(missing_char).replace("ABOVE", "BELOW")
#             for char in self._all_glyphs:
#                 if unicodedata.name(char) == letter_name:
#                     substitute = char
#                     break

#         return substitute