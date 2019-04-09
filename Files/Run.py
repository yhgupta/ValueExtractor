from Files.POST import get_image
from Files.TableFinder import table_create

testName = "vitamin"
image = r"Directory containing Image to be analyzed"
get_image(testName, image)
table_create(testName)
