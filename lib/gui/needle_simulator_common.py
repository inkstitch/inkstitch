from itertools import izip

import numpy
import wx
import math

from lib.gui.generic_simulator import BaseDrawingPanel
from lib.stitch_plan.stitch_blocks import PIXEL_DENSITY
from lib.svg import PIXELS_PER_MM


class NeedleDistanceInformation:
    def __init__(self, pixel_density, pixels_per_mm):
        self.pixel_density = pixel_density
        self.pixels_per_mm = pixels_per_mm
        self.np_needle_points_mm = None
        self.np_needle_points_display = None
        self.calculated_needle_pens = []
        self.calculated_needle_points = []
        # TODO likely speed things up a bit if these are defined as preallocated numpy arrays
        self.minx = None
        self.miny = None

    def number_of_calculated_needle_points(self):
        return len(self.calculated_needle_pens)

    def number_of_input_needle_points(self):
        return len(self.np_needle_points_mm)

    def xrange_needle_points_left_to_calculate(self):
        return xrange(self.number_of_calculated_needle_points(), self.number_of_input_needle_points())

    def point_display(self, int_this_needle_point):
        return self.np_needle_points_display[int_this_needle_point]

    def point_mm(self, current_needle_point):
        return self.np_needle_points_mm[current_needle_point]

    def x_and_y_for_point_mm(self, current_needle_point):
        return self.np_needle_points_mm[current_needle_point, 0], self.np_needle_points_mm[current_needle_point, 1]

    def bol_array_points_close_to_x_mm(self, current_x_mm, max_x_distance_mm):
        return numpy.isclose(self.np_needle_points_mm[:, 0], current_x_mm, 0, max_x_distance_mm)

    def bol_array_points_close_to_y_mm(self, current_y_mm, max_y_distance_mm):
        return numpy.isclose(self.np_needle_points_mm[:, 1], current_y_mm, 0, max_y_distance_mm)

    def needle_points_mm_for_and_of_bol_arrays(self, np_possibly_close_x, np_possibly_close_y):
        return self.np_needle_points_mm[numpy.logical_and(np_possibly_close_x, np_possibly_close_y)]

    def update_minx_and_miny(self, minx, miny):
        self.minx = minx
        self.miny = miny

    def load_all_needle_points(self, pens, stitch_blocks):
        self.np_needle_points_mm = numpy.empty((0, 2), float)
        self.np_needle_points_display = numpy.empty((0, 2), float)
        # TODO change above to preallocate size, will speed it up
        for pen, stitches in izip(pens, stitch_blocks):
            for stitch in stitches:
                self.np_needle_points_mm = numpy.append(self.np_needle_points_mm,
                                                        [[self.scale_to_color_block_xpoint(stitch[0]),
                                                          self.scale_to_color_block_ypoint(stitch[1])]], axis=0)
                self.np_needle_points_display = numpy.append(self.np_needle_points_display,
                                                             [[stitch[0],
                                                               stitch[1]]], axis=0)

    def scale_to_color_block_xpoint(self, stitch_block_point):
        return (stitch_block_point / self.pixel_density + self.minx) / self.pixels_per_mm

    def scale_to_color_block_ypoint(self, stitch_block_point):
        return (stitch_block_point / self.pixel_density + self.miny) / self.pixels_per_mm

    def calculate_distance_up_to_current_point(self, current_stitch, distance_search):
        # TODO in all these, I likely should ignore counting STOP commands?
        last_calculated_needle_point = self.number_of_calculated_needle_points()
        for int_this_needle_point in self.xrange_needle_points_left_to_calculate():
            this_needle_point_display = self.point_display(int_this_needle_point)
            if last_calculated_needle_point < current_stitch:
                needle_pen = self.select_pen_per_min_distance(last_calculated_needle_point, distance_search)
                self.append_needle_pen(needle_pen)
                self.append_calculated_point_as_x_line(this_needle_point_display, needle_pen.width)
                # self.canvas.DrawLines(((this_needle_point_display[0] - 1, this_needle_point_display[1]),
                #                       (this_needle_point_display[0] + 1, this_needle_point_display[1])))
                # self.draw_crosshair(this_needle_point_display[0], this_needle_point_display[1], self.canvas,
                # self.transform)
                # self.canvas.DrawPointList([(this_needle_point_display[0], this_needle_point_display[1])])
                # self.dc.DrawCircle(int(this_needle_point_display[0]), int(this_needle_point_display[1]),8)
                # self.canvas.StrokeLineSegments((this_needle_point_display[0], this_needle_point_display[1]),
                #                               (this_needle_point_display[0], this_needle_point_display[1]))
                last_calculated_needle_point += 1
            else:
                break
        return last_calculated_needle_point

    def select_pen_per_min_distance(self, current_needle_point, distance_search):
        pen_info = NeedlePenInfo("BLACK", 2)
        self.check_distance_limits_for_axis_candidates(current_needle_point, pen_info, distance_search)
        return distance_search.pen_info

    def append_needle_pen(self, needle_pen):
        self.calculated_needle_pens.append([needle_pen.colour, needle_pen.width])

    def append_calculated_point_as_x_line(self, this_needle_point_display, x_length):
        self.calculated_needle_points.append([this_needle_point_display[0] - x_length / 2,
                                              this_needle_point_display[1],
                                              this_needle_point_display[0] + x_length / 2,
                                              this_needle_point_display[1]])

    def check_distance_for_axis_candidates(self, current_needle_point, pen_info, distance_search):
        current_x, current_y = self.x_and_y_for_point_mm(current_needle_point)
        distance_search.reset_for_next_point_check(pen_info)
        np_possibly_close_x = self.bol_array_points_close_to_x_mm(
            current_x, distance_search.thread_to_thread_warning_mm)
        np_possibly_close_y = self.bol_array_points_close_to_y_mm(
            current_y, distance_search.thread_to_thread_warning_mm)
        # np_possibly_close = self.get_bol_array_points_close_to_point_mm(
        #    current_needle_point, distance_search.thread_to_thread_warning_mm)
        distance_search.check_if_candidate_points_are_close(
                current_x, current_y, self.needle_points_mm_for_and_of_bol_arrays(np_possibly_close_x,
                                                                                  np_possibly_close_y))
        # distance_search.check_if_candidate_points_are_close(
        #        current_x, current_y, self.get_needle_points_mm_for_bol_array(np_possibly_close))

    def check_distance_limits_for_axis_candidates(self, current_needle_point, pen_info, distance_search):
        current_x, current_y = self.x_and_y_for_point_mm(current_needle_point)
        for this_limit_to_compare in xrange(distance_search.number_of_distance_limits):
            distance_search.reset_for_next_point_check(pen_info)
            if distance_search.pen_info.colour != "PURPLE":
                np_possibly_close_x = self.bol_array_points_close_to_x_mm(
                    current_x, distance_search.get_distance_limit(this_limit_to_compare))
                np_possibly_close_y = self.bol_array_points_close_to_y_mm(
                    current_y, distance_search.get_distance_limit(this_limit_to_compare))
                distance_search.check_if_candidate_points_are_close_to_this_limit(
                    self.point_mm(current_needle_point),
                    self.needle_points_mm_for_and_of_bol_arrays(np_possibly_close_x, np_possibly_close_y),
                    this_limit_to_compare)

    def last_calculated_stitch_as_list(self):
        return self.np_needle_points_display[self.number_of_calculated_needle_points() - 1].tolist()

    def calculated_stitch_at_index_as_list(self, wanted_index):
        return self.np_needle_points_display[wanted_index].tolist()


