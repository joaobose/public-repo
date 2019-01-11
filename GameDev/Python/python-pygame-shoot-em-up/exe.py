from cx_Freeze import setup, Executable

setup(name = "Smup",
	   version = "0.1.2", 
	   description = ".",
	   executables = [Executable("game.py")],)