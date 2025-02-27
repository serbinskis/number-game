from typing import List, Optional, Callable

class TreeNode:
  def __init__(self, text: str, parent: Optional["TreeNode"] = None):
    self.text: str = text
    self.parent: Optional["TreeNode"] = parent
    self.children: List["TreeNode"] = []
    self.next_sibling: Optional["TreeNode"] = None  # Next node at the same depth
    self.prev_sibling: Optional["TreeNode"] = None  # Previous node at the same depth
    self.siblings_count: int = 1 # Count how many siblings incluing ourself
    self.width: int = -1  # To be calculated based on text width
    self.height: int = -1  # To be calculated based on text height
    self.position: List[int] = [-1, -1]  # (x, y) based on depth and order
    self.depth: int = 0 if parent is None else parent.depth + 1  # Node depth

  def add_children(self, child_node: "TreeNode"):
    if (child_node.parent == None): child_node.parent = self
    child_node.depth = self.depth + 1
    self.children.append(child_node)
    child_node.__update_siblings()
    child_node.__update_siblings_count()
    child_node.__update_dimensions()

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

    # Update all siglings to left with new count
    prev_node = self.prev_sibling
    while prev_node:
        prev_node.siblings_count = self.siblings_count
        prev_node = prev_node.prev_sibling

    # Update all siglings to right with new count
    next_node = self.next_sibling
    while next_node:
        next_node.siblings_count = self.siblings_count
        next_node = next_node.next_sibling

  def __update_dimensions(self):
    pass
    # https://prnt.sc/uitUZvEqKlqt
    # Now you can use siblings_count to determine total with
    # IDK, use something from tkinter to determine text width
    # And then you can determine total with (margin + text width + margin)
    # Imagine you are building pyrmid, layer by layer
    # Given the node you have to update node's and it siblings positions
    # Then later you can draw 

class TreeVizualizer:
  def __init__(self, root: "TreeNode"):
    self.root = root

  def start(self):
    pass
    #Begin new thread and render tree each frame
    #In new thread we create window and call fucntion which will
    #Each node position and then render it

  def stop(self):
    pass

  def update(self):
    pass

  def render(self):
    pass

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
      if depth == -1: depth = self.find_max_depth(self.root)
      node = self.find_first_node_at_depth(self.root, depth)
      while node.prev_sibling: node = node.prev_sibling

      while node:
        if callback: callback(node)
        node = node.next_sibling

  def find_max_depth(self, node: Optional["TreeNode"] = None, current_max: int = 0) -> int:
      if node is None: node = self.root
      if not node.children: return max(current_max, node.depth)
      return max([self.find_max_depth(child, current_max) for child in node.children])

  def find_first_node_at_depth(self, node: Optional["TreeNode"] = None, depth: int = 0) -> Optional["TreeNode"]:
      if node is None: node = self.root
      if node.depth == depth: return node
      
      for child in node.children:
          found_node = self.find_first_node_at_depth(child, depth)
          if found_node: return found_node