# File: parking_lot_tracker_part_a.py
# Description: tracks parking-bay occupancy using a dictionary of dictionaries
# Author: Ezlan Sohani
# Date created: 2026-09-12


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
# Purpose: read saved state and update dictBays
# Inputs: dictBays dict
# Outputs: updates dictBays in place
# Data types: dict, int, string, bool
def loadData(dictBays):
	# load saved bay data
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

				if bay_number in dictBays:
					dictBays[bay_number]["plate"] = plate
					dictBays[bay_number]["occupied"] = occupied_text == "True"
	except FileNotFoundError:
		# start with empty bays when no save file exists
		pass


# Function: saveData()
# Purpose: write current bay data to file
# Inputs: dictBays dict
# Outputs: writes parking_data.txt
# Data types: dict, int, string, bool
def saveData(dictBays):
	# save current bay data
	with open("parking_data.txt", "w", encoding="utf-8") as data_file:
		for bay_number, bay_data in dictBays.items():
			data_file.write(
				f"{bay_number}|{bay_data['plate']}|{bay_data['occupied']}\n"
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


# Function: getBayNumber()
# Purpose: get and validate bay number from user
# Inputs: dictBays dict
# Outputs: bay number int or None if invalid
# Data types: dict, int
def getBayNumber(dictBays):
	# get and validate bay number
	try:
		bay_number = int(input("enter bay number: "))
	except ValueError:
		return None

	if bay_number not in dictBays:
		return None
	return bay_number


# Function: recordEntry()
# Purpose: park a car in a free bay
# Inputs: dictBays dict
# Outputs: updates dictBays prints confirmation or error
# Data types: dict, int, string, bool
def recordEntry(dictBays):
	# record a car in a free bay
	bay_number = getBayNumber(dictBays)
	if bay_number is None:
		print("invalid bay number")
		return

	plate = input("enter licence plate: ").strip()
	if not isValidPlate(plate):
		print("invalid licence plate")
		return

	if dictBays[bay_number]["occupied"]:
		print("bay is already occupied")
		return

	dictBays[bay_number]["plate"] = plate
	dictBays[bay_number]["occupied"] = True
	print("entry recorded")


# Function: removeCar()
# Purpose: remove a car from an occupied bay
# Inputs: dictBays dict
# Outputs: updates dictBays prints confirmation or error
# Data types: dict, int, bool
def removeCar(dictBays):
	# remove a car from an occupied bay
	bay_number = getBayNumber(dictBays)
	if bay_number is None:
		print("invalid bay number")
		return

	if not dictBays[bay_number]["occupied"]:
		print("bay is empty")
		return

	dictBays[bay_number]["plate"] = ""
	dictBays[bay_number]["occupied"] = False
	print("car removed")


# Function: viewStatus()
# Purpose: show all bays with status and plate
# Inputs: dictBays dict
# Outputs: prints every bay
# Data types: dict, int, string, bool
def viewStatus(dictBays):
	# display every bay
	for bay_number, bay_data in dictBays.items():
		status = "occupied" if bay_data["occupied"] else "free"
		if bay_data["occupied"]:
			print(f"bay {bay_number}: {status} - {bay_data['plate']}")
		else:
			print(f"bay {bay_number}: {status}")


# Function: calculateTotals()
# Purpose: count total occupied and free bays
# Inputs: dictBays dict
# Outputs: prints totals returns counts
# Data types: dict, int
def calculateTotals(dictBays):
	# calculate bay totals
	i_total = len(dictBays)
	i_occupied = 0

	for bay_data in dictBays.values():
		if bay_data["occupied"]:
			i_occupied += 1

	i_free = i_total - i_occupied
	print(f"total bays: {i_total}")
	print(f"occupied bays: {i_occupied}")
	print(f"free bays: {i_free}")
	return i_total, i_occupied, i_free


# Function: main()
# Purpose: load data then run five option menu loop
# Inputs: none
# Outputs: runs menu updates dictBays saves on exit
# Data types: dict, string, bool
def main():
	# part a dictionary of dictionaries
	dictBays = {
		1: {"plate": "", "occupied": False},
		2: {"plate": "", "occupied": False},
		3: {"plate": "", "occupied": False},
	}

	# load saved state before menu
	loadData(dictBays)
	b_running = True

	# menu loop
	while b_running:
		displayMenu()
		choice = input("choose an option: ").strip()

		if choice == "1":
			recordEntry(dictBays)
		elif choice == "2":
			removeCar(dictBays)
		elif choice == "3":
			viewStatus(dictBays)
		elif choice == "4":
			calculateTotals(dictBays)
		elif choice == "5":
			saveData(dictBays)
			print("data saved")
			print("program ended")
			b_running = False
		else:
			print("invalid choice")


if __name__ == "__main__":
	main()
