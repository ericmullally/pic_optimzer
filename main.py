from PIL import Image, ImageEnhance
import os
import sys


class Optimizer:
    def __init__(self, old_file, output_file):
        self.imgs_path = old_file
        self.old_file = os.listdir(old_file)
        self.output_file = output_file
        self.operations_to_perform = None
        self.form = "jpeg"

    def get_request(self):
        choices = {"1": "change_size", "2": "sharpen", "3": "change_file_type"}
        print("what would you like to do with these photos?")
        for key, value in choices.items():
            print(f"{key} : {value}")
        user_answer = input("please separate multiple choices with commas: ")
        while len(user_answer) > 1 and not "," in user_answer:
            user_answer = input(
                "please separate multiple choices with commas: ")
        answer_arr = user_answer.split(",")
        self.operations_to_perform = [choices[x] for x in answer_arr]

    def calc_size(self, img, size_tuple):
        width, height = size_tuple[0], size_tuple[1]
        if width < height:
            base_width = width
            width_percent = (base_width/float(img.size[0]))
            height = int((float(img.size[1])*float(width_percent)))
            return (base_width, height)
        else:
            base_height = height
            height_percent = (base_height/float(img.size[1]))
            width = int((float(img.size[0])*float(height_percent)))
            return (width, base_height)

    def change_size(self, img_str, size_desired):
        try:
            img = Image.open(f"{self.imgs_path}/{img_str}")
            size = self.calc_size(img, size_desired)
            new_img = img.resize(size, Image.LANCZOS)
            print(f"{img_str} resized to {new_img.size} to maintain aspect ratio")
            return new_img
        except OSError:
            print(OSError)

    def sharpen(self, img):
        enhancer = ImageEnhance.Sharpness(img)
        factor = 2.0
        new_img = enhancer.enhance(factor)
        return new_img

    def save_imgs(self):
        if "change_size" in self.operations_to_perform:
            height = int(input("what height would you like? "))
            width = int(input("what width would you like? "))
        new_imgs = []
        for item in self.old_file:
            new_img = item
            for term in self.operations_to_perform:
                if term == "change_size":
                    new_img = self.change_size(item, (width, height))
                if term == "change_file_type":
                    pass
                if term == "sharpen":
                    if type(new_img) == str:
                        sharpened_img = self.sharpen(
                            Image.open(f"{self.imgs_path}/{new_img}"))
                    else:
                        sharpened_img = self.sharpen(new_img)
                    new_img = sharpened_img
            new_imgs.append(new_img)
        for i, img in enumerate(new_imgs):
            img.save(f"{self.output_file}/new_img{i}.png", "png")


if __name__ == "__main__":
    if not os.path.exists("./output_file"):
        os.mkdir("output_file")
    new_pics = Optimizer(sys.argv[1], "output_file")
    new_pics.get_request()
    new_pics.save_imgs()