class NeedleDensityInformation(NeedleDistanceInformation):
    def __init__(self, pixel_density, pixels_per_mm):
        NeedleDistanceInformation.__init__(self, pixel_density, pixels_per_mm)
        # Do not add instance variables here, since class is casted

    def bol_array_points_close_to_point_mm(self, current_needle_point, max_point_distance_mm):
        return numpy.isclose(self.np_needle_points_mm,
                             self.np_needle_points_mm[current_needle_point], 0, max_point_distance_mm)

    def needle_points_mm_for_bol_array(self, np_bol_array):
        return self.np_needle_points_mm[np_bol_array]

    def check_one_density_for_axis_candidates(self, current_needle_point, pen_info,
                                              thread_to_thread_density_search):
        current_x, current_y = self.x_and_y_for_point_mm(current_needle_point)
        thread_to_thread_density_search.reset_for_next_point_check(pen_info)
        np_possibly_close_x = self.bol_array_points_close_to_x_mm(
            current_x, thread_to_thread_density_search.density_area_radius_mm)
        np_possibly_close_y = self.bol_array_points_close_to_y_mm(
            current_y, thread_to_thread_density_search.density_area_radius_mm)
        np_possibly_close_combined = self.needle_points_mm_for_and_of_bol_arrays(np_possibly_close_x,
                                                                                 np_possibly_close_y)
        thread_to_thread_density_search.count_points_in_density_radius(current_x, current_y, np_possibly_close_combined)
        thread_to_thread_density_search.translate_count_to_density_colour()
        return current_x, current_y, np_possibly_close_combined

    def calculate_needle_density_up_to_current_point(self, current_stitch, thread_to_thread_density_search):
        last_calculated_needle_point = self.number_of_calculated_needle_points()
        for int_this_needle_point in self.xrange_needle_points_left_to_calculate():
            this_needle_point_display = self.point_display(int_this_needle_point)
            if last_calculated_needle_point < current_stitch:
                needle_pen = self.select_pen_per_density_count(last_calculated_needle_point,
                                                               thread_to_thread_density_search)
                self.append_needle_pen(needle_pen)
                self.append_calculated_point_as_x_line(this_needle_point_display, needle_pen.width)
                last_calculated_needle_point += 1
            else:
                break
        return last_calculated_needle_point

    def select_pen_per_density_count(self, current_needle_point, thread_to_thread_density_search):
        pen_info = NeedlePenInfo("BLACK", 2)
        self.check_one_density_for_axis_candidates(current_needle_point, pen_info, thread_to_thread_density_search)
        return thread_to_thread_density_search.pen_info


