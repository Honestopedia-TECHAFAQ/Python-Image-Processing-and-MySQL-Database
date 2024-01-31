import mysql.connector
import cv2
import numpy as np
from tkinter import Tk, filedialog
db_connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)
def add_images_to_database(image_paths):
    cursor = db_connection.cursor()
    for path in image_paths:
        with open(path, "rb") as file:
            image_data = file.read()
            insert_query = "INSERT INTO images (image) VALUES (%s)"
            cursor.execute(insert_query, (image_data,))
    db_connection.commit()
    cursor.close()
def retrieve_images_from_database():
    cursor = db_connection.cursor()
    cursor.execute("SELECT image FROM images")
    images = cursor.fetchall()
    cursor.close()
    return images
def analyze_images(images):
    for image_data in images:
        nparr = np.frombuffer(image_data[0], np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
def select_images():
    root = Tk()
    root.withdraw() 

    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    return file_paths
if __name__ == "__main__":
    selected_image_paths = select_images()

    if not selected_image_paths:
        print("No images selected. Exiting.")
    else:
        add_images_to_database(selected_image_paths)
        retrieved_images = retrieve_images_from_database()
        analyze_images(retrieved_images)
