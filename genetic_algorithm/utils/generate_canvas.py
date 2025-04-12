from PIL import Image, ImageDraw
from .create_individuals import create_individuals

def canvas_to_image(canvas, width=500, height=500):
    image = Image.new('RGBA', (width, height), (255, 255, 255, 255))

    for triangle in canvas.triangles:
        triangle_temp = Image.new('RGBA', (width, height), (0, 0, 0, 0))    # creo el template para el triángulo
        draw = ImageDraw.Draw(triangle_temp, 'RGBA')    # permite dibujar sobre el template

        vertexes = triangle.vertexes
        r, g, b, a = triangle.color
        alpha = int(a * 255)

        draw.polygon(vertexes, fill=(r, g, b, alpha))   # dibujo el triángulo en el template
        image = Image.alpha_composite(image, triangle_temp)  # superpongo el triángulo al canvas
    
    image_rgb = image.convert('RGB')
    return image_rgb


if __name__ == "__main__":
    individuals = create_individuals(1, 50) 
    image = canvas_to_image(individuals[0])
    image.show()
    image.save("output.png")