class ThreadDensityInformation(NeedleDensityInformation):
    def __init__(self, pixel_density, pixels_per_mm):
        NeedleDensityInformation.__init__(self, pixel_density, pixels_per_mm)
        # Do not add instance variables here, since class is casted

    def append_calculated_thread_pen(self, this_needle_point_display, thread_to_thead_needle_pen):
        self.append_needle_pen(thread_to_thead_needle_pen)
        self.append_calculated_point_as_x_line(this_needle_point_display, thread_to_thead_needle_pen.width)

    def check_thread_densities_for_axis_candidates(self, current_needle_point, pen_info,
                                                   thread_to_core_density_search, thread_to_thread_density_search):
        current_x, current_y, np_possibly_close_combined = self.check_one_density_for_axis_candidates(
            current_needle_point, pen_info, thread_to_thread_density_search)
        thread_to_core_density_search.reset_for_next_point_check(pen_info)
        thread_to_core_density_search.count_points_in_density_radius(current_x, current_y, np_possibly_close_combined)
        thread_to_core_density_search.translate_count_to_density_colour()

    def calculate_thread_density_up_to_current_point(self, current_stitch, thread_to_core_density_search,
                                                     thread_to_thread_density_search):
        last_calculated_needle_point = self.number_of_calculated_needle_points()
        for int_this_needle_point in self.xrange_needle_points_left_to_calculate():
            this_needle_point_display = self.point_display(int_this_needle_point)
            if last_calculated_needle_point < current_stitch:
                thread_to_thread_needle_pen = self.select_pen_per_thread_density_count(
                    last_calculated_needle_point, thread_to_core_density_search, thread_to_thread_density_search)
                self.append_calculated_thread_pen(this_needle_point_display, thread_to_thread_needle_pen)
                # self.append_calculated_thread_pen(this_needle_point_display, thread_to_core_needle_pen)
                last_calculated_needle_point += 1
            else:
                break
        return last_calculated_needle_point

    def select_pen_per_thread_density_count(self, current_needle_point, thread_to_core_density_search,
                                            thread_to_thread_density_search):
        pen_info = NeedlePenInfo("BLACK", 2)
        self.check_thread_densities_for_axis_candidates(current_needle_point, pen_info, thread_to_core_density_search,
                                                        thread_to_thread_density_search)
        self.evaluate_thread_to_core_and_to_thread_together(thread_to_core_density_search,
                                                            thread_to_thread_density_search)
        return thread_to_thread_density_search.pen_info

    def evaluate_thread_to_core_and_to_thread_together(self, thread_to_core_density_search,
                                                       thread_to_thread_density_search):
        if not self.evaluate_specific_warning_colour_for_core_and_thread(
                "PURPLE", thread_to_core_density_search, thread_to_thread_density_search):
            if not self.evaluate_specific_warning_colour_for_core_and_thread(
                    "RED", thread_to_core_density_search, thread_to_thread_density_search):
                if not self.evaluate_specific_warning_colour_for_core_and_thread(
                        "ORANGE", thread_to_core_density_search, thread_to_thread_density_search):
                    self.evaluate_specific_warning_colour_for_core_and_thread(
                        "SKY_BLUE", thread_to_core_density_search, thread_to_thread_density_search)
        return

    def evaluate_specific_warning_colour_for_core_and_thread(self, thread_colour,
                                                             thread_to_core_density_search,
                                                             thread_to_thread_density_search):
        if thread_to_thread_density_search.pen_info.colour == thread_colour:
            return True
        else:
            if thread_to_core_density_search.pen_info.colour == thread_colour:
                thread_to_thread_density_search.pen_info.colour = thread_colour
                return True
        return False


