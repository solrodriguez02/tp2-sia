import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from utils.generate_canvas import canvas_to_image

class FitnessFunction:
    def __init__(self, target_image):
        self.target_image = target_image
    # Usa cv2 para obtener la diferencia absoluta de cada píxel entre dos imágenes
    # Devuelve el promedio de esas diferencias 
    def fitness_avg_pixel_difference(self, individual):
        imageA = self.target_image
        imageB = canvas_to_image(individual)
        imageB = np.array(imageB)
        if imageB.shape[2] == 4:
        # dropping the alpha channel
            imageB = imageB[:, :, :3]
        imageB = cv2.resize(imageB, (self.target_image.shape[1], imageA.shape[0]))
        diff = cv2.absdiff(imageA, imageB) # Calcula la diferencia absoluta por píxel
        diff_mean = np.mean(diff) 
        simil_percent = 1 - (diff_mean / 255)
        return simil_percent 

    # Calcula el error cuadrático medio (MSE: Mean Squared Error) entre las dos imágenes
    # Toma la diferencia de cada píxel, la eleva al cuadrado, y promedia todo
    # Penaliza más fuerte las diferencias grandes (o al menos deberia hacerlo)
    def fitness_mse(self, individual):
        imageA = self.target_image
        imageB = canvas_to_image(individual)
        imageB = np.array(imageB)
        if imageB.shape[2] == 4:
        # dropping the alpha channel
            imageB = imageB[:, :, :3]

        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
        err = np.mean((imageA.astype("float") - imageB.astype("float")) ** 2)
        simil_percent = 1 - (err / 255**2)

        return simil_percent

    # Calcula el SSIM (Structural Similarity Index), que compara estructura, luminancia y contraste
    # Parte de las imágenes en escala de grises
    def fitness_ssim(self, individual):
        imageA = self.target_image
        imageB = canvas_to_image(individual)
        imageB = np.array(imageB)
        if imageB.shape[2] == 4:
        # Option 1: Simply drop the alpha channel
            imageB = imageB[:, :, :3]

        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
        score, _ = ssim(imageA, imageB, full=True)
        return 1 - score  



#if __name__ == "__main__":

    # Pruebas para cada función de fitness	

    # Cargar las imágenes
    #imageA = cv2.imread("./images/image_1.png")
    #imageB = cv2.imread("./images/image_2.png")
    #imageC = cv2.imread("./images/image_3.png")
    #imageD = cv2.imread("./images/image_4.png")
    #imageE = cv2.imread("./images/image_5.png")
    #imageF = cv2.imread("./images/image_6.png")

    # Calcular la diferencia absoluta
    #fitness_value = fitness_avg_pixel_difference(imageA, imageB)
    #print(f"Fitness value 1: {fitness_value}")

    #fitness_value = fitness_avg_pixel_difference(imageA, imageC)
    #print(f"Fitness value 2: {fitness_value}")

    #fitness_value = fitness_avg_pixel_difference(imageA, imageD)
    #print(f"Fitness value 3: {fitness_value}")

    #fitness_value = fitness_avg_pixel_difference(imageA, imageE)
    #print(f"Fitness value 4: {fitness_value}")

    #fitness_value = fitness_avg_pixel_difference(imageA, imageF)
    #print(f"Fitness value 5: {fitness_value}")


    # Calcular el MSE
    #mse_value = fitness_mse(imageA, imageB)
    #print(f"MSE value 1: {mse_value}")

    #mse_value = fitness_mse(imageA, imageC)
    #print(f"MSE value 2: {mse_value}")

    #mse_value = fitness_mse(imageA, imageD)
    #print(f"MSE value 3: {mse_value}")

    #mse_value = fitness_mse(imageA, imageE)
    #print(f"MSE value 4: {mse_value}")

    #mse_value = fitness_mse(imageA, imageF)
    #print(f"MSE value 5: {mse_value}")


    # Calcular el SSIM
    #ssim_value = fitness_ssim(imageA, imageB)
    #print(f"SSIM value: {ssim_value}")

    #ssim_value = fitness_ssim(imageA, imageC)
    #print(f"SSIM value: {ssim_value}")

    #ssim_value = fitness_ssim(imageA, imageD)
    #print(f"SSIM value: {ssim_value}")

    #ssim_value = fitness_ssim(imageA, imageE)
    #print(f"SSIM value: {ssim_value}")

    #ssim_value = fitness_ssim(imageA, imageF)
    #print(f"SSIM value: {ssim_value}")

