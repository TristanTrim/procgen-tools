
import numpy as np


def to_ndsp_file(data, labels=None, title="untitled", dimAx=0, afAx=None):
    """
    to_ndsp_file(data, labels=None, title="untitled", dimAx=0, afAx=None)

    data: nd numpy array
    labels: 1d numpy array integer classes of each datapoint
            or "zeros" to generate empty classes
    title: human readable string for file identification.
          If title starts with a path, the file will be
          saved at that location.

    dimAx: which axis should be used for dimensions in ndsp
    afAx: which axis should become animated timeline.
          set None for no timeline.

    ( axes not marked by dimAx or afAx will be treated as datapoints )

    """

    # move from torch to numpy if not already done
    if not type(data) == np.ndarray:
        data = data.detach().numpy()
    
    # get the dimension indices
    axes = list(range(data.ndim))
    
    # move dimension vals to end
    axes.remove(dimAx)
    axes.append(dimAx)
    
    # move animation frames to start
    if not afAx is None:
        axes.remove(afAx)
        axes.insert(0,afAx)
    
    # reshape data
    transposed_data = np.transpose(data, axes=axes)
    shape = transposed_data.shape
    if not afAx is None:
        reshaped_data = transposed_data.reshape([shape[0],-1,shape[-1]])
    else:
        reshaped_data = transposed_data.reshape([-1,shape[-1]])

    # get shape info for flname
    shape = reshaped_data.shape
    if afAx is None:
        af = 1
    else:
        af = shape[0]
    dp = shape[-2]
    dim = shape[-1]

    # save data
    flname = f"{title}._{af}af_{dp}dp_{dim}dim_.bin"
    reshaped_data.tofile(flname)

    # save labels if any
    if not labels is None:
        if labels=="zeros":
            labels = np.zeros(dp,dtype=np.uint8)
        
        flname = f"{title}_labels._{af}af_{dp}dp_{dim}dim_.bin"
        labels.tofile(flname)
            

def classif_pastedump(colors, labels, classif):
    """
    classif_pastedump(colors, labels, classif)

    colors: list of rgb lists. values in [0, 255] as you do.
    labels: list of strings or stringable obj for class labels.
    classif: 0 indexed label class for each datapoint
    """
    colors = list(list(x) for x in colors)
    labels = list(str(x) for x in labels)
    classif = list(int(x) for x in classif)

    return str([colors, labels, classif]).replace("'",'"')


def nddata_pastedump(data, title="untitled", dimAx=0, afAx=None):
    """
    nddata_pastedump(data, title="untitled", dimAx=0, afAx=None)

    data: nd numpy array
    title: human readable string for file identification

    dimAx: which axis should be used for dimensions in ndsp
    afAx: which axis should become animated timeline.
          set None for no timeline.

    ( axes not marked by dimAx or afAx will be treated as datapoints )

    """
    print("nyi")
    return

    # move from torch to numpy if not already done
    if not type(data) == np.ndarray:
        data = data.detach().numpy()
    
    # get the dimension indices
    axes = list(range(data.ndim))
    
    # move dimension vals to end
    axes.remove(dimAx)
    axes.append(dimAx)
    
    # move animation frames to start
    if not afAx is None:
        axes.remove(afAx)
        axes.insert(0,afAx)
    
    # reshape data
    transposed_data = np.transpose(data, axes=axes)
    shape = transposed_data.shape
    if not afAx is None:
        reshaped_data = transposed_data.reshape([shape[0],-1,shape[-1]])
    else:
        reshaped_data = transposed_data.reshape([-1,shape[-1]])

    # get shape info for flname
    shape = reshaped_data.shape
    if afAx is None:
        af = 1
    else:
        af = shape[0]
    dp = shape[-2]
    dim = shape[-1]

    # save data
    flname = f"{title}._{af}af_{dp}dp_{dim}dim_.bin"

    reshaped_data.tofile(flname)