class NeedleDrawingPanel(BaseDrawingPanel):
    """"""

    def __init__(self, *args, **kwargs):
        BaseDrawingPanel.__init__(self, *args, **kwargs)
        self.needle_density_info = NeedleDistanceInformation(PIXEL_DENSITY, PIXELS_PER_MM)

    def load(self, stitch_plan):
        self.initialize_load(stitch_plan)
        self.needle_density_info.update_minx_and_miny(self.minx, self.miny)
        self.needle_density_info.load_all_needle_points(self.stitch_block_info.pens,
                                                        self.stitch_block_info.stitch_blocks)
        self.start_simulation_after_load()

    def output_needle_points_up_to_current_point(self, dp_wanted_stitch, suppress_colours=None):
        for this_calculated_point in xrange(dp_wanted_stitch):
            needle_pen_attributes = self.needle_density_info.calculated_needle_pens[this_calculated_point]
            if (suppress_colours is None) or (not needle_pen_attributes[0] in suppress_colours):
                # TODO make a tick box option to deselect showing of black points
                self.canvas.SetPen(wx.Pen(wx.Colour(needle_pen_attributes[0]), needle_pen_attributes[1]))
                needle_line_points = self.needle_density_info.calculated_needle_points[this_calculated_point]
                self.canvas.DrawLines(((needle_line_points[0], needle_line_points[1]),
                                      (needle_line_points[2], needle_line_points[3])))
            # self.canvas.DrawLineList(self.calculated_needle_points, pens=self.calculated_needle_pens)
            # calculated_wx_pens = []
            # pen_colour, pen_width = self.calculated_needle_pens[this_calculated_point]
            # calculated_wx_pens.append(wx.Pen(wx.Colour(pen_colour), pen_width))
            # this_needle_point_display = self.np_needle_points_mm[this_calculated_point]
            # self.dc.DrawLineList(this_calculated_point - 100, this_calculated_point-10,
            #                     this_calculated_point + 100, this_calculated_point+10,
            #                     pens=calculated_wx_pens)
            # self.dc.DrawLineList([this_needle_point_display[0] - 1, this_needle_point_display[1],
            #                     this_needle_point_display[0] + 1, this_needle_point_display[1]],
            #                     pens=calculated_wx_pens)

    def initialise_distance_search_with_limits(self, options=None):
        pen_info = NeedlePenInfo("BLACK", 2)
        thread_to_core_warning_mm = NeedleCommonSearch.THREAD_TO_CORE_WARNING_MM
        thread_to_thread_warning_mm = NeedleCommonSearch.THREAD_TO_THREAD_WARNING_MM
        if options is not None:
            if options.purple_distance_mm:
                thread_to_core_warning_mm = options.purple_distance_mm
            if options.blue_distance_mm:
                thread_to_thread_warning_mm = options.blue_distance_mm
        distance_search = NeedleDistanceSearch(pen_info, thread_to_core_warning_mm=thread_to_core_warning_mm,
                                               thread_to_thread_warning_mm=thread_to_thread_warning_mm)
        distance_search.add_distance_limit(distance_search.thread_to_core_warning_mm, "PURPLE", 4, 1)
        distance_search.add_distance_limit(distance_search.thread_to_thread_warning_mm, "SKY BLUE", 3, 2)
        return distance_search


