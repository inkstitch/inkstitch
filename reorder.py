#!/usr/bin/python
#
# Remove selected objects from the document and readd them in the order they
# were selected.

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
import inkex


class Reorder(inkex.Effect):

    def get_selected_in_order(self):
        selected = []

        for i in self.options.ids:
            path = '//*[@id="%s"]' % i
            for node in self.document.xpath(path, namespaces=inkex.NSS):
                selected.append(node)

        return selected

    def effect(self):
        objects = self.get_selected_in_order()

        for obj in objects[1:]:
            obj.getparent().remove(obj)

        insert_parent = objects[0].getparent()
        insert_pos = insert_parent.index(objects[0])

        insert_parent.remove(objects[0])

        insert_parent[insert_pos:insert_pos] = objects

if __name__ == '__main__':
    e = Reorder()
    e.affect()
