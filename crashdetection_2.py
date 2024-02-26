import torch
from PIL import Image, ImageDraw
import cv2
from centroidtracker import CentroidTracker
ct = CentroidTracker()

class Detections:
    def __init__(self):
        model_path = r'C:\Users\ravis\OneDrive\Desktop\crash_detection_2.0\best.pt'
        self.model1 = self.__load_model(model_path,'image')
        self.model2 = self.__load_model(model_path,'video')
        self.classes1 = self.model1.names
        self.classes2 = self.model2.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.objects_labels = {0:'car-accident',1:'bike',2:'car',3:'truck'}
        self.speed_factor = 2    # speed factor for adjusting speed of frames to be detected
        self.min_width_rectangle = 30    # min  width of rectangle over car
        self.min_height_rectangle = 30   # min height of rectangle over car
        self.count = 0
        self.center_pt_previous_frame = []

    def __load_model(self, model_path, status):
        if model_path and status == 'image':
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model
    
    def call_for_image(self, image_path):
        # Load and preprocess the image
        image_path = rf'C:\Users\ravis\OneDrive\Desktop\crash_detection_2.0\images\{image_path}.jpg'
        image = Image.open(image_path)
        
        results = self.model1(image)
        print(results)
        draw = ImageDraw.Draw(image)
        
        # Access bounding boxes, labels, and scores from results tensor
        boxes = results.xyxy[0][:, :4]  # Extract bounding box coordinates (x1, y1, x2, y2)
        labels = results.xyxy[0][:, 5]  # Extract class labels
        scores = results.xyxy[0][:, 4]  # Extract confidence scores
    
        # Iterate over detected objects and draw bounding boxes
        for box, label, score in zip(boxes, labels, scores):
            box = box.tolist()
            label = int(label.item())
            score = float(score.item())
            label_name = self.objects_labels.get(label, None)
            # Check if the label corresponds to a car accident
    
            if label_name == 'car-accident' and score>0.33:
                # Calculate text size and position
                # Draw bounding box
                draw.rectangle(xy=box, outline='red', width=2)
                text = f"car-accident : {score:.2f}"
                text_width, text_height = draw.textsize(text)
                text_position = (box[0], box[1] - text_height - 5)  # Position the text above the bounding box
                
                # Draw red strip background
                draw.rectangle([box[0], box[1] - text_height - 5, box[0] + text_width, box[1]], fill='red')
                
                # Add label text
                draw.text(text_position, text, fill='white')
        
        # Display the image with bounding boxes
        image.show()

    def __center_and_dimensions(self, x1, y1, x2, y2):
        '''
        x1 is x co-ordinate of top left corner of box
        x2 is x co-ordinate of bottom right corner of box
        y1 is y co-ordinate of top left corner of box
        y2 is y co-ordinate of bottom right corner of box

        function for finding center , width and height of the box
        '''
        cx = (x1 + x2)/2
        cy = (y1 + y2)/2
        h = y2 - y1
        w = x2 - x1
        return int(cx), int(cy), h, w
    
    def call_for_video(self, video_path):
        
        video_path = rf'C:\Users\ravis\OneDrive\Desktop\crash_detection_2.0\videos\{video_path}.mp4'
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened(): 
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame.")
                break

            self.count += 1

            # Performing YOLOv5 object detection
            results = self.model2(frame)

            # Getting the detection results for single frame
            detections = results.xyxy[0] 
            print(detections)
            desired_classes = ["car", "bike", "truck", "car-accident"]
            conf_threshold = 0.4        # confidence of the object to be the object from the desired class

            # Filter the detections based on the desired classes and confidence threshold
            filtered_detections = [x for x in detections if (self.classes2[int(x[5])] in desired_classes)]

            center_pt_current_frame =[]
            # forming bounding boxes for the filtered detections
            for box in filtered_detections:
                x1, y1, x2, y2, conf, class_id = box
                print(x1, y1, x2, y2, conf, class_id)
                cx, cy, h, w = self.__center_and_dimensions(x1.item(), y1.item(), x2.item(), y2.item())
                validate_counter = (w >= self.min_width_rectangle) and (h >= self.min_height_rectangle)
                if not validate_counter:
                    continue

                center_pt_current_frame.append((cx, cy))
            
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(cx),int(cy)), 4, (0, 0, 255), -1)
            

            tracked_dict = ct.register(center_pt_current_frame, self.center_pt_previous_frame, self.count)
            
            for object_id, pt in tracked_dict.items():
                cv2.circle(frame, pt, 5, (0,0,225), -1)

            self.center_pt_previous_frame = center_pt_current_frame.copy()
            # Display the frame with bounding boxes
            cv2.imshow('YOLOv5 Object Detection', frame)

            delay = int(1000 / (self.speed_factor * cap.get(cv2.CAP_PROP_FPS)))
            if cv2.waitKey(delay) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()
        # Display the results

