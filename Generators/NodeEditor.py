import dearpygui.dearpygui as dpg


class NodeEditor:
    def __init__(self):
        self.node_list = {}

        with dpg.node_editor(callback=self.link_callback, delink_callback=self.delink_callback, tag='editor'):
            with dpg.node(label='Texture Image', pos=(100, 150)):
                with dpg.node_attribute(attribute_type=2):
                    dpg.add_image("texture_tag", width=40, height=40)
                with dpg.node_attribute(attribute_type=1, tag='Image Color', shape=1):
                    dpg.add_text('Color')
                with dpg.node_attribute(attribute_type=1):
                    dpg.add_text('Alpha')

            with dpg.node(label='OutPut', pos=(300, 150)):
                with dpg.node_attribute(tag='Output Color', shape=dpg.mvNode_PinShape_Circle):
                    dpg.add_text('Color')

    def link_callback(self, sender, app_data):
        # app_data -> (link_id1, link_id2)
        if app_data[1] in self.node_list.keys():
            dpg.delete_item(self.node_list[app_data[1]])

        self.node_list[app_data[1]] = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    # callback runs when user attempts to disconnect attributes

    def delink_callback(self, sender, app_data):
        # app_data -> link_id
        if app_data in self.node_list.values():
            list_node = list(self.node_list.values())
            for i in range(len(list_node)):
                if list_node[i] == app_data:
                    del self.node_list[list(self.node_list.keys())[i]]
        dpg.delete_item(app_data)



