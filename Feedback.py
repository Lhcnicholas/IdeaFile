# author: Peter Okma
import xml.etree.ElementTree as et


class Feedback:
    """Feedback used by Alfred Script Filter

    Usage:
        fb = Feedback()
        fb.add_item('Hello', 'World')
        fb.add_item('Foo', 'Bar')
        print(fb)

    """

    def __init__(self):
        self.feedback = et.Element('items')

    def __repr__(self):
        """XML representation used by Alfred

        Returns:
            XML string
        """
        return et.tostring(self.feedback).decode('utf-8')

    def add_item(self, title, subtitle="", arg="", valid="yes", autocomplete="", icon="icon.png"):
        """
        Add item to alfred Feedback

        Args:
            @param title: the title displayed by Alfred
        Keyword Args:
            @param subtitle:     the subtitle displayed by Alfred
            @param arg:          the value returned by alfred when item is selected
            @param valid:        whether the entry can be selected in Alfred to trigger an action
            @param autocomplete: the text to be inserted if an invalid item is selected.
                                 This is only used if 'valid' is 'no'
            @param icon:         filename of icon that Alfred will display
        """
        item = et.SubElement(self.feedback, 'item', uid=str(len(self.feedback)),
                             arg=arg, valid=valid, autocomplete=autocomplete)
        _title = et.SubElement(item, 'title')
        _title.text = title
        _sub = et.SubElement(item, 'subtitle')
        _sub.text = subtitle
        _icon = et.SubElement(item, 'icon')
        _icon.text = icon

    def isEmpty(self):
        """
        判断是否为空
        @return:
        """
        if len(self.feedback.findall(path="./")) == 0:
            return True
        else:
            return False
