blmm.exe: dist/main.exe
	mv ./dist/main.exe ./blmm.exe

dist/main.exe: main.py
	pyinstaller --icon res/icon.ico --onefile main.py

clean:
	rm -rf ./dist
	rm -rf ./build
	rm main.spec