class NeedlePenInfo:
    def __init__(self, pen_colour, pen_width):
        self.colour = pen_colour
        self.width = pen_width

    def update(self, colour, width):
        self.colour = colour
        self.width = width


class NeedleCommonSearch:
    THREAD_DIAMETER_MM = 0.4
    THREAD_RADIUS_OVERLAP = 0.05
    THREAD_TO_CORE_WARNING_MM = THREAD_DIAMETER_MM / 2 - THREAD_RADIUS_OVERLAP
    THREAD_TO_THREAD_WARNING_MM = THREAD_DIAMETER_MM - THREAD_RADIUS_OVERLAP * 2

    def __init__(self, pen_info, thread_to_core_warning_mm=THREAD_TO_CORE_WARNING_MM,
                 thread_to_thread_warning_mm=THREAD_TO_THREAD_WARNING_MM,
                 bol_found_short_distance=False, int_found_same_points=0, int_level_of_search=1):
        self.thread_to_core_warning_mm = thread_to_core_warning_mm
        self.thread_to_thread_warning_mm = thread_to_thread_warning_mm
        self.pen_info = pen_info
        self.int_found_same_points = int_found_same_points
        self.level_of_search = int_level_of_search
        self.found_short_distance = bol_found_short_distance

    @property
    def thread_to_core_warning_mm(self):
        return self.thread_to_core_warning_mm

    @thread_to_core_warning_mm.setter
    def thread_to_core_warning_mm(self, value):
        self.thread_to_core_warning_mm = value

    @property
    def thread_to_thread_warning_mm(self):
        return self.thread_to_core_warning_mm

    @thread_to_thread_warning_mm.setter
    def thread_to_thread_warning_mm(self, value):
        self.thread_to_core_warning_mm = value

    def reset_count_of_same_points(self):
        self.int_found_same_points = 0

    def reset_for_next_point_check(self, pen_info):
        self.reset_count_of_same_points()
        self.found_short_distance = False
        self.pen_info = pen_info

    def possible_same_point(self):
        return self.int_found_same_points < self.level_of_search

    def increase_possibly_seen_same_points(self):
        self.int_found_same_points += 1

    @property
    def pen_info(self):
        return self.pen_info

    @pen_info.setter
    def pen_info(self, value):
        self.pen_info = value

    @property
    def found_short_distance(self):
        return self.found_short_distance

    @found_short_distance.setter
    def found_short_distance(self, value):
        self.found_short_distance = value

    def mark_distance_as_found(self):
        self.found_short_distance = True

    @property
    def level_of_search(self):
        return self.int_level_of_search

    @level_of_search.setter
    def level_of_search(self, value):
        self.int_level_of_search = value


