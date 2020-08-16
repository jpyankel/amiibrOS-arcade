from FBpyGIF import fb
from argparse import ArgumentParser
from pathlib import Path

root_path = (Path(__file__).parent.parent).resolve()
app_path = root_path / "app"
resource_path = root_path / "resources"

BIT_DEPTH = 8
FRAME_BUFFER = 0

def main(image_name):
    img_path = str(resource_path / image_name)

    fb.ready_fb(BIT_DEPTH, FRAME_BUFFER)
    fb.show_img(fb.ready_img(img_path))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-img", action="store", required=True, dest="image_name", help="name of splash image")

    args = parser.parse_args()
    main(args.image_name)