class BaseController:
    def __init__(self, view_class):
        self.view = view_class(self)

    def _show_view(self):
        self.view.show()

    def _handle_button_click(self, button_text):
        pass
    
    def _get_input_data(self):
        label_input_pairs = self.view._label_input_map
        for input_label, input_field in label_input_pairs.items():
            label_value = input_label.text()
            input_value = input_field.text()
            print(f"{label_value}: {input_value}")