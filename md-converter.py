import markdown
# Open the file for reading and read the input to a temp variable
with open('../WinDynamicDesktop/README.md', 'r') as f:
    tempMd= f.read()

# Convert the input to HTML
tempHtml = markdown.markdown(tempMd)
# If necessary, could print or edit the results at this point.
# Open the HTML file and write the output.
with open('temp.html', 'w') as f:
    f.write(tempHtml)