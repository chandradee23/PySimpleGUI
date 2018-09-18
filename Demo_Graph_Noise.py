import time
import random
import PySimpleGUI as sg


STEP_SIZE=1
SAMPLES = 300
SAMPLE_MAX = 300
CANVAS_SIZE = (300,300)


def main():
    global g_exit, g_response_time

    with sg.FlexForm('Enter graph size') as form:
        layout = [[sg.T('Enter width, height of graph')],
                  [sg.In(size=(6, 1)), sg.In(size=(6, 1))],
                  [sg.Ok(), sg.Cancel()]]

        b,v = form.LayoutAndRead(layout)
        if b is None or b == 'Cancel':
            exit(69)
        w, h = int(v[0]), int(v[1])
        CANVAS_SIZE = (w,h)

    # start ping measurement thread

    sg.ChangeLookAndFeel('Black')
    sg.SetOptions(element_padding=(0,0))

    layout = [  [sg.Quit( button_color=('white','black'))],
               [sg.Graph(CANVAS_SIZE, (0,0), (SAMPLES,SAMPLE_MAX),background_color='black', key='graph')],]

    form = sg.FlexForm('Canvas test', grab_anywhere=True, background_color='black', no_titlebar=False, use_default_focus=False)
    form.Layout(layout)

    form.Finalize()
    graph = form.FindElement('graph')

    prev_response_time = None
    i=0
    prev_x, prev_y = 0, 0
    graph_value = 250
    while True:
        # time.sleep(.2)
        button, values = form.ReadNonBlocking()
        if button == 'Quit' or values is None:
            break
        graph_offset = random.randint(-10, 10)
        graph_value = graph_value + graph_offset
        if graph_value > SAMPLE_MAX:
            graph_value = SAMPLE_MAX
        if graph_value < 0:
            graph_value = 0
        new_x, new_y = i, graph_value
        prev_value = graph_value
        if i >= SAMPLES:
            graph.Move(-STEP_SIZE,0)
            prev_x = prev_x - STEP_SIZE
        graph.DrawLine((prev_x, prev_y), (new_x, new_y), color='white')
        # form.FindElement('graph').DrawPoint((new_x, new_y), color='red')
        prev_x, prev_y = new_x, new_y
        i += STEP_SIZE if i < SAMPLES else 0



if __name__ == '__main__':
    main()
    exit(69)