# ZodiacMotion

**ZodiacMotion** is a Python program that creates a zodiacal motion between two different times according to given latitude and longitude values. The program calculates the zodiacal positions repeatedly by adding the amount of time increase to the starting date until it becomes equal to the finishing date. The increase time amount range is between 1 to 3600 seconds. Displaying the chart depends on the refresh scale which has a range between 0 and 10 seconds. The house system and orb factors are changeable.

## Availability

Linux, Mac, Windows

## Dependencies

In order to run **ZodiacMotion**, at least Python's 3.6 version must be installed on your computer. Note that in order to use Python on the command prompt, Python should be added to the PATH.

There are several libraries that the program requires. In order to install these requirements users should type the below command on console window.

```
pip3 install -r requirements.txt
```

## Usage

**For Linux and Mac**

```
python3 ZodiacMotion.py
```

**For Windows**
```
python ZodiacMotion.py
```

Please watch the video in order to see how the program is used.

[![Watch the video](https://user-images.githubusercontent.com/29302909/75923566-690f8c80-5e76-11ea-9f25-2a667d44e286.png)](https://www.youtube.com/watch?v=6udc7c4_nzE&vq=hd720)
