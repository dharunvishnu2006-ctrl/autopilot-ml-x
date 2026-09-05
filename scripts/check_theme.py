from PIL import Image

img = Image.open("test_chart.png").convert("RGBA")
white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
combined = Image.alpha_composite(white_bg, img)
combined.convert("RGB").save("test_chart_on_white.png")
print("saved test_chart_on_white.png")