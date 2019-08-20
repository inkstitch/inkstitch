from .stitch import END, NO_COMMAND, TRIM, JUMP


class PointLists:
    def __init__(self, color_block=None):
        self.point_lists = [[]]
        if color_block is not None:
            self.color_block_to_point_lists(color_block)

    @property
    def num_point_lists(self):
        return len(self.point_lists)

    @property
    def previous_point_list(self):
        if self.point_lists and self.num_point_lists >= 2:
            return self.point_lists[-2]
        else:
            return None

    @property
    def current_point_list(self):
        if self.point_lists and self.num_point_lists >= 1:
            return self.point_lists[-1]
        else:
            return None

    def point_list_at_index(self, int_index):
        if self.point_lists and self.num_point_lists >= int_index:
            return self.point_lists[int_index]
        else:
            return None

    def delete_point_list_at_index(self, int_index):
        if self.point_lists and self.num_point_lists >= int_index:
            del self.point_lists[int_index]
        else:
            raise ValueError("internal error: can't remove a non existing point list")

    def __iter__(self):
        return iter(self.point_lists)

    def __len__(self):
        return len(self.point_lists)

    def __repr__(self):
        return "PointList(%s)" % ", ".join(repr(cb) for cb in self.point_lists)

    def add_point_list(self):
        if self.point_lists[-1]:
            self.point_lists.append([])

    def color_block_to_point_lists(self, color_block):
        self.point_lists = [[]]
        previous_command = NO_COMMAND
        pre_previous_command = NO_COMMAND
        for stitch in color_block:
            command = stitch.command_at_point
            if command == END:
                self.current_point_list.append(stitch.as_tuple())
                self.add_point_list()
            elif command == JUMP and previous_command == END:
                self.current_point_list.append(stitch.as_tuple())
            elif command == TRIM and pre_previous_command == END and previous_command == JUMP:
                self.current_point_list.append(stitch.as_tuple())
            elif stitch.trim:
                if self.point_lists[-1]:
                    self.point_lists.append([])
                    continue
            if not stitch.jump and not stitch.color_change and not stitch.end:
                self.current_point_list.append(stitch.as_tuple())
            pre_previous_command = previous_command
            previous_command = command

        # filter out empty point lists
        self.point_lists = [p for p in self.point_lists if p]

        return self.point_lists
