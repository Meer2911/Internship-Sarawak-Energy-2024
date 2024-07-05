from vsdx import VisioFile

fileName = 'D:\\DataManagementSystem\\CON_June2024_Corporate Services_main_v1.0.vsdx'

with VisioFile(fileName) as vis:
    # find shape by its text on first page
    shape = vis.pages[0].find_shape_by_text('1 General Manager – SG1\n50012277 – Vacant \n')

    # get text color(s) from shape.text to check the text color
    shape.get_text_colors()

    # from the list, get unique elements that have #
    colors = [color for color in shape.get_text_colors() if '#' in color]

    # filter the list to get the color that are unique
    unique_colors = list(set(colors))

    print(unique_colors)