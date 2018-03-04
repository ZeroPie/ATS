from PIL import Image, ImageDraw

class VectorMap:

	def __init__(self, gridSize, unitSize):
		self.gridSize = gridSize
		self.unitSize = unitSize

		imgSizeX = (gridSize[0]+2)*unitSize
		imgSizeY = (gridSize[1]+2)*unitSize
		self.lineWidth = unitSize / 7
		if self.lineWidth <= 0:
			self.lineWidth = 1

		self.im = Image.new("RGB", (imgSizeX, imgSizeY), "white")
		self.draw = ImageDraw.Draw(self.im)

	def drawVector(self, basis, richtung, dif):
		pointTu = ()
		for i in range(0, 2):
			pointTu = pointTu + (basis[i]*self.unitSize + self.unitSize, )
		for i in range(0, 2):
			n = basis[i] * self.unitSize + richtung[i] * (self.unitSize/2)
			n = n + self.unitSize
			pointTu = pointTu + (n , )
		f = int(dif * 500)
		if f > 255:
			f = 255
		vC = (f, 0, 255 - f)
		self.draw.line(pointTu, fill=vC, width = self.lineWidth)
		kreisEck = pointTu[2] - self.lineWidth, pointTu[3] - self.lineWidth
		kreisEck = kreisEck + (pointTu[2] + self.lineWidth, pointTu[3] + self.lineWidth)
		self.draw.ellipse(kreisEck, fill=vC, outline=128)

	def drawLandmark(self, basis):
		pointTu = ()
		for i in range(0, 2):
			pointTu = pointTu + (basis[i]*self.unitSize + self.unitSize, )
		kreisEck = (pointTu[0] - self.unitSize/2, pointTu[1] - self.unitSize/2)
		kreisEck = kreisEck + (pointTu[0] + self.unitSize/4, pointTu[1] + self.unitSize/4)
		self.draw.ellipse(kreisEck, fill=50, outline=50)

	def saveMap(self, path):
		self.im.save(path, "PNG")

if __name__ == "__main__":
	map = VectorMap((14, 14), 20)
	map.drawVector((0, 0), (1, 0))
	map.drawVector((1, 0), (0, -1))
	map.drawVector((0, 1), (-1, 0))
	map.drawVector((1, 1), (0.71, 0.71))
	map.drawVector((14, 14), (-1, 0))
	map.saveMap("testPic")
