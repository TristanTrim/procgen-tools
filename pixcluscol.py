
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


## debug tool
import os
def dbgmsg(msg): # hacky: print to server term (since matplotlib eats print)
    os.write(1, (msg+"\n").encode())
## /debug tool








class InteractivePixCol():
  """
  USE WITH:
  %matplotlib ipympl

  pass in 2d array (image) of class index labels: [1, n-labels]

  """

  def __init__(self,
          cluster_img,
          ):

      self.cluster_img = cluster_img

      self.num_labels = cluster_img.max()
      self.label_indices = tuple(range(self.num_labels))
      self.label_names = list(
              "_"+str(i+1) 
              for i in self.label_indices)

      self.shape = cluster_img.shape

      self._cluster_mask = np.full(
              (self.num_labels,) + self.shape,
              False,
              )
      self.color_img = np.zeros(
              self.shape+(3,),
              dtype=int,
              )
      self._precomp_imgs = np.zeros(
              (self.num_labels,) + self.shape+(3,),
              dtype=int,
              )
      self.palette = [[0,0,0],] * self.num_labels
      self._colbox = None

      # get everything ready !

      self._make_clus_mask()
      self._make_colbox()
      self._disable_hotkeys()

      self._do_precomp()
      
      self._fig, self._ax, self._img, self._txt = (None,)*4

      # vars for interactivity:
      self.prevGroup = None
      self.choosing_color = None
      self.label_buf = None
      self.overFig = False


  def _disable_hotkeys(self):

      # backup
      self._keymap_backup = list(((k,v) for k,v in plt.rcParams.items() if k.startswith("keymap") ))

      # DISABLE MATPLOTLIB HOTKEYS
      for k,v in plt.rcParams.items():
          if k.startswith("keymap"):
              plt.rcParams[k] = []

  def _restore_hotkeys(self):
      print("nyi")

  def _make_colbox(self):
      colbox = np.arange(256)/256
      colbox = np.broadcast_to(colbox,(256,256))
      colbox = np.stack((
            colbox, 
            np.full((256,256),.7),
            1-colbox.T*.6
            ))
      colbox = colbox.transpose((1,2,0))
      colbox = matplotlib.colors.hsv_to_rgb(colbox)

      self._colbox = colbox
      
  def _make_clus_mask(self):
      for i in self.label_indices:
        self._cluster_mask[i] = ( 1+i == self.cluster_img )

  def _do_precomp(self):
      for i in self.label_indices:
        self._precomp_imgs[i] = self.color_img//2+32

        self._precomp_imgs[i][self._cluster_mask[i]] = [200,200,200]
        #self._precomp_imgs[i][self._cluster_mask[i]] = [223,223,223]

  def _recalc_color_img(self):
      for i in self.label_indices:
          self.color_img[self._cluster_mask[i]] = self.palette[i]


  def drawPlot(self):
      
      self._fig, self._ax = plt.subplots()
      self._img = self._ax.imshow(self.color_img)

      self._txt = self._ax.text(0,-2.4,"",
               # color = (1,1,1,0.4),
               # backgroundcolor=(0,0,0,0.2),
               color = (1,1,1),
               backgroundcolor=(0,0,0),
               )


       ############################ ###  #
      ## define interactivity ### ### ### # #
       ############################ ###  #

      def on_motion(event):
          if not self.overFig: return
          if(not (self.choosing_color is None)): return
          
          group_index = self.cluster_img[round(event.ydata),round(event.xdata)] - 1

          if (not group_index == self.prevGroup):
              self.prevGroup = group_index
              self._img.set(data=self._precomp_imgs[group_index])

              self.label_buf = self.label_names[group_index]

              self._txt.set(
                  text=f"{str(group_index)}: {self.label_buf}" )

      self._fig.canvas.mpl_connect('motion_notify_event', on_motion)

      def on_enter_axis(event):
          if event.inaxes == self._ax:
              self.overFig = True

      self._fig.canvas.mpl_connect("axes_enter_event", on_enter_axis)

      def on_leave_axis(event):
          self.overFig = False
          if not self.choosing_color:
              self._img.set(data=self.color_img)

      self._fig.canvas.mpl_connect("axes_leave_event", on_leave_axis)

      def on_click(event):
        if self.overFig:
          if self.choosing_color is None:
              self.choosing_color = self.cluster_img[round(event.ydata),round(event.xdata)] - 1
              self._img.set(data=self._colbox)
              self.label_buf = self.label_names[self.choosing_color]

          else:
              new_color = self._img.get_cursor_data(event)

              # put in palette
              self.palette[self.choosing_color] = (new_color*256).astype(int).tolist()
              # recolor in image
              self.color_img[self._cluster_mask[self.choosing_color]] = new_color*256
              # show user
              self._img.set(data=self.color_img)
              # reset vars
              self.choosing_color = None
              self.label_buf = None
              # recompute higlight imgs
              # this could be optimized but w/e
              self._do_precomp()

      self._fig.canvas.mpl_connect("button_release_event", on_click)

      def on_keypress(event):
          _editing = "(editing)"
          if event.key in( "shift+backspace", "ctrl+backspace", "ctrl+d"):
              self.label_buf = ""
          elif event.key == "escape":
              self.choosing_color = None
              self._img.set(data=self.color_img)
          elif event.key == "backspace":
              self.label_buf = self.label_buf[:-1]
          elif event.key == "enter":
              self.label_names[self.prevGroup] = self.label_buf
              _editing = ""
              self.choosing_color = None
              self._img.set(data=self._precomp_imgs[self.prevGroup])
          elif len(event.key)==1:    
              self.label_buf += event.key
          
          self._txt.set( text=f"{str(self.prevGroup)}{_editing}: {self.label_buf}" )

      self._fig.canvas.mpl_connect("key_press_event",on_keypress)

       ############################ ###  #
      ##    end interactivity ### ### ### # #
       ############################ ###  #

  def classif_to_str(self):
      return str([
                    list(self.palette),
                    self.label_names,
                    (self.cluster_img.flatten()-1).tolist(), # minus 1 to zero indexing
                ]).replace("'",'"')

  def printClassif(self):
      print(self.classif_to_str())

  def loadClassif(self, classif):
      p, l, ci = classif

      self.palette = p
      self.label_names = l
      self.cluster_img = np.array(ci).reshape(self.shape) + 1 # plus 1 to one indexing

      self._recalc_color_img()
      self._img.set(data=self.color_img)
      self._do_precomp()

