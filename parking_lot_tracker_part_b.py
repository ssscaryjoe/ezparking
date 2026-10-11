# File: parking_lot_tracker_part_b.py
# Description: tracks parking-bay occupancy using an object-oriented design with encapsulation
# Author: Ezlan Sohani
# Date created: 2026-10-11


class ParkingBay:
	# Class: ParkingBay
	# Purpose: encapsulate parking bay state and operations
	def __init__(self, bayNumber):
		# initialise bay number and empty state
		self.__bayNumber = bayNumber
		self.__plate = ""
		self.__occupied = False

	# Method: parkCar()
	# Purpose: occupy a free bay with a licence plate
	# Inputs: plate string
	# Outputs: success bool and message string
	# Data types: string, bool
	def parkCar(self, plate):
		# reject if already occupied
		if self.__occupied:
			return False, "bay is already occupied"

		# reject empty plate
		cleaned_plate = plate.strip()
		if not cleaned_plate:
			return False, "invalid licence plate"

		self.__plate = cleaned_plate
		self.__occupied = True
		return True, "entry recorded"

	# Method: removeCar()
	# Purpose: free an occupied bay and clear the plate
	# Inputs: none
	# Outputs: success bool and message string
	# Data types: bool, string
	def removeCar(self):
		# reject if already empty
		if not self.__occupied:
			return False, "bay is empty"

		self.__plate = ""
		self.__occupied = False
		return True, "car removed"

	# Method: isOccupied()
	# Purpose: report occupancy status
	# Inputs: none
	# Outputs: True if occupied else False
	# Data types: bool
	def isOccupied(self):
		# report occupancy state
		return self.__occupied

	# Method: getBayNumber()
	# Purpose: report the bay number
	# Inputs: none
	# Outputs: bay number integer
	# Data types: int
	def getBayNumber(self):
		# report bay number
		return self.__bayNumber

	# Method: getPlate()
	# Purpose: report the licence plate
	# Inputs: none
	# Outputs: licence plate string
	# Data types: string
	def getPlate(self):
		# report licence plate
		return self.__plate


# Function: displayMenu()
# Purpose: show five menu options
# Inputs: none
# Outputs: prints menu
# Data types: none
def displayMenu():
	# menu choices
	print("\nparking lot tracker")
	print("1. record a car entering a bay")
	print("2. remove a car from a bay")
	print("3. view status of all bays")
	print("4. display occupancy totals")
	print("5. save data and exit")


# Function: loadData()
# Purpose: read saved state and update parking bay objects
# Inputs: lstBays list of ParkingBay objects
# Outputs: updates bay objects in place
# Data types: list, ParkingBay, int, string, bool
def loadData(lstBays):
	# load saved bay data into objects
	try:
		with open("parking_data.txt", "r", encoding="utf-8") as data_file:
			for line in data_file:
				parts = line.strip().split("|")
				if len(parts) != 3:
					continue

				bay_number_text, plate, occupied_text = parts
				try:
					bay_number = int(bay_number_text)
				except ValueError:
					continue

				for bay in lstBays:
					if bay.getBayNumber() == bay_number:
						if occupied_text == "True":
							bay.parkCar(plate)
						break
	except FileNotFoundError:
		# start with empty bays when no save file exists
		pass


# Function: saveData()
# Purpose: write current bay objects to file using getters
# Inputs: lstBays list of ParkingBay objects
# Outputs: writes parking_data.txt
# Data types: list, ParkingBay, int, string, bool
def saveData(lstBays):
	# save current bay objects using getters
	with open("parking_data.txt", "w", encoding="utf-8") as data_file:
		for bay in lstBays:
			data_file.write(
				f"{bay.getBayNumber()}|{bay.getPlate()}|{bay.isOccupied()}\n"
			)


# Function: isValidPlate()
# Purpose: check licence plate is non empty and valid chars
# Inputs: plate string
# Outputs: True if valid else False
# Data types: string, bool
def isValidPlate(plate):
	# basic plate validation
	cleaned_plate = plate.strip()
	return bool(cleaned_plate) and all(
		character.isalnum() or character in " -" for character in cleaned_plate
	)


# Function: getBay()
# Purpose: prompt user and find matching ParkingBay object
# Inputs: lstBays list of ParkingBay objects
# Outputs: ParkingBay object or None if invalid
# Data types: list, ParkingBay, int
def getBay(lstBays):
	# find bay object by user input
	try:
		bay_number = int(input("enter bay number: "))
	except ValueError:
		return None

	for bay in lstBays:
		if bay.getBayNumber() == bay_number:
			return bay
	return None


# Function: recordEntry()
# Purpose: park a car using bay object method
# Inputs: lstBays list of ParkingBay objects
# Outputs: updates bay object, prints confirmation or error
# Data types: list, ParkingBay, string, bool
def recordEntry(lstBays):
	# record entry using bay method
	bay = getBay(lstBays)
	if bay is None:
		print("invalid bay number")
		return

	plate = input("enter licence plate: ").strip()
	if not isValidPlate(plate):
		print("invalid licence plate")
		return

	success, message = bay.parkCar(plate)
	print(message)


# Function: removeCar()
# Purpose: remove a car using bay object method
# Inputs: lstBays list of ParkingBay objects
# Outputs: updates bay object, prints confirmation or error
# Data types: list, ParkingBay, bool
def removeCar(lstBays):
	# remove car using bay method
	bay = getBay(lstBays)
	if bay is None:
		print("invalid bay number")
		return

	success, message = bay.removeCar()
	print(message)


# Function: viewStatus()
# Purpose: show all bays with status and plate using getters
# Inputs: lstBays list of ParkingBay objects
# Outputs: prints every bay
# Data types: list, ParkingBay, int, string, bool
def viewStatus(lstBays):
	# display every bay using getters
	for bay in lstBays:
		status = "occupied" if bay.isOccupied() else "free"
		if bay.isOccupied():
			print(f"bay {bay.getBayNumber()}: {status} - {bay.getPlate()}")
		else:
			print(f"bay {bay.getBayNumber()}: {status}")


# Function: calculateTotals()
# Purpose: count total occupied and free bays using isOccupied()
# Inputs: lstBays list of ParkingBay objects
# Outputs: prints totals returns counts
# Data types: list, ParkingBay, int
def calculateTotals(lstBays):
	# calculate bay totals using isOccupied
	i_total = len(lstBays)
	i_occupied = 0

	for bay in lstBays:
		if bay.isOccupied():
			i_occupied += 1

	i_free = i_total - i_occupied
	print(f"total bays: {i_total}")
	print(f"occupied bays: {i_occupied}")
	print(f"free bays: {i_free}")
	return i_total, i_occupied, i_free


# Function: main()
# Purpose: initialise bay objects then run five option menu loop
# Inputs: none
# Outputs: runs menu updates bay objects saves on exit
# Data types: list, ParkingBay, string, bool
def main():
	# part b list of parking bay objects
	lstBays = [
		ParkingBay(1),
		ParkingBay(2),
		ParkingBay(3),
	]

	# load saved state before menu
	loadData(lstBays)
	b_running = True

	# menu loop
	while b_running:
		displayMenu()
		choice = input("choose an option: ").strip()

		if choice == "1":
			recordEntry(lstBays)
		elif choice == "2":
			removeCar(lstBays)
		elif choice == "3":
			viewStatus(lstBays)
		elif choice == "4":
			calculateTotals(lstBays)
		elif choice == "5":
			saveData(lstBays)
			print("data saved")
			print("program ended")
			b_running = False
		else:
			print("invalid choice")


if __name__ == "__main__":
	main()

