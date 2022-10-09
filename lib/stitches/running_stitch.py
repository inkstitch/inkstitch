# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
import random
from copy import copy

from shapely.geometry import LineString

""" Utility functions to produce running stitches. """


def running_stitch(points, stitch_length, tolerance,length_decrease=0,length_increase=0):
    """Generate running stitch along a path.

    Given a path and a stitch length, walk along the path in increments of the
    stitch length.  If sharp corners are encountered, an extra stitch will be
    added at the corner to avoid rounding the corner.  The starting and ending
    point are always stitched.

    The path is described by a set of line segments, each connected to the next.
    The line segments are described by a sequence of points.
    """

    if len(points) < 2:
        return []
    
    ## no stitch_length randomness required
    if not length_decrease and not length_increase:
        # simplify will remove as many points as possible while ensuring that the
        # resulting path stays within the specified tolerance of the original path.
        path = LineString(points)
        simplified = path.simplify(tolerance, preserve_topology=False)

        # save the points that simplify picked and make sure we stitch them
        important_points = set(simplified.coords)
        important_point_indices = [i for i, point in enumerate(points) if point.as_tuple() in important_points]

        output = []
        for start, end in zip(important_point_indices[:-1], important_point_indices[1:]):
            # consider sections of the original path, each one starting and ending
            # with an important point
            section = points[start:end + 1]
            if not output or output[-1] != section[0]:
                output.append(section[0])

            # Now split each section up evenly into stitches, each with a length no
            # greater than the specified stitch_length.
            section_ls = LineString(section)
            section_length = section_ls.length
            if section_length > stitch_length:
                # a fractional stitch needs to be rounded up, which will make all
                # the stitches shorter
                num_stitches = math.ceil(section_length / stitch_length)
                actual_stitch_length = section_length / num_stitches

                distance = actual_stitch_length
                
                segment_start = section[0]
                for segment_end in section[1:]:
                    segment = segment_end - segment_start
                    segment_length = segment.length()

                    if distance < segment_length:
                        segment_direction = segment.unit()

                        while distance < segment_length:
                            output.append(segment_start + distance * segment_direction)
                            distance += actual_stitch_length

                    distance -= segment_length
                    segment_start = segment_end

        if points[-1] != output[-1]:
            output.append(points[-1])

        return output
    else: # add randomness to the stitch length
        path = LineString(points)
        simplified = path.simplify(tolerance, preserve_topology=False)

        # save the points that simplify picked and make sure we stitch them
        important_points = set(simplified.coords)
        important_point_indices = [i for i, point in enumerate(points) if point.as_tuple() in important_points]

        output = []
        for start, end in zip(important_point_indices[:-1], important_point_indices[1:]):
            # consider sections of the original path, each one starting and ending
            # with an important point
            section = points[start:end + 1]
            if not output or output[-1] != section[0]:
                if (section[1]-section[0]).length()>0.5:
                    length_perturbation=random.uniform(-length_decrease/100,length_increase/100)
                    segment_direction=(section[1]-section[0]).unit()
                    output.append(section[0]+stitch_length*(length_perturbation)*segment_direction)
                else:
                    output.append(section[0])

            # Now split each section up evenly into stitches, each with a length no
            # greater than the specified stitch_length.
            section_ls = LineString(section)
            section_length = section_ls.length
            if section_length > stitch_length:
                distance = stitch_length
                
                segment_start = section[0]
                
                length_perturbation=random.uniform(-length_decrease/100,length_increase/100)
                segment_direction=(section[1]-section[0]).unit()
                segment_start+=stitch_length*(length_perturbation)*segment_direction
                for segment_end in section[1:]:
                    segment = segment_end - output[-1]
                    segment_length = segment.length()

                    if distance < segment_length:
                        segment_direction = segment.unit()
                        while distance < segment_length:
                            output.append(segment_start + distance * segment_direction)
                            length_perturbation=random.uniform(-length_decrease/100,length_increase/100)
                            distance += stitch_length*(1+length_perturbation)

                    #distance = stitch_length
                    distance -= segment_length
                    
                    segment_start = output[-1]
                   
        if points[-1] != output[-1]:
            output.append(points[-1])

        return output


def bean_stitch(stitches, repeats):
    """Generate bean stitch from a set of stitches.

    "Bean" stitch is made by backtracking each stitch to make it heaver.  A
    simple bean stitch would be two stitches forward, one stitch back, two
    stitches forward, etc.  This would result in each stitch being tripled.

    We'll say that the above counts as 1 repeat.  Backtracking each stitch
    repeatedly will result in a heavier bean stitch.  There will always be
    an odd number of threads piled up for each stitch.
    """

    if len(stitches) < 2:
        return stitches

    new_stitches = [stitches[0]]

    for stitch in stitches:
        new_stitches.append(stitch)

        for i in range(repeats):
            new_stitches.extend(copy(new_stitches[-2:]))

    return new_stitches
