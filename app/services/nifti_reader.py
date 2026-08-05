import nibabel as nib

def read_nifti(path):

    try:

        img = nib.load(path)

        return {
            "shape": img.shape,
            "voxel_size": img.header.get_zooms()
        }

    except Exception as e:

        return {
            "error": str(e)
        }