class NeedleDistanceSearch(NeedleCommonSearch):

    def __init__(self, pen_info,
                 thread_to_core_warning_mm=NeedleCommonSearch.THREAD_TO_CORE_WARNING_MM,
                 thread_to_thread_warning_mm=NeedleCommonSearch.THREAD_TO_THREAD_WARNING_MM,
                 bol_found_short_distance=False, int_found_same_points=0, int_level_of_search=1):
        NeedleCommonSearch.__init__(self, pen_info, thread_to_core_warning_mm, thread_to_thread_warning_mm,
                                    bol_found_short_distance, int_found_same_points, int_level_of_search)
        self.distance_limits = []

    def add_distance_limit(self, distance_limit_mm, pen_colour, pen_width, int_level_of_search):
        self.distance_limits.append([distance_limit_mm, pen_colour, pen_width, int_level_of_search])

    def get_distance_limit(self, distance_limit_index):
        return self.distance_limits[distance_limit_index][0]

    @property
    def number_of_distance_limits(self):
        return len(self.distance_limits)

    def select_pen_for_distance_vs_limit(self, this_distance, distance_limit_index):
        self.level_of_search = self.distance_limits[distance_limit_index][3]
        if this_distance <= self.get_distance_limit(distance_limit_index):
            # if this_distance < 15:
            #    print(str(this_distance)+","+str(possibly_close[0])+","+str(possibly_close[1])+",
            #          "+str(current_x)+","+str(current_y))
            if (this_distance == 0) and self.possible_same_point():
                self.increase_possibly_seen_same_points()
            else:
                self.pen_info.update(self.distance_limits[distance_limit_index][1],
                                     self.distance_limits[distance_limit_index][2])
                self.mark_distance_as_found()
        return self.found_short_distance

    def check_if_candidate_points_are_close(self, current_x, current_y, np_possibly_close):
        for possibly_close in np_possibly_close:
            this_distance = numpy.linalg.norm(possibly_close - [current_x, current_y])
            for this_limit_to_compare in xrange(self.number_of_distance_limits):
                if self.select_pen_for_distance_vs_limit(this_distance, this_limit_to_compare):
                    break
        return self.found_short_distance

    def check_if_candidate_points_are_close_to_this_limit(self, this_numpy_point, np_possibly_close,
                                                          this_limit_to_compare):
        for possibly_close in np_possibly_close:
            this_distance = numpy.linalg.norm(possibly_close - [this_numpy_point])
            if self.select_pen_for_distance_vs_limit(this_distance, this_limit_to_compare):
                break
        return self.found_short_distance


