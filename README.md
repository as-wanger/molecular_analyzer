# molecular_analyzer
It's a little tool for my friend to analyze the peptide molecular from mass spectrometer<br>
Since 2022.2.17-

## Step 1 Open a file
You can open a file (***xlsx is recommended***, example_data.xlsx e.g.)<br>
The list will be changed to get the amino_acids, peptide types and input data

## Step 2 (If required) Append Matter
Peptide's tail may be appended with some matter like water<br>
input the matter to multiple the peptide types

## Step 3 Analyze
You need to input to get<br>
***Most nembers one side*** - if input **5**, it means weill get **10** numbers at most,<br>
***First variation*** - if the first one's gap larger than ***First variation***, you won't get any number on this side,<br>
***Near variarion*** - those numbers near by the first get number. Gap smaller than the Near variarion will contain, but limited by ***Most nembers one side***<br>
After this, you should get the result data in bottom-right table

## Step 4 Draw the figure
Open another window to show the data in figure<br>
Also you can open another figure to compare (but override former figure, so remember to save it or just back to main window to redraw)<br>

## Step 5 Save
Since ***xlsx is recommended*** (I implement **molecular weight**, **peptide types**, **input data**, **result data** in different excel sheets which all contain in single page to suit in .csv or .txt will be future goal)<br>
If there's four sheets (as you having a *result1* sheets), it'll add another sheet to put your new result data (sheet name will be *result2*)
