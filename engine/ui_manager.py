# engine/ui_manager.py

import pygame
from engine.base_manager import BaseManager
from engine.ui_button import UIButton
from engine.ui_element import UIElement
from engine.ui_label import UILabel

class UIManager(BaseManager):
    """
    Manage interface elements, focus and input routing.

    Constants:
        DEFAULT_LAYER (str): Default layer name.
        LAYER_ORDER (list[str]): Default order for layers (background -> UI -> overlay).

    Attributes:
        UI Attributes:
            elements (dict[str, UIElement]): Registered UI elements by name.
            layers (dict[str, list[str]]): Mapping layer -> ordered list of element names.
            layer_order (list[str]): Ordered list of layers (render/update order).
            focus_name (str|None): Name of the currently focused element.
            persisted_config (dict): Raw UI config loaded from app_config (if any).

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        Element management:
            create_element(name, element_type, layer='default', **kwargs)
            remove_element(name)
            get_element(name)
            set_layer_order(list_of_layers)

        Focus & navigation:
            focus(name|None)
            focus_next()
            focus_prev()
            activate_focused()

        Input:
            handle_event(event): route pygame events (mouse/keyboard) to UI
            update(dt): update elements (and maintain focus behaviour)
            render(surface): draw elements in layer order

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    # Defaults
    DEFAULT_LAYER = "ui"
    LAYER_ORDER = ["background", "ui", "overlay"]

    # Element type registry (string -> class)
    ELEMENT_TYPES = {
        "UIElement": UIElement,
        "UILabel": UILabel,
        "UIButton": UIButton,
    }

    def __init__(self, core_manager=None, app_config=None):
        # UI Attributes
        self.elements = {}               # name -> element instance
        self.layers = {}                 # layer -> [element_name,...]
        self.layer_order = list(self.LAYER_ORDER)  # default order; configurable
        self.focus_name = None
        self.persisted_config = {}

        # Initialize BaseManager and components
        super().__init__(core_manager, app_config)

    """
    Configuration
        _setup
        load_config
    """
    def _setup(self):
        """
        Initialize components and refresh refs.
        """
        # Refresh manager refs so elements can access other managers safely.
        self.update_manager_refs()

        # Load manager config (elements/layers)
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration.

        Expected config keys:
            elements: dict of element_name -> element_cfg
            layer_order: optional list of layer names (overrides default order)
        """
        if not config:
            return

        # Allow overriding layer order
        if "layer_order" in config:
            order = config["layer_order"]
            if isinstance(order, list):
                self.set_layer_order(order)

        # Create elements declared in config
        elements_cfg = config.get("elements", {})
        for name, element_cfg in elements_cfg.items():
            # Accept element_cfg as dict; allow type aliasing
            elem_type = element_cfg.get("type", "UIElement")
            layer = element_cfg.get("layer", self.DEFAULT_LAYER)
            # Remove keys that will be passed to constructor automatically
            cfg = dict(element_cfg)
            cfg.pop("type", None)
            cfg.pop("layer", None)
            self.create_element(name, elem_type, layer=layer, **cfg)

        # Save persisted config for potential future use
        self.persisted_config = config

    """
    Element management
        create_element
        remove_element
        get_element
        set_layer_order
    """
    def create_element(self, name: str, element_type: str, layer: str = None, **kwargs):
        """
        Create and register a new UI element.

        Args:
            name (str): Identifier for the element.
            element_type (str): One of keys in ELEMENT_TYPES (e.g., "UIButton").
            layer (str): Layer name where element belongs (render/update order).
            **kwargs: forwarded to element constructor.

        Returns:
            UIElement: The created element instance.
        """
        # Resolve defaults
        if layer is None:
            layer = self.DEFAULT_LAYER

        # Choose element class
        element_class = self.ELEMENT_TYPES.get(element_type, UIElement)

        # Instantiate element (ensure name is passed)
        element = element_class(name=name, **kwargs)

        # Register element
        self.elements[name] = element

        # Ensure layer exists
        if layer not in self.layers:
            self.layers[layer] = []
            # If new layer not in order, append at end
            if layer not in self.layer_order:
                self.layer_order.append(layer)

        # Insert at end of layer (stack order; later items draw on top)
        self.layers[layer].append(name)

        # If element is focusable and no focus yet, set initial focus
        if getattr(element, "focusable", False) and self.focus_name is None:
            self.focus(name)

        return element

    def remove_element(self, name: str):
        """
        Remove a registered element by name.

        Args:
            name (str): Element identifier.
        """
        el = self.elements.pop(name, None)
        if not el:
            return

        # Remove from layers
        for layer, names in list(self.layers.items()):
            if name in names:
                names.remove(name)
                if not names:
                    # Optionally keep empty layers; we do not delete to keep ordering stable
                    pass

        # Clear focus if needed
        if self.focus_name == name:
            self.focus(None)

        # If element has a cleanup hook, call it
        if hasattr(el, "destroy"):
            try:
                el.destroy()
            except Exception:
                pass

    def get_element(self, name: str):
        """Return element instance by name or None."""
        return self.elements.get(name)

    def set_layer_order(self, order_list):
        """
        Replace layer order.

        Args:
            order_list (list[str]): New layer order; layers not present are appended.
        """
        self.layer_order = list(order_list)
        # Ensure existing layers are included
        for l in list(self.layers.keys()):
            if l not in self.layer_order:
                self.layer_order.append(l)

    """
    Focus Management
        focus
        _focusable_names_in_order
        focus_first
        focus_last
        focus_next
        focus_prev
        activate_focused
    """
    def focus(self, name):
        """
        Set focus to a specific element by name.
        """
        # Fetch previously focused element
        previous_name = self.focus_name
        if previous_name and previous_name in self.elements:
            previous_element = self.elements[previous_name]

            # Update focus state of the previous element
            if hasattr(previous_element, "set_focus"):
                previous_element.set_focus(False)

        # Clear focus if None is passed
        if name is None:
            self.focus_name = None
            return

        # Early return if not applicable
        if name not in self.elements:
            return

        # Set focus to the new element
        new_element = self.elements[name]
        self.focus_name = name

        # Call 'on_focus' hook if available
        if hasattr(new_element, "on_focus"):
            new_element.on_focus()

        # Update focus state of the new element
        if hasattr(new_element, "set_focus"):
            new_element.set_focus(True)

    def _focusable_names_in_order(self):
        """
        Return a list of element names that can receive focus in visual order.
        """
        names = []

        # Iterate through layers in visual order
        for layer in self.layer_order:
            # Iterate through element names in this layer
            for name in self.layers.get(layer, []):
                element = self.elements.get(name)

                # Element must exist and be marked focusable
                if element and getattr(element, "focusable", False):
                    # Skip invisible or disabled elements
                    if not getattr(element, "visible", True):
                        continue
                    if getattr(element, "disabled", False):
                        continue

                    # Append to ordered list
                    names.append(name)
        return names

    def focus_first(self):
        """
        Move focus to the first focusable element in visual order.
        """
        # Collect focusable element names in order
        names = self._focusable_names_in_order()

        # Early return if not applicable
        if not names:
            return

        # Skip invisible or disabled elements
        self.focus(names[0])

    def focus_last(self):
        """
        Move focus to the last focusable element in visual order.
        """
        # Collect focusable element names in order
        names = self._focusable_names_in_order()

        # Early return if not applicable
        if not names:
            return

        # Set focus to the last element
        self.focus(names[-1])

    def focus_next(self):
        """
        Move focus to the next focusable element in visual order.
        """
        # Collect focusable element names in order
        names = self._focusable_names_in_order()

        # Early return if not applicable
        if not names:
            return

        # If no element currently has focus, start with the first
        if self.focus_name not in names:
            self.focus_first()
            return

        # Advance focus to the next element
        idx = names.index(self.focus_name)
        self.focus(names[(idx + 1) % len(names)])

    def focus_prev(self):
        """
        Move focus to the previous focusable element in visual order.
        """
        # Collect focusable element names in order
        names = self._focusable_names_in_order()

        # Early return if not applicable
        if not names:
            return

        # If no element currently has focus, start with the last
        if self.focus_name not in names:
            self.focus_last()
            return

        # Advance focus to the previous element
        idx = names.index(self.focus_name)
        self.focus(names[(idx - 1) % len(names)])

    def activate_focused(self):
        """
        Trigger the currently focused element's callback function.
        """
        # Early return if not applicable
        if not self.focus_name:
            return

        # Fetch the focused element
        element = self.elements.get(self.focus_name)
        if not element:
            return

        # Call the element activation method
        callback = getattr(element, "callback", None)
        if callable(callback):
            callback()

    """
    Element Handling
        _topmost_element_at
        _handle_hover
        _handle_click
    """
    def _topmost_element_at(self, pos):
        """
        Return the topmost element under the given position.
        """
        # Iterate layers from topmost to bottom
        for layer in reversed(self.layer_order):
            # Iterate elements in layer from topmost to bottom
            for name in reversed(self.layers.get(layer, [])):
                element = self.elements.get(name)
                if not element:
                    continue

                # Skip invisible elements
                if getattr(element, "visible", True) is False:
                    continue

                # Check if cursor is over element
                hit = False
                if hasattr(element, "rect"):
                    hit = element.rect.collidepoint(pos)

                # Return first element hit
                if hit:
                    return element

        return None

    def _handle_hover(self, pos):
        """
        Process hover events for topmost element under cursor.
        """
        # Fetch topmost element
        element = self._topmost_element_at(pos)
        if not element:
            return

        # Call hover callback
        if hasattr(element, "on_hover"):
            element.on_hover(pos)

    def _handle_click(self, pos):
        """
        Process click events for topmost element under cursor.
        """
        # Fetch topmost element
        element = self._topmost_element_at(pos)
        if not element:
            return

        # Set focus if element is focusable
        if getattr(element, "focusable", False):
            self.focus(element.name)

        # Call click callback
        if hasattr(element, "on_click"):
            element.on_click(pos)

        # Call activate callback
        if hasattr(element, "on_activate"):
            element.on_activate()

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
        print(f"Layers: {self.layer_order}")
        for layer in self.layer_order:
            names = self.layers.get(layer, [])
            print(f"  {layer}: {names}")
        print(f"Focus: {self.focus_name}")
        print(f"Elements: {list(self.elements.keys())}")
        print()

    """
    Operations
        events
        update
        render
    """
    def events(self, event):
        """
        Process components events.
        """
        if event.type == pygame.MOUSEMOTION:
            self._handle_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def update(self, dt=None):
        """
        Update components.
        """
        # Update all elements in layer order
        for layer in self.layer_order:
            # Iterate through element names in this layer
            for name in list(self.layers.get(layer, [])):
                # Fetch element from registry
                element = self.elements.get(name)
                if not element:
                    continue

                # Update element
                element.update()

    def render(self, surface=None):
        """
        Render components.
        """
        # Render all elements in layer order
        for layer in self.layer_order:
            # Iterate through element names in this layer
            for name in list(self.layers.get(layer, [])):
                # Fetch element
                element = self.elements.get(name)
                if not element:
                    continue

                # Skip invisible element
                if hasattr(element, "visible") and not getattr(element, "visible"):
                    continue

                # Render element
                element.render(surface)
