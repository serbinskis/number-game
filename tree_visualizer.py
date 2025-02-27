class TreeNode:
  def __init__(self, text, parent=None):
    self.text = text
    self.parent = parent
    self.children = []
    self.sibling = None #Sigling is next node in the same depth
    self.width = -1 #Calculate based on text width
    self.height = -1 #Calculate based on text height
    self.position = [-1, -1] #Calculate based on depth and depth_count + width and height
    self.depth = -1 #Nodes depth, I guess we can start with 1 or 0, as you like
    self.depth_count = -1 #How many nodes there are on the same depth

  def add_children(self, child_node):
    self.children.append(child_node)
    if (child_node.parent = None): child_node.parent = self

class TreeVizualizer:
  def __init__(self, root):
    self.root = root

  def start(self)
    #Begin new thread and render tree each frame
    #In new thread we create window and call fucntion which will
    #Each node position and then render it

  def stop(self):
    pass

  def update(self):
    pass

  def render(self):
    pass
    
