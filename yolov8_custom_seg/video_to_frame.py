import cv2
import os

def video_to_frames(video_path, output_folder, num_frames=200, filename_format="frame_{:04d}.jpg"):
    try:
        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Unable to open video file {video_path}")
            return
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total_frames // num_frames)
        
        frame_count = 0
        saved_count = 0
        
        while cap.isOpened() and saved_count < num_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % step == 0:
                frame_filename = os.path.join(output_folder, filename_format.format(saved_count))
                cv2.imwrite(frame_filename, frame)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        print(f"Saved {saved_count} frames to {output_folder}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_path = 'akomulator_i_osiguraci_Noc.mp4'  # Replace with the actual path to your video
output_folder = 'output_frames_akomulator_i_osiguraci_Noc'  # Replace with your desired output folder
filename_format = 'akomulator_i_osiguraci_Dan_{:04d}.jpg'  # Replace with your desired filename format
video_to_frames(video_path, output_folder, num_frames=200, filename_format=filename_format)
