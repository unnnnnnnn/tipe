# TIPE - Following the sun

* This small project was realised as my oral exam during my 2nd year of CPGE (Classes Préparatoires aux Grandes Écoles).
The topic for this year was "Societal issues (environment, safety, energy)"
I choose to work on the efficiency of solar panels, and how can they be improved.
I thought about pre-calculating the solar position for a set day, and then piloting motors to make a solar panel follow the sun.
The program I wrote is really not efficient in my opinion and could be improved a lot.

* I'm piloting Lego Mindstorms NXT motors to make the solar panel move, and I'm using the nxt-python library (https://github.com/Eelviny/nxt-python). To plot the sun's position, I'm using the ephem library (https://pypi.org/project/ephem/). Part of this project works with Python 2.7, and the other with Python 3 (I'm trying to make it fully work with 2.7)

* I don't have any (of a few) comments on my program, and it's something I need to work on !

* If you are curious about the plateform I built for the solar panel, here is it (quite simple but I might need to add sensors in order to set the initial position). I drilled one of my Lego gear so that I could get 2 different rotations from the same axis. This is based on a concept shown in this video: https://www.youtube.com/watch?v=H_xllHoNJ8o
 
![Img](https://i.imgur.com/vxE9XiP.jpg)
