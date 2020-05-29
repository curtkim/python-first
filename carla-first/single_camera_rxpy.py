import carla
import random
import time
import threading

import numpy as np
from PIL import Image

import pygame

import rx
from rx import operators as ops
from rx.scheduler.mainloop import PyGameScheduler

from _datetime import datetime

import torch
import torchvision.transforms as T
from detr import DETRdemo

from PIL import Image

#WIDTH, HEIGHT = pygame.display.get_surface().get_size()
#WIDTH = 1920 #*2
#HEIGHT = 1200 #*2

WIDTH = 1600
HEIGHT = 1000

def make_sensor(world, vehicle, rgb_bp, tf, fov):
    rgb_bp.set_attribute('image_size_x', str(WIDTH))
    rgb_bp.set_attribute('image_size_y', str(HEIGHT))
    rgb_bp.set_attribute('fov', str(fov))
    rgb_bp.set_attribute('sensor_tick', '0.033')
    return world.spawn_actor(rgb_bp, tf, attach_to=vehicle)


def image_carla2numpy(image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    return array


def from_sensor(sensor):
    def subscribe(observer, scheduler):
        def callback(image):
            #print('from_sensor', idx, threading.get_ident())
            observer.on_next(image_carla2numpy(image))
        sensor.listen(callback)

    return rx.create(subscribe)


# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

"""Let's put everything together in a `detect` function:"""
def detect(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    img = transform(im).unsqueeze(0)

    img = img.to('cuda:0')

    start_time = datetime.now()
    # propagate through the model
    outputs = model(img)
    print(datetime.now() - start_time)

    outputs['pred_logits'] = outputs['pred_logits'].to('cpu')
    outputs['pred_boxes'] = outputs['pred_boxes'].to('cpu')

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > 0.7

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)
    return probas[keep], bboxes_scaled

# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# colors for visualization
COLORS = [
    [0.000 * 256, 0.447 * 256, 0.741 * 256],
    [0.850 * 256, 0.325 * 256, 0.098 * 256],
    [0.929 * 256, 0.694 * 256, 0.125 * 256],
    [0.494 * 256, 0.184 * 256, 0.556 * 256],
    [0.466 * 256, 0.674 * 256, 0.188 * 256],
    [0.301 * 256, 0.745 * 256, 0.933 * 256]
]


def plot_results(surface, font, prob, boxes):
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), COLORS * 100):
        pygame.draw.rect(surface, c, (xmin, ymin, xmax-xmin, ymax-ymin), 2)

        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        textsurface = font.render(text, False, c)
        textRect = textsurface.get_rect()
        textRect.center = (xmin, ymin)
        surface.blit(textsurface, textRect)

        #ax.text(xmin, ymin, text, fontsize=15, bbox=dict(facecolor='yellow', alpha=0.5))

def main():

    detr = DETRdemo(num_classes=91)
    state_dict = torch.hub.load_state_dict_from_url(
        url='https://dl.fbaipublicfiles.com/detr/detr_demo-da2a99e9.pth',
        map_location='cpu', check_hash=True)
    detr.load_state_dict(state_dict)
    detr.eval();
    detr.to('cuda:0')

    transform = T.Compose([
        T.Resize(800),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    try:
        pygame.init()
        pygame.font.init()
        print(pygame.font.get_default_font())
        myfont = pygame.font.Font(pygame.font.get_default_font(), 16)

        pygame_scheduler = PyGameScheduler(pygame)

        display = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF)


        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)
        #client.load_world("/Game/Carla/Maps/Town10HD")

        world = client.get_world()

        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))
        rgb_bp = blueprint_library.find('sensor.camera.rgb')

        spawn_points = world.get_map().get_spawn_points()
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()

        vehicle = world.try_spawn_actor(bp, spawn_point)

        print('created %s' % vehicle.type_id)
        vehicle.set_autopilot(True)

        sensor = make_sensor(world, vehicle, rgb_bp, carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=0)), 120)
        image_ob = from_sensor(sensor)

        def grid_draw(params):
            print(threading.get_ident(), datetime.now(), "grid_draw")
            frame = params[0]
            image = params[1]
            scores, boxes = detect(Image.fromarray(image), detr, transform)
            #print(scores)
            surface = pygame.surfarray.make_surface(image.swapaxes(0, 1))
            display.blit(surface, (0, 0))
            #for box in boxes:
            #    pygame.draw.rect(surface, (255,0,0), (box[0], box[1], box[2]-box[0], box[3]-box[1]), 2)
            plot_results(display, myfont, scores, boxes)

            pygame.display.flip()


        rx.interval(0.1).pipe(
            ops.with_latest_from(image_ob),
            ops.observe_on(pygame_scheduler),
            ops.do_action(grid_draw)
        ).subscribe()

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick_busy_loop(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            print(threading.get_ident(), datetime.now(), "main")
            pygame_scheduler.run()

    except Exception as ex:
        print(ex)

    finally:
        print('finally')
        sensor.stop()
        sensor.destroy()
        vehicle.destroy()

        pygame.quit()
        print('done')


if __name__ == '__main__':
    main()
    print('last sleep')
    time.sleep(2)
