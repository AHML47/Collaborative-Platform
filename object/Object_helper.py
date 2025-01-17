import cv2
class ObjectHelper:
    def __init__(self ,id,color,shape,size,x,y) :
        self.id = id
        self.color = color
        self.shape = shape
        self.size = size
        self.x = x
        self.y = y

    def calculateXY(self):
        return (self.x-self.size//2,self.y-self.size//2),(self.x+self.size//2,self.y+self.size//2)

    def draw(self, frame, Nx, Ny):
        frame_height, frame_width, _ = frame.shape
        # Calculate center of the square based on the normalized inputs
        center_x = int(Nx * frame_width)
        center_y = int(Ny * frame_height)

        # Define the size of the square


        # Calculate top-left and bottom-right corners
        top_left ,bottom_right = self.calculateXY()



        if top_left[0]<center_x<bottom_right[0] and top_left[1]<center_y<bottom_right[1]:
            # Ensure the center of the square is within the bounding box
            print(
                f"x: {center_x}, y: {center_y} xA: {top_left[0]}, xB: {bottom_right[0]} yA: {top_left[1]}, yB: {bottom_right[1]}"
            )

            # Update the square's position
            self.x = center_x
            self.y = center_y
            top_left, bottom_right = self.calculateXY()


        # Draw the square on the frame
        cv2.rectangle(frame, top_left, bottom_right, self.color, -1)
        return frame