class NeedleDensitySearch(NeedleCommonSearch):
    def __init__(self, pen_info, density_area_radius_mm=0.5,
                 thread_to_core_warning_mm=NeedleCommonSearch.THREAD_TO_CORE_WARNING_MM,
                 thread_to_thread_warning_mm=NeedleCommonSearch.THREAD_TO_THREAD_WARNING_MM,
                 bol_found_short_distance=False, int_found_same_points=0, int_level_of_search=1,
                 int_number_within_limit=0, found_needle_within_limit=False):
        NeedleCommonSearch.__init__(self, pen_info, thread_to_core_warning_mm, thread_to_thread_warning_mm,
                                    bol_found_short_distance, int_found_same_points, int_level_of_search)
        self.density_area_radius_mm = density_area_radius_mm
        self.number_counted_within_limit = int_number_within_limit
        self.density_limits = []
        self.terrible_density_limit_count = 11
        self.bad_density_limit_count = 9
        self.warn_density_limit_count = 7
        self.high_density_limit_count = 5
        self.found_needle_within_limit = found_needle_within_limit

    def other_threads_perfectly_fitting_within_radius(self):
        area_examined_mm2 = math.pi * math.pow(self.density_area_radius_mm, 2)
        area_needed_by_a_thread_mm2 = math.pi * math.pow(NeedleCommonSearch.THREAD_DIAMETER_MM / 2, 2)
        return area_examined_mm2 / area_needed_by_a_thread_mm2 - 1

    def int_other_threads_perfectly_fitting_within_radius(self):
        return int(self.other_threads_perfectly_fitting_within_radius())

    def set_density_limits_based_on_radius_and_thread(self):
        perfect_count_other_threads = self.other_threads_perfectly_fitting_within_radius()
        int_perfect_count_other_threads = self.int_other_threads_perfectly_fitting_within_radius()
        int_additional_step_to_add_above_one = int(int_perfect_count_other_threads/5)
        if perfect_count_other_threads >= 0:
            self.high_density_limit_count = int_perfect_count_other_threads
            self.set_density_limits_for_all_after_high(self.high_density_limit_count,
                                                       int_additional_step_to_add_above_one)
        else:
            self.set_density_limits_for_all_after_high(0, int_additional_step_to_add_above_one)
            self.high_density_limit_count = self.terrible_density_limit_count + 1

    def set_density_limits_for_all_after_high(self, start_limit, int_additional_stepping):
        self.warn_density_limit_count = start_limit + 1 + int_additional_stepping
        self.bad_density_limit_count = self.warn_density_limit_count + 1 + int_additional_stepping
        self.terrible_density_limit_count = self.bad_density_limit_count + 1 + int_additional_stepping

    def add_density_limit(self, bad_density_limit_count, pen_colour, pen_width, int_level_of_search):
        self.density_limits.append([bad_density_limit_count, pen_colour, pen_width, int_level_of_search])

    @property
    def number_of_density_limits(self):
        return len(self.density_limits)

    @property
    def number_counted_within_limit(self):
        return self.number_counted_within_limit

    @number_counted_within_limit.setter
    def number_counted_within_limit(self, value):
        self.number_counted_within_limit = value

    def increase_number_within_limit(self):
        self.number_counted_within_limit += 1
        self.mark_needle_within_limit_as_found()

    def reset_for_next_point_check(self, pen_info):
        self.reset_count_of_same_points()
        self.number_counted_within_limit = 0
        self.found_needle_within_limit = False
        self.pen_info = pen_info

    @property
    def found_needle_within_limit(self):
        return self.found_needle_within_limit

    @found_needle_within_limit.setter
    def found_needle_within_limit(self, value):
        self.found_needle_within_limit = value

    def mark_needle_within_limit_as_found(self):
        self.found_needle_within_limit = True

    def add_point_if_within_limit(self, this_distance):
        if this_distance <= self.density_area_radius_mm:
            if (this_distance == 0) and self.possible_same_point():
                self.increase_possibly_seen_same_points()
            else:
                self.increase_number_within_limit()
        return self.found_needle_within_limit

    def count_points_in_density_radius(self, current_x, current_y, np_possibly_close):
        for possibly_close in np_possibly_close:
            this_distance = numpy.linalg.norm(possibly_close - [current_x, current_y])
            self.add_point_if_within_limit(this_distance)
        return self.found_needle_within_limit

    def translate_count_to_density_colour(self):
        for density_limit_index in xrange(len(self.density_limits)):
            if self.number_counted_within_limit >= self.density_limits[density_limit_index][0]:
                self.pen_info.update(self.density_limits[density_limit_index][1],
                                     self.density_limits[density_limit_index][2])
                break
