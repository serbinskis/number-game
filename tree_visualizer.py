import copy
import random
from tkinter import *
from typing import List, Optional, Callable, Sequence, cast
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk, ImageFont

class Picaso:
  def draw_rectangle(self: ImageDraw, coords, fill_ink, num, dotted):
    if dotted:
      Picaso.draw_dotted_rectangle(self, coords, fill_ink)
    else:
      self.draw.draw_rectangle(coords, fill_ink, num)
     

  def draw_dotted_rectangle(self: ImageDraw, coords, fill_ink):
    # Create the dotted line effect using multiple short lines
    x0, y0, x1, y1 = coords
    step = 5  # Length of each dot or segment
    gap = 5   # Space between dots

    # Draw top side of the rectangle
    for i in range(x0, x1, step + gap):
        self.line((i, y0, min(i + step, x1), y0), fill=fill_ink)

    # Draw bottom side of the rectangle
    for i in range(x0, x1, step + gap):
        self.line((i, y1, min(i + step, x1), y1), fill=fill_ink)

    # Draw left side of the rectangle
    for i in range(y0, y1, step + gap):
        self.line((x0, i, x0, min(i + step, y1)), fill=fill_ink)

    # Draw right side of the rectangle
    for i in range(y0, y1, step + gap):
        self.line((x1, i, x1, min(i + step, y1)), fill=fill_ink)

  def rounded_rectangle(
          self: ImageDraw,
          xy: any, # type: ignore
          radius: float = 0,
          fill: any = None, # type: ignore
          outline: any = None, # type: ignore
          dotted: bool = False,
          width: int = 1,
          *,
          corners: tuple[bool, bool, bool, bool] | None = None,
      ) -> None:
          """Draw a rounded rectangle."""
          if isinstance(xy[0], (list, tuple)):
              (x0, y0), (x1, y1) = cast(Sequence[Sequence[float]], xy)
          else:
              x0, y0, x1, y1 = cast(Sequence[float], xy)
          if x1 < x0:
              msg = "x1 must be greater than or equal to x0"
              raise ValueError(msg)
          if y1 < y0:
              msg = "y1 must be greater than or equal to y0"
              raise ValueError(msg)
          if corners is None:
              corners = (True, True, True, True)

          d = radius * 2

          x0 = round(x0)
          y0 = round(y0)
          x1 = round(x1)
          y1 = round(y1)
          full_x, full_y = False, False
          if all(corners):
              full_x = d >= x1 - x0 - 1
              if full_x:
                  # The two left and two right corners are joined
                  d = x1 - x0
              full_y = d >= y1 - y0 - 1
              if full_y:
                  # The two top and two bottom corners are joined
                  d = y1 - y0
              if full_x and full_y:
                  # If all corners are joined, that is a circle
                  return self.ellipse(xy, fill, outline, width)

          if d == 0 or not any(corners):
              # If the corners have no curve,
              # or there are no corners,
              # that is a rectangle
              return self.rectangle(xy, fill, outline, width)

          r = int(d // 2)
          ink, fill_ink = self._getink(outline, fill)

          def draw_corners(pieslice: bool) -> None:
              parts: tuple[tuple[tuple[float, float, float, float], int, int], ...]
              if full_x:
                  # Draw top and bottom halves
                  parts = (
                      ((x0, y0, x0 + d, y0 + d), 180, 360),
                      ((x0, y1 - d, x0 + d, y1), 0, 180),
                  )
              elif full_y:
                  # Draw left and right halves
                  parts = (
                      ((x0, y0, x0 + d, y0 + d), 90, 270),
                      ((x1 - d, y0, x1, y0 + d), 270, 90),
                  )
              else:
                  # Draw four separate corners
                  parts = tuple(
                      part
                      for i, part in enumerate(
                          (
                              ((x0, y0, x0 + d, y0 + d), 180, 270),
                              ((x1 - d, y0, x1, y0 + d), 270, 360),
                              ((x1 - d, y1 - d, x1, y1), 0, 90),
                              ((x0, y1 - d, x0 + d, y1), 90, 180),
                          )
                      )
                      if corners[i]
                  )
              for part in parts:
                  if pieslice:
                      self.draw.draw_pieslice(*(part + (fill_ink, 1)))
                  else:
                      self.draw.draw_arc(*(part + (ink, width)))

          if fill_ink is not None:
              draw_corners(True)

              if full_x:
                  Picaso.draw_rectangle(self, (x0, y0 + r + 1, x1, y1 - r - 1), fill_ink, 1, False)
              elif x1 - r - 1 > x0 + r + 1:
                  Picaso.draw_rectangle(self, (x0 + r + 1, y0, x1 - r - 1, y1), fill_ink, 1, False)
              if not full_x and not full_y:
                  left = [x0, y0, x0 + r, y1]
                  if corners[0]:
                      left[1] += r + 1
                  if corners[3]:
                      left[3] -= r + 1
                  Picaso.draw_rectangle(self, left, fill_ink, 1, False)

                  right = [x1 - r, y0, x1, y1]
                  if corners[1]:
                      right[1] += r + 1
                  if corners[2]:
                      right[3] -= r + 1
                  Picaso.draw_rectangle(self, right, fill_ink, 1, False)
          if ink is not None and ink != fill_ink and width != 0:
              draw_corners(False)

              if not full_x:
                  top = [x0, y0, x1, y0 + width - 1]
                  if corners[0]:
                      top[0] += r + 1
                  if corners[1]:
                      top[2] -= r + 1
                  Picaso.draw_rectangle(self, top, ink, 1, dotted)

                  bottom = [x0, y1 - width + 1, x1, y1]
                  if corners[3]:
                      bottom[0] += r + 1
                  if corners[2]:
                      bottom[2] -= r + 1
                  Picaso.draw_rectangle(self, bottom, ink, 1, dotted)
              if not full_y:
                  left = [x0, y0, x0 + width - 1, y1]
                  if corners[0]:
                      left[1] += r + 1
                  if corners[3]:
                      left[3] -= r + 1
                  Picaso.draw_rectangle(self, left, ink, 1, dotted)

                  right = [x1 - width + 1, y0, x1, y1]
                  if corners[1]:
                      right[1] += r + 1
                  if corners[2]:
                      right[3] -= r + 1
                  Picaso.draw_rectangle(self, right, ink, 1, dotted)



class TreeNode:
  _shared_font = font = ImageFont.truetype("arial.ttf", 10)
  _shared_marging_height = 20 #Marging between nodes, for drawing
  _shared_marging_width = 15 #Marging between nodes, for drawing

  def __init__(self, text: str, parent: Optional["TreeNode"] = None):
    self.text: str = text
    self.parent: Optional["TreeNode"] = parent
    self.children: List["TreeNode"] = []
    self.next_sibling: Optional["TreeNode"] = None  # Next node at the same depth
    self.prev_sibling: Optional["TreeNode"] = None  # Previous node at the same depth
    self.siblings_count: int = 1 # Count how many siblings incluing ourself
    self.width: int = -1  # To be calculated based on text width
    self.total_width: int = -1 # Total width of all siblings texts + gaps
    self.height: int = -1  # To be calculated based on text height
    self.outline_color = f"#{random.randint(0, 0xFFFFFF):06x}"
    self.fill_color = "#ffffff"
    self.selected = False # Should we highlight node
    self.__update_dimensions() # Update width and height
    self.max_height: int = self.height # Max text height for this depth
    self.position: List[int] = [0, (self.height // 2) + self._shared_marging_height]  # (x, y) based on depth and order
    self.depth: int = 0 if parent is None else parent.depth + 1  # Node depth
    self.image = None

  def add_children(self, child_node: "TreeNode"):
    if (child_node.parent == None): child_node.parent = self
    self.image = None
    child_node.depth = self.depth + 1
    self.children.append(child_node)
    child_node.__update_siblings()
    child_node.__update_siblings_count()
    child_node.__update_position()
  
  def is_leaf(self):
    return len(self.children) == 0

  def get_count(self) -> int:
    """Recursively count all nodes in the subtree, including this node."""
    return 1 + sum(child.get_count() for child in self.children)

  def get_fill_color(self):
    if self.is_selected(): return "#ffcc00"
    return self.fill_color

  def is_selected(self):
    return self.selected

  def set_selected(self, selected):
    self.selected = selected

  def draw_link(self, canvas: Canvas, parent: "TreeNode", x: int, y: int):
    y0 = parent.position[1] + (parent.max_height // 2) + y # Calculate the coordinates for the start point
    x0 = parent.position[0] + x
    y1 = self.position[1] - (self.max_height // 2) + y # Calculate the coordinates for the end point
    x1 = self.position[0] + x

    # Check if both positions are outside the canvas boundaries
    if (x0 < 0 or x0 > canvas.winfo_reqwidth() or y0 < 0 or y0 > canvas.winfo_reqheight()) and \
       (x1 < 0 or x1 > canvas.winfo_reqwidth() or y1 < 0 or y1 > canvas.winfo_reqheight()): return

    outline = self.outline_color if not self.parent else self.parent.outline_color
    canvas.create_line(x0, y0, x1, y1, fill=outline, width=2)

  def draw_on_position(self, canvas: Canvas, x: int, y: int):
    if (self.width == -1 or self.height == -1): self.__update_dimensions()
    if (x + self.width < 0 or x > canvas.winfo_reqwidth() or y + self.height < 0 or y > canvas.winfo_reqheight()): return
    if (not self.image):
      outline = "black" if not self.parent else self.parent.outline_color
      self.pil_image = Image.new('RGB', (self.width, self.height), "white")
      self.image_draw = ImageDraw.Draw(self.pil_image)
      Picaso.rounded_rectangle(self.image_draw, [(0, 0), (self.width - 1, self.height - 1)], outline=outline, width=2, radius=10, fill=self.get_fill_color(), dotted=self.is_leaf())
      self.image_draw.text((10, 10), self.text, font=self._shared_font, fill="black")
      self.image = ImageTk.PhotoImage(self.pil_image)
    canvas.create_image(x, y, image=self.image, anchor="nw")
  
  def draw_relatively(self, canvas: Canvas, x: int, y: int):
    self.draw_on_position(canvas, self.position[0] - (self.width // 2) + x, self.position[1] - (self.height // 2) + y)
    if (self.parent): self.draw_link(canvas, self.parent, x, y)

  def __update_siblings(self):
    if (self.parent == None): return # Root cannot have siblings

    # https://prnt.sc/F2tMDN83T5Cs #New node is always added at the end of the list
    if (len(self.parent.children)-1 > 0):
      self.__assign_siblings(self.parent.children[-2], "prev_sibling")

    # https://prnt.sc/41AIQX4O3v4M
    # We either found parent with children or there was no children, meaning that the node is first in this depth
    if ((self.prev_sibling == None) and (self.parent.prev_sibling != None)):
      parent_prev_sibling = self.__find_sibling_with_children(self.parent.prev_sibling, "prev_sibling")
      if (parent_prev_sibling != None) > 0: self.__assign_siblings(parent_prev_sibling.children[-1], "prev_sibling")

    # https://prnt.sc/FX3H9m-x9l6u
    if ((self.next_sibling == None) and (self.parent.next_sibling != None)):
      parent_next_sibling = self.__find_sibling_with_children(self.parent.next_sibling, "next_sibling")
      if (parent_next_sibling != None): self.__assign_siblings(parent_next_sibling.children[0], "next_sibling")

  def __find_sibling_with_children(self, parent: "TreeNode", direction: str) -> Optional["TreeNode"]:
    while (parent and not parent.children): parent = getattr(parent, direction, None)
    return parent if (parent and parent.children) else None

  def __assign_siblings(self,  sibling: "TreeNode", direction: str) -> "TreeNode":
    setattr(self, direction, sibling)
    setattr(sibling, ("prev_sibling" if direction == "next_sibling" else "next_sibling"), self)

  def __update_siblings_count(self):
    # Update our siblings_count from sibling, if no siblings found then default count to 1
    ref_sibling = self.prev_sibling or self.next_sibling
    self.siblings_count = (ref_sibling.siblings_count + 1) if ref_sibling else 1
    self.__execute_on_siblings(lambda node: setattr(node, 'siblings_count', self.siblings_count))

# https://prnt.sc/uitUZvEqKlqt
  def __update_dimensions(self):
    lines = self.text.split("\n")
    self.height += 20

    for line in lines:
      bbox = self._shared_font.getbbox(line)
      self.width = max(self.width, bbox[2] - bbox[0] + 20)
      self.height += (bbox[3] - bbox[1] + 5)

  def __update_position(self):
    self.total_width = self.width + ((self.siblings_count-1) * self._shared_marging_width) # Add ourself width and width for gaps between siblings
    self.total_width = self.__acumulate_on_siblings(self.total_width, lambda acumulator, node: acumulator + node.width) # Sum all other sibling's width
    self.max_height = self.__acumulate_on_siblings(self.height, lambda acumulator, node: max(acumulator, node.height))
    self.__execute_on_siblings(lambda node: setattr(node, 'total_width', self.total_width)) # Set other sibling's total_width
    self.__execute_on_siblings(lambda node: setattr(node, 'max_height', self.max_height)) # Set other sibling's max_height

    position_y = self.parent.position[1] + (self.parent.max_height // 2) + (self._shared_marging_height) + (self.max_height // 2) # All nodes on same depth share same y position, which is center of max_height
    sibling = self.__get_first_sibling()
    sibling.position[0] = (self.width // 2) - (self.total_width // 2)

    while (sibling):
       sibling.position[1] = position_y
       if sibling.prev_sibling: sibling.position[0] = sibling.prev_sibling.position[0] + (sibling.prev_sibling.width // 2) + self._shared_marging_width + (sibling.width // 2)
       if (sibling.prev_sibling and (sibling.prev_sibling.parent != sibling.parent)): sibling.position[0] += self._shared_marging_width * 2
       sibling = sibling.next_sibling

  def __execute_on_siblings(self, callback: Callable[["TreeNode"], None] = None):
    # Update all siglings to left with callback
    prev_node = self.prev_sibling
    while prev_node:
        callback(prev_node)
        prev_node = prev_node.prev_sibling

    # Update all siglings to right with callback
    next_node = self.next_sibling
    while next_node:
        callback(next_node)
        next_node = next_node.next_sibling

  def __acumulate_on_siblings(self, acumulator: int, callback: Callable[[int, "TreeNode"], None] = None) -> int:
     _acumulator = { 'value': acumulator }
     self.__execute_on_siblings(lambda node: _acumulator.update({'value': callback(_acumulator['value'], node)}))
     return _acumulator['value']

  def __get_first_sibling(self):
      prev_node = self
      while prev_node.prev_sibling: prev_node = prev_node.prev_sibling
      return prev_node
     

class TreeVizualizer:
  def __init__(self, root: "TreeNode"):
    self.root = root
    self.selected_node = root
    self.current_center = copy.deepcopy(root.position)
    self.target_center = self.current_center

  def render(self, canvas: Canvas):
    self.current_center[0] = self.current_center[0] + (self.target_center[0] - self.current_center[0]) * 0.2
    self.current_center[1] = self.current_center[1] + (self.target_center[1] - self.current_center[1]) * 0.2
    self.draw_selected(canvas)

  def get_count(self) -> int:
    return self.root.get_count()

  def print_tree(self, node: Optional["TreeNode"] = None, prefix: str = "", is_last: bool = True):
      """Prints the tree structure in a formatted way."""
      if node is None: node = self.root
      connector = "└── " if is_last else "├── "
      print(prefix + connector + f"'{node.text}'")
      prefix += "    " if is_last else "│   "
      
      for i, child in enumerate(node.children):
          is_last_child = (i == len(node.children) - 1)
          self.print_tree(child, prefix, is_last_child)

  def execute_on_depth(self, depth: int = -1, callback: Optional[Callable[["TreeNode"], None]] = None):
      node = self.find_first_node_at_depth(depth=depth, node=self.root)
      if (node is None): return
      while node.prev_sibling: node = node.prev_sibling

      while (callback and node):
        callback(node)
        node = node.next_sibling

  def find_max_depth(self, node: Optional["TreeNode"] = None, current_max: int = 0) -> int:
      if node is None: node = self.root
      if not node.children: return max(current_max, node.depth)
      return max([self.find_max_depth(child, current_max) for child in node.children])

  def find_first_node_at_depth(self, depth: int = -1, node: Optional["TreeNode"] = None) -> Optional["TreeNode"]:
      if node is None: node = self.root
      if depth == -1: depth = self.find_max_depth(self.root)
      if node.depth == depth: return node
      
      for child in node.children:
          found_node = self.find_first_node_at_depth(depth, child)
          if found_node: return found_node

  def draw(self, node: Optional["TreeNode"], canvas: Canvas):
    canvas_center_x = canvas.winfo_reqwidth() // 2
    canvas_center_y = canvas.winfo_reqheight() // 2
    x_offset = canvas_center_x - self.current_center[0]
    y_offset = canvas_center_y - self.current_center[1]
    node.draw_relatively(canvas, x_offset, y_offset)

  def draw_depth(self, canvas: Canvas, depth: int = -1, depths: list = None):
    if (depth > -1): self.execute_on_depth(depth, lambda node: self.draw(node, canvas))
    if (depth < 0 and (depths is None)): depths = [i for i in range(self.find_max_depth() + 1)]
    for depth in depths: self.execute_on_depth(depth, lambda node: self.draw(node, canvas))

  def draw_selected(self, canvas: Canvas, depth: int = -1, depths: list = None):
     self.selected_node.set_selected(True)
     self.draw_depth(canvas, depth=depth, depths=depths)
     self.selected_node.set_selected(False)

  def set_selected(self, node: "TreeNode"):
     self.selected_node.image = None
     self.selected_node = node
     self.selected_node.image = None
     self.set_center(node)

  def set_center(self, node: "TreeNode"):
     self.current_center = self.target_center
     self.target_center = copy.deepcopy(node.position)

  def move_selected(self, direction: str):
      if direction == "Up" and self.selected_node.parent:
          self.set_selected(self.selected_node.parent)
      elif direction == "Down" and self.selected_node.children:
          self.set_selected(self.selected_node.children[len(self.selected_node.children) // 2])  # Move to first child
      elif direction == "Left" and self.selected_node.prev_sibling:
          self.set_selected(self.selected_node.prev_sibling)
      elif direction == "Left" and self.selected_node.children:
          self.set_selected(self.selected_node.children[0])
      elif direction == "Right" and self.selected_node.next_sibling:
          self.set_selected(self.selected_node.next_sibling)
      elif direction == "Right" and self.selected_node.children:
          self.set_selected(self.selected_node.children[-1])