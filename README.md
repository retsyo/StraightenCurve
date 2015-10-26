#1.What is that?
##1.1 A addon to straighten curve
* This addon straightens Blender Curve, while keeping the length of every segment.<br>
* The origonal Curve can be made up with several curves.<br>
* The straighten line starts at the first vertex of original Curve-converted-Mesh.<br>

##1.2 An exmaple to show how internationalization GUI, i.e. display text in different language
* Please use gettext, and stop doing translate the string directly in your addon source file.<br>
* This addon supplies English and Chinese interface.<br>
<br>
* `However, I don't know how to support bl_info with gettext. If you know, please drop me some light, Thanks.`<br>

#2.Usage
##2.1 basic
* Enable Straighten Curve in Add-ons.<br>
* Select a Curve in 3D Window, click the button under 'Straighten Curve' on 'Tool Shelf'.<br>
* The new staight line has same fill/depth/resolution parameters as the original one.<br>

##2.2 switch language
* Choose language under 'User preferences - system - language', click 'Save User Setting'<br>
* Relaunch Blender and enable this addon again. Currently, this addon supplies Chinese/English translation,<br>
* if you choose other languages, Englsih will be used.<br>
<br>

#3.Version Information
* 2015.10.26 0.4，Can change GUI text according to User Preferences - system - language<br>
* 2015.10.26 0.3，Change to Addon<br>
* 2015.10.26 0.2，The Script can deals with Curve which has many curves<br>
* 2015.10.26 0.1，Initial version<br>
<br>

#4.Author
Lee June @ BlenderCN<br>
<br>

#5.CopyRight
GPL<br>
<br>

#6.Website
https://github.com/retsyo/StraightenCurve<br>

