from gradio import Image
from PIL import Image, ImageFilter

class smooth_filter:
    def apply(self, pil_img: Image.Image) -> Image.Image:
        return pil_img.filter(ImageFilter.SMOOTH)

class edge_filter:
    def apply(self, pil_img: Image.Image) -> Image.Image:
        return pil_img.filter(ImageFilter.FIND_EDGES)

class sharpen_filter:
    def apply(self, pil_img: Image.Image) -> Image.Image:
        return pil_img.filter(ImageFilter.SHARPEN)

class blur_filter:
    def apply(self, pil_img: Image.Image) -> Image.Image:
        return pil_img.filter(ImageFilter.BLUR)
    
class contour_filter:
    def apply(self, pil_img: Image.Image) -> Image.Image:
        return pil_img.filter(ImageFilter.CONTOUR